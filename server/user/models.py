import uuid
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomBaseUserManager(BaseUserManager):
    def create_user(self, username, email, password, first_name, last_name):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, first_name, last_name):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomBaseUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    password = models.CharField(_('password'), max_length=128)
    email = models.EmailField(unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomBaseUserManager()

    def __str__(self):
        return self.username + ' - ' + self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        help_text=_('Specific permissions for this user.'),
    )
    
    def send_password_reset_email(self):
        token = PasswordResetToken.objects.create(
            email=self.email, 
            token=PasswordResetToken.generate_token(),
            role=self.__class__.__name__.lower()
        )
        token.send_email()

class Student(CustomBaseUser):
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        db_table = 'students'

class Coordinator(CustomBaseUser):
    code = models.CharField(max_length=22, unique=True)

    class Meta:
        verbose_name = 'Coordinador'
        verbose_name_plural = 'Coordinadores'
        db_table = 'coordinators'

class Speaker(CustomBaseUser):
    bio = models.TextField()
    phone = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = 'Ponente'
        verbose_name_plural = 'Ponentes'
        db_table = 'speakers'

class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
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