from django.urls import reverse
from user.models import PasswordResetToken
from server.utils.test_base_test import BaseTest

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

class RegisterViewsTests(BaseTest):
    def test_register_student_success(self):
        data = REGISTER_USER_DATA.copy()
        data['role'] = 'student'
        response = self.client.post(REGISTER_URL, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['detail'], 'Student registered')

    def test_register_coordinator_success(self):
        data = REGISTER_USER_DATA.copy()
        data['role'] = 'coordinator'
        response = self.client.post(REGISTER_URL, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['detail'], 'Coordinator registered')

    def test_register_speaker_success(self):
        data = REGISTER_USER_DATA.copy()
        data['role'] = 'speaker'
        response = self.client.post(REGISTER_URL, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['detail'], 'Speaker registered')

class LoginViewsTests(BaseTest):
    def setUp(self):
        self.register_student()
        self.register_coordinator()

    def test_login_student_success(self):
        login_data = LOGIN_USER_DATA.copy()
        login_data['role'] = 'student'
        response = self.client.post(LOGIN_URL, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Login successful')

    def test_login_invalid_credentials(self):
        invalid_login_data = {
            'email_username': LOGIN_USER_DATA['email_username'],
            'password': 'wrongpassword',
            'role': 'student'
        }
        response = self.client.post(LOGIN_URL, invalid_login_data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Credenciales Incorrectas')

class MeLogoutViewsTests(BaseTest):
    def setUp(self):
        self.register_student()
        self.register_coordinator()

    def test_me_student_success(self):
        self.login_user()
        url = reverse('local:me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'username': REGISTER_USER_DATA['username'],
            'email': REGISTER_USER_DATA['email'],
            'first_name': REGISTER_USER_DATA['first_name'],
            'last_name': REGISTER_USER_DATA['last_name'],
            'code': REGISTER_USER_DATA['username']
        }
        self.assertEqual(response.data, expected_data)

    def test_me_coordinator_success(self):
        self.login_user(role='coordinator')
        url = reverse('local:me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'username': REGISTER_USER_DATA['username'],
            'email': REGISTER_USER_DATA['email'],
            'first_name': REGISTER_USER_DATA['first_name'],
            'last_name': REGISTER_USER_DATA['last_name'],
            'code': ''
        }
        self.assertEqual(response.data, expected_data)
    
    def test_logout_success(self):
        self.login_user()
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
        self.register_student()
        self.login_user()

    def test_refresh_token_success(self):
        url = reverse('local:refresh')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class PasswordResetTests(BaseTest):
    def setUp(self):
        self.register_student()
        self.login_user()

    def test_send_password_reset_token(self):
        url = reverse('local:send-password-reset-token')
        response = self.client.post(url, {'email': REGISTER_USER_DATA['email'], 'role': 'student'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Correo electrónico enviado')

    def test_password_reset(self):
        url = reverse('local:password-reset')
        token = PasswordResetToken.objects.create(
            email=REGISTER_USER_DATA['email'],
            token=PasswordResetToken.generate_token(),
            role='student'
        )
        response = self.client.post(url, {
            'password': 'newpassword123', 
            'token': token.token
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Contraseña restablecida')
