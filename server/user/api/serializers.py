from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import PasswordResetToken
from user.models import Student, Coordinator, Speaker
"""
We need to create a custom serializer to include the role in the token.
This way we can modify permissions based on the role.
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        user_class = str(user.__class__.__name__)
        token['role'] = user_class.lower()
        return token

# ----------------- Auth -----------------  
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    code = serializers.CharField(max_length=22, required=False)
    phone = serializers.CharField(max_length=9, required=False)
    role = serializers.CharField(write_only=True)
    
class LoginSerializer(serializers.Serializer):
    email_username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True, required=False)

# ----------------- User -----------------
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'email', 'first_name', 'last_name', 'code']

class CoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinator
        fields = ['username', 'email', 'first_name', 'last_name', 'code']

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['username', 'email', 'first_name', 'last_name']

# ----------------- Password Reset -----------------
class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField()

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = PasswordResetToken
        fields = ['token', 'password']
