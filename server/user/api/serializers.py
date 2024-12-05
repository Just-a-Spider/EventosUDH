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
        token['username'] = user.username
        return token

# ----------------- Auth ----------------- 
role_to_model = {
    'student': Student,
    'coordinator': Coordinator,
    'speaker': Speaker,
}
 
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    role = serializers.ChoiceField(choices=['student', 'coordinator', 'speaker'])
    code = serializers.CharField(max_length=22, required=False)
    bio = serializers.CharField(required=False)
    phone = serializers.CharField(max_length=10, required=False)

    def create(self, validated_data):
        role = validated_data.pop('role')
        user_class = role_to_model[role]
        user = user_class(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email_username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['student', 'coordinator', 'speaker'])

# ----------------- User -----------------
class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = instance.__class__.__name__.lower()
        return data

class StudentSerializer(BaseUserSerializer):
    class Meta:
        model = Student
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'code', 
            'profile_picture'
        ]

class CoordinatorSerializer(BaseUserSerializer):
    class Meta:
        model = Coordinator
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'code',
            'profile_picture'
        ]

class SpeakerSerializer(BaseUserSerializer):
    class Meta:
        model = Speaker
        fields = [
            'id',
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'bio', 
            'phone',
            'profile_picture'
        ]

# ----------------- Password Reset -----------------
class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField()

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = PasswordResetToken
        fields = ['token', 'password']
