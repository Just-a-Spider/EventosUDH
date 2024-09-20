from . import views
from django.urls import path

app_name = 'user'

urlpatterns = [
    # Account Related
    path('register/', views.RegisterView.as_view(), name='register'),
    path(
        'send-password-reset-token/', 
        views.GetSendPasswordReset.as_view(), 
        name='send-password-reset-token'
    ),
    path(
        'password-reset/', 
        views.PasswordResetView.as_view(), 
        name='password-reset'
    ),

    # Session Related
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.MeView.as_view(), name='me'),
]
