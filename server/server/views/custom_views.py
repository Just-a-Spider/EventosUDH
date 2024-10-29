from rest_framework_simplejwt.views import TokenObtainPairView
from user.api.serializers import CustomTokenObtainPairSerializer

# Custom TokenObtainPairView to include the role in the token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
