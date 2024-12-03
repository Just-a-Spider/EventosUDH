import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from user.api.serializers import CustomTokenObtainPairSerializer
from faculties.models import Faculty, FacultyStudent
from django.shortcuts import redirect


from social_core.pipeline.partial import partial
from user.models import Student
@partial
def create_student(backend, user=None, response=None, *args, **kwargs):
    if user:
        return {'user': user}

    email = response.get('email')
    first_name = response.get('given_name')
    last_name = response.get('family_name')
    username = response.get('email').split('@')[0]

    # Create an encrypted password
    password = make_password(None)

    # Check if a Student with the given username already exists
    student, created = Student.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'code': username,
            'password': password
        }
    )

    return {'user': student}


from social_core.pipeline.social_auth import associate_user as social_associate_user
def associate_student(backend, uid, user=None, social=None, *args, **kwargs):
    if user:
        return {'social': social}

    return social_associate_user(backend, uid, user, social, *args, **kwargs)

def login_success_response(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    access_token = refresh.access_token
    refresh_token = str(refresh)
    user.last_login = timezone.now()
    user.save()

    response = redirect(settings.LOGIN_REDIRECT_URL)
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=str(access_token),
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    return response

def fetch_google_classroom_courses(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    access_token = response.get('access_token')
    if not access_token:
        return

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Fetch the user's Google Classroom courses
    courses_url = 'https://classroom.googleapis.com/v1/courses'
    response = requests.get(courses_url, headers=headers)
    if response.status_code != 200:
        return

    # Ensure the user is a Student instance
    if not isinstance(user, Student):
        raise ValueError(f"Cannot query {user}: Must be a 'Student' instance.")

    courses_data = response.json().get('courses', [])

    # Use a transaction to ensure atomicity
    with transaction.atomic():
        linked_faulties = False

        for course_data in courses_data:
            if course_data.get('courseState') != 'ACTIVE':
                continue

            # course_name = course_data.get('name')
            course_faculty = course_data.get('descriptionHeading').split(': ')[1]

            if not linked_faulties:
                faculty, _ = Faculty.objects.get_or_create(name=course_faculty)
                FacultyStudent.objects.get_or_create(faculty=faculty, student=user)
                linked_faulties = True

    # Login the user with JWT from the user's view
    return login_success_response(user)

