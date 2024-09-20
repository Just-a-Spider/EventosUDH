from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from server.middleware.auth import CustomJWTAuthentication
from server.utils.user_utils import authenticate_user, set_token_cookie
from server.views.custom_views import CustomAuthenticatedAPIView
from django.db.utils import IntegrityError
from user import models
from . import serializers

class RegisterView(APIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = models.User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
            )
            return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'detail': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': 'Datos de entrada no válidos'}, status=status.HTTP_400_BAD_REQUEST)
        email_username = serializer.validated_data.get('email_username')
        password = serializer.validated_data.get('password')

        try:
            if '@' in email_username:
                user = models.User.objects.get(email=email_username)
            else:
                user = models.User.objects.get(username=email_username)      
        except models.User.DoesNotExist:
            return Response({'detail': 'Usuario no Encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return authenticate_user(user, password)

class LogoutView(CustomAuthenticatedAPIView):

    def get(self, request):
        response = Response({'detail': 'Logout successful'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class MeView(RetrieveAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer
    
    def get_object(self):
        user = self.request.user
        if not user:
            raise NotFound('User not found')
        return user

class RefreshTokenView(CustomAuthenticatedAPIView):

    def get(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'No se encontró el token de refresco'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Create a new access token
            new_refresh_token = serializers.CustomTokenObtainPairSerializer.get_token(request.user)
            new_access_token = new_refresh_token.access_token
            response = Response({'detail': 'Token de refresco exitoso'})
            set_token_cookie(response, new_access_token)
            return response

        except Exception as e:
            print(e)
            return Response({'detail': 'Token de refresco no válido'}, status=status.HTTP_400_BAD_REQUEST)
        
class GetSendPasswordReset(APIView):
    serializer_class = serializers.SendEmailSerializer

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Correo electrónico no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        user.send_password_reset_email()
        return Response({'detail': 'Correo electrónico enviado'}, status=status.HTTP_200_OK)
        
class PasswordResetView(APIView):
    serializer_class = serializers.PasswordResetTokenSerializer

    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        if not token or not password:
            return Response({'detail': 'Token o contraseña no proporcionados'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = models.PasswordResetToken.objects.get(token=token)
            user = models.User.objects.get(email=token.email)
            user.set_password(password)
            user.save()
            # Delete all the tokens for the user
            serializers.PasswordResetToken.objects.filter(email=token.email).delete()
            return Response({'detail': 'Contraseña restablecida'}, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except serializers.PasswordResetToken.DoesNotExist:
            return Response({'detail': 'Token no encontrado'}, status=status.HTTP_404_NOT_FOUND)
