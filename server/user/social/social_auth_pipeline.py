import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse
from user.api.serializers import CustomTokenObtainPairSerializer
from faculties.models import Faculty, FacultyStudent

def login_success_response(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    access_token = refresh.access_token
    refresh_token = str(refresh)
    user.last_login = timezone.now()
    user.save()

    response = HttpResponse('Login successful')
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

