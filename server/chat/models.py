import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField('user.Student', related_name='chats')

    def __str__(self):
        return f'Chat {self.pk}'

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_object_id = models.PositiveIntegerField()
    author = GenericForeignKey('author_content_type', 'author_object_id')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.pk}'    
