from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import Student, Coordinator, Speaker

REGISTER_URL = reverse('local:register')
LOGIN_URL = reverse('local:login')
REGISTER_USER_DATA = {
    'username': '2017110918',
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john.doe@udh.edu.pe',
    'password': 'password123',
}
LOGIN_USER_DATA = {
    'email_username': 'john.doe@udh.edu.pe',
    'password': 'password123',
}

class BaseTest(APITestCase):
    # ----------------- STUDENT -----------------
    def register_student(self, raw_data=REGISTER_USER_DATA, code='2017110918'):
        data = raw_data.copy()
        data['code'] = code
        data['role'] = 'student'
        self.client.post(REGISTER_URL, data, format='json')

    def get_student(self, register_data=REGISTER_USER_DATA, code='2017110918'):
        self.register_student(raw_data=register_data, code=code)
        user = Student.objects.get(username=REGISTER_USER_DATA['username'])
        return user

    # ----------------- COORDINATOR -----------------
    def register_coordinator(self, raw_data=REGISTER_USER_DATA):
        data = raw_data.copy()
        data['role'] = 'coordinator'
        self.client.post(REGISTER_URL, data, format='json')

    def get_coordinator(self, register_data=REGISTER_USER_DATA):
        self.register_coordinator(raw_data=register_data)
        user = Coordinator.objects.get(username=REGISTER_USER_DATA['username'])
        return user
    
    # ----------------- GENERAL -----------------
    def login_user(self, data=LOGIN_USER_DATA, role='student'):
        data['role'] = role
        self.client.post(LOGIN_URL, data, format='json')