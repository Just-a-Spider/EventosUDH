from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import User, PasswordResetToken

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='2017110918',
            email='johndoe@example.com',
            password='password123',
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, '2017110918')
        self.assertEqual(self.user.email, 'johndoe@example.com')
        self.assertTrue(self.user.check_password('password123'))

class PasswordResetTokenModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='2017110918',
            email='johndoe@example.com',
            password='password123'
        )
        self.token = PasswordResetToken.objects.create(
            email=self.user.email,
            token=PasswordResetToken.generate_token()
        )

    def test_password_reset_token_creation(self):
        self.assertEqual(self.token.email, self.user.email)
        self.assertIsNotNone(self.token.token)
        self.assertTrue(len(self.token.token) > 0)