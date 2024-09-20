from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import PasswordResetToken
from user.models import User
"""
We need to create a custom serializer to include the role in the token.
This way we can modify permissions based on the role.
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = [ 
            'username',
            'email', 
            'password',
            'first_name', 
            'last_name'
        ]
    
class LoginSerializer(serializers.Serializer):
    email_username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)
    # role = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'email_username',
            'password', 
            # 'role'
        ]

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username',
            'email'
        ]

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name', 
            'last_name', 
            'username',
            'email',
            'role'
        ]

class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = PasswordResetToken
        fields = ['token', 'password']
