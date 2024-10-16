from rest_framework import viewsets, views
from server.middleware.auth import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from user.api.serializers import CustomTokenObtainPairSerializer

# Custom TokenObtainPairView to include the role in the token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class AuthenticatedModelViewset(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

class AuthenticatedAPIView(views.APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]