import uuid
from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey('faculties.Faculty', on_delete=models.CASCADE, related_name='faculty_event_types')

    class Meta:
        db_table = 'event_types'

    def __str__(self):
        return self.name

class Event(models.Model):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)

    # Foreigns
    faculty = models.ForeignKey('faculties.Faculty', on_delete=models.CASCADE, related_name='faculty_events')
    organizer = models.ForeignKey('user.Coordinator', on_delete=models.CASCADE, related_name='coordinator_organizer')
    student_organizer = models.ForeignKey(
        'user.Student', 
        on_delete=models.CASCADE, 
        related_name='student_organizer', 
        null=True,
        blank=True
    )
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name='event_type')
    participants = models.ManyToManyField('user.Student', through='EventParticipant', related_name='participated_events')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'events'

    def __str__(self):
        return self.title
    
class EventParticipant(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='event_participants')
    user = models.ForeignKey('user.Student', on_delete=models.CASCADE, related_name='events_participated')
    attended = models.BooleanField(default=False)

    class Meta:
        db_table = 'event_participants'

    def __str__(self):
        return f'{self.user} - {self.event}'
