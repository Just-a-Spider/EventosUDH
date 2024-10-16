from events import models
from user.api.serializers import StudentSerializer, CoordinatorSerializer, SpeakerSerializer
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
    organizer = CoordinatorSerializer(required=False)
    student_organizer = StudentSerializer(required=False)
    participants = StudentSerializer(many=True, read_only=True)
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Event
        fields = '__all__'

class EventParticipantModelSerializer(serializers.ModelSerializer):
    user = StudentSerializer()

    class Meta:
        model = models.EventParticipant
        fields = '__all__'
