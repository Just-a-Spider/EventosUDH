from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from server.middleware.auth import CustomJWTAuthentication
from server.views.custom_views import CustomAuthenticatedModelViewset
from chat.models import Chat
from .serializers import ChatSerializer

class ChatsListView(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'chat_id'
    
    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)

class ChatDetailView(CustomAuthenticatedModelViewset):
    serializer_class = ChatSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'chat_id'
    queryset = Chat.objects.all()
