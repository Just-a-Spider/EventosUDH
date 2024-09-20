from events import models
from user.api.serializers import SimpleUserSerializer
from rest_framework import serializers

class EventTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventType
        fields = '__all__'

class SimpleEventModelSerializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    faculty = serializers.StringRelatedField()

    class Meta:
        model = models.Event
        fields = '__all__'

class CreateEventModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        exclude = ['organizer', 'faculty']

class FullEventModelSerializer(serializers.ModelSerializer):
    organizer = SimpleUserSerializer(required=False)
    student_organizer = SimpleUserSerializer(required=False)
    participants = SimpleUserSerializer(many=True, read_only=True)
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Event
        fields = '__all__'

class EventParticipantModelSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = models.EventParticipant
        fields = '__all__'
