from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        user_group = f'user_{instance.user.id}'
        message = {
            'type': 'echo.notification',
            'data': instance.body,
        }
        async_to_sync(channel_layer.group_send)(user_group, message)