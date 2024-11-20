from notifications.models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

class NotificationList(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    filter_fields = ['seen']
    lookup_field = 'id'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        # Mark notification as seen
        instance = self.get_object()
        instance.seen = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='seen')
    def seen_notifications(self, request):
        queryset = self.get_queryset().filter(seen=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='unseen')
    def unseen_notifications(self, request):
        queryset = self.get_queryset().filter(seen=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_notifications(self, request):
        queryset = self.get_queryset().filter(seen=True)
        queryset.delete()
        return Response(status=204)