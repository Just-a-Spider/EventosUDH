from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import PasswordResetToken, User

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
    def register_user(self):
        self.client.post(REGISTER_URL, REGISTER_USER_DATA, format='json')

    def login_user(self):
        self.client.post(LOGIN_URL, LOGIN_USER_DATA, format='json')

class RegisterViewsTests(BaseTest):
    def test_register_success(self):
        response = self.client.post(REGISTER_URL, REGISTER_USER_DATA, format='json')
        self.assertEqual(response.status_code, 201)

    def test_register_existing_user(self):
        self.register_user()
        response = self.client.post(REGISTER_URL, REGISTER_USER_DATA, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'User with this username already exists')

class LoginViewsTests(BaseTest):
    def setUp(self):
        self.register_user()

    def test_login_success(self):
        response = self.client.post(LOGIN_URL, LOGIN_USER_DATA, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Login successful')

    def test_login_invalid_credentials(self):
        invalid_login_data = {
            'email_username': LOGIN_USER_DATA['email_username'],
            'password': 'wrongpassword'
        }
        response = self.client.post(LOGIN_URL, invalid_login_data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Credenciales Incorrectas')

class MeLogoutViewsTests(BaseTest):
    def setUp(self):
        self.register_user()
        self.login_user()

    def test_me_success(self):
        url = reverse('local:me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'id': response.data['id'],
            'username': REGISTER_USER_DATA['username'],
            'first_name': REGISTER_USER_DATA['first_name'],
            'last_name': REGISTER_USER_DATA['last_name'],
            'email': REGISTER_USER_DATA['email']
        }
        self.assertEqual(response.data, expected_data)

    def test_logout_success(self):
        url = reverse('local:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Logout successful')

    # Change the token expiration time to 1 second for testing purposes
    # def test_with_expired_access_token(self): 
    #     import time
    #     time.sleep(4)
    #     url = reverse('me')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RefreshTokenViewTests(BaseTest):
    def setUp(self):
        self.register_user()
        self.login_user()

    def test_refresh_token_success(self):
        url = reverse('local:refresh')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class PasswordResetTests(BaseTest):
    def setUp(self):
        self.register_user()
        self.login_user()

    def test_send_password_reset_token(self):
        url = reverse('local:send-password-reset-token')
        response = self.client.post(url, {'email': REGISTER_USER_DATA['email']}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Correo electrónico enviado')

    def test_password_reset(self):
        url = reverse('local:password-reset')
        token = PasswordResetToken.objects.create(
            email=REGISTER_USER_DATA['email'],
            token=PasswordResetToken.generate_token()
        )
        response = self.client.post(url, {
            'password': 'newpassword123', 
            'token': token.token
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Contraseña restablecida')
