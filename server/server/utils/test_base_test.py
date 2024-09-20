from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User

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
    def register_user(self, data=REGISTER_USER_DATA):
        self.client.post(REGISTER_URL, data, format='json')

    def login_user(self, data=LOGIN_USER_DATA):
        self.client.post(LOGIN_URL, data, format='json')

    def register_coordinator(self):
        self.client.post(REGISTER_URL, REGISTER_USER_DATA, format='json')
        # Change the role of the user to coordinator
        user = User.objects.get(username=REGISTER_USER_DATA['username'])
        user.role = 'coordinator'
        user.save()

    def get_coordinator(self, register_data=REGISTER_USER_DATA, login_data=LOGIN_USER_DATA):
        self.register_user(data=register_data)
        # Change the role of the user to coordinator
        user = User.objects.get(username=REGISTER_USER_DATA['username'])
        user.role = 'coordinator'
        user.save()
        return user

    def get_user(self, register_data=REGISTER_USER_DATA, login_data=LOGIN_USER_DATA):
        self.register_user(data=register_data)
        self.login_user(data=login_data)
        user = User.objects.get(username=REGISTER_USER_DATA['username'])
        return user