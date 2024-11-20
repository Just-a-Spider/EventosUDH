import uuid
from django.db import models

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    seen = models.BooleanField(default=False)

    # Foreigns
    user = models.ForeignKey('user.Student', on_delete=models.CASCADE, related_name='notifications')

    # Meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

