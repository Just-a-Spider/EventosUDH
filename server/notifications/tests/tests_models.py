from django.test import TestCase
from notifications.models import Notification
from user.models import Student

class NotificationModelTest(TestCase):
    def setUp(self):
        user = Student.objects.create_user(
            username='2017110918',
            email='testuser@gmail.com',
            password='Test0116p',
            first_name='Test',
            last_name='User'
        )
        Notification.objects.create(
            title='Test notification', 
            body='This is a test notification.',
            user=user
        )

    def test_notification_model(self):
        notification = Notification.objects.get(title='Test notification')
        self.assertEqual(notification.body, 'This is a test notification.')

    def test_notification_str(self):
        notification = Notification.objects.get(title='Test notification')
        self.assertEqual(str(notification), 'Test notification')