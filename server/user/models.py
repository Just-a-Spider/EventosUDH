import uuid
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES=[
        ('student', 'Estudiante'),
        ('coordinator', 'Coordinador'),
        ('speaker', 'Ponente')
    ]
    # Add any other custom fields here
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'
    
    def send_password_reset_email(self):
        token = PasswordResetToken.objects.create(
            email=self.email, 
            token=PasswordResetToken.generate_token()
        )
        token.send_email()

class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def send_email(self):
        send_mail(
            subject='Password reset token',
            message=f'Your password reset token is {self.token}',
            recipient_list=[self.email],
            from_email=settings.EMAIL_HOST_USER,
            html_message=f'Your password reset token is <b>{self.token}</b>',
        )
        pass
    
    @staticmethod
    def generate_token():
        return uuid.uuid4().hex
        

    class Meta:
        verbose_name = 'password reset token'
        verbose_name_plural = 'password reset tokens'
        db_table = 'password_reset_tokens'

    def __str__(self):
        return self.email