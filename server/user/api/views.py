from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from server.middleware.auth_classes import role_to_model, serializer_class_map
from server.utils.user_utils import authenticate_user, set_token_cookie
from django.db.utils import IntegrityError
from user import models
from . import serializers

class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({'detail': f'{user.__class__.__name__.capitalize()} registered'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'detail': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': 'Datos de entrada no válidos'}, status=status.HTTP_400_BAD_REQUEST)
        email_username = serializer.validated_data.get('email_username')
        password = serializer.validated_data.get('password')
        role = serializer.validated_data.get('role')

        if role not in role_to_model:
            return Response({'detail': 'Rol no válido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            model = role_to_model[role]

        try:
            if '@' in email_username:
                user = model.objects.get(email=email_username)
            else:
                user = model.objects.get(username=email_username)      
        except model.DoesNotExist:
            return Response({'detail': 'Usuario no Encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return authenticate_user(user, password)

class LogoutView(APIView):
    def get(self, request):
        response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', path='/', domain=None, samesite='None')
        response.delete_cookie('refresh_token', path='/', domain=None, samesite='None')
        response.delete_cookie('sessionid', path='/', domain=None, samesite='None')
        return response

class MeView(RetrieveAPIView):
    def get_serializer_class(self):
        user = self.request.user
        user_class_name = user.__class__.__name__
        return serializer_class_map[user_class_name]
    
    def get_object(self):
        user = self.request.user
        if not user:
            raise NotFound('User not found')
        return user

class ProfileView(APIView):
    def get_serializer_class(self):
        user = self.request.user
        user_class_name = user.__class__.__name__
        return serializer_class_map[user_class_name]
    
    def post(self, request):
        user = request.user
        serializer = self.get_serializer_class()(user, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'detail': 'Perfil actualizado'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


class RefreshTokenView(APIView):
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
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.SendEmailSerializer

    def post(self, request):
        email = request.data.get('email')
        role = request.data.get('role')
        if not email:
            return Response({'detail': 'Correo electrónico no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_model = role_to_model.get(role)
        if not user_model:
            return Response({'detail': 'Rol no válido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = user_model.objects.get(email=email)            
        except user_model.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        user.send_password_reset_email()
        return Response({'detail': 'Correo electrónico enviado'}, status=status.HTTP_200_OK)
        
class PasswordResetView(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.PasswordResetTokenSerializer

    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        if not token or not password:
            return Response({'detail': 'Token o contraseña no proporcionados'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_obj = models.PasswordResetToken.objects.get(token=token)
            user_model = role_to_model.get(token_obj.role)
            if not user_model:
                return Response({'detail': 'Rol no válido'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = user_model.objects.get(email=token_obj.email)
            user.set_password(password)
            user.save()
            # Delete all the tokens for the user
            models.PasswordResetToken.objects.filter(email=token_obj.email).delete()
            return Response({'detail': 'Contraseña restablecida'}, status=status.HTTP_200_OK)
        except models.PasswordResetToken.DoesNotExist:
            return Response({'detail': 'Token no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except user_model.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
