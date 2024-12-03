from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from events import models as e_models
from faculties import models as f_models
from user import models as u_models

@receiver(post_save, sender=e_models.Event)
def send_notification(sender, instance, created, **kwargs):
    if created:
        # Get the students of the faculty
        faculty = f_models.Faculty.objects.get(id=instance.faculty.id)
        students = faculty.students.all()

        # Send notification to students
        for student in students:
            # Send Realtime Notification
            channel_layer = get_channel_layer()
            user_group = f'{student.__class__.__name__.lower()}_{student.username}_channel'
            message = {
                'type': 'echo.notification',
                'data': 'Nuevo Evento en tu Facultad',
            }
            async_to_sync(channel_layer.group_send)(user_group, message)
            # Send Email to the student
            student.send_email(
                subject='Nuevo Evento en tu Facultad',
                message=f'Se ha creado un nuevo evento en tu facultad: {instance.title}',
            )