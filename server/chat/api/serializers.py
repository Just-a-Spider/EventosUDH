from rest_framework import serializers
from chat.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    members = serializers.StringRelatedField(many=True)

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



