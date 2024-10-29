from rest_framework import viewsets
from chat.models import Chat
from .serializers import ChatSerializer

class ChatsListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'chat_id'
    
    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)

class ChatDetailView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'chat_id'
    queryset = Chat.objects.all()
