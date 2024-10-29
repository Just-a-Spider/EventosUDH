from rest_framework import viewsets
from notifications.models import Notification
from .serializers import NotificationSerializer
    
class NotificationList(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
