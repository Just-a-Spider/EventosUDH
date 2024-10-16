from events import models
from user.api.serializers import StudentSerializer, CoordinatorSerializer, SpeakerSerializer
from rest_framework import serializers

class EventTypeModelSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.EventType
        fields = '__all__'

class SimpleEventModelSerializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()

    class Meta:
        model = models.Event
        exclude = ['organizer', 'faculty']

class FullEventModelSerializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    organizer = CoordinatorSerializer(required=False)
    student_organizer = StudentSerializer(required=False)
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Event
        exclude = ['participants']
