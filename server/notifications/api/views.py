from rest_framework import viewsets
from server.views.custom_views import CustomAuthenticatedModelViewset
from notifications.models import Notification
from .serializers import NotificationSerializer
    
class NotificationList(CustomAuthenticatedModelViewset):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
