from rest_framework import serializers
from chat.models import Chat, Message
from user import models as user_models
from user.api import serializers as user_serializers

class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    members = serializers.StringRelatedField(many=True, read_only=True)

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return last_message.content
        return None

    class Meta:
        model = Chat
        fields = [
            'id', 
            'last_message',
            'members',
            'created_at', 
        ]

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        if isinstance(obj.author, user_models.Student):
            return user_serializers.StudentSerializer(obj.author).data
        elif isinstance(obj.author, user_models.Coordinator):
            return user_serializers.CoordinatorSerializer(obj.author).data
        elif isinstance(obj.author, user_models.Speaker):
            return user_serializers.SpeakerSerializer(obj.author).data
        return None

    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'author',
            'content',
            'created_at',
        ]
