from events import models
from user.api.serializers import StudentSerializer, CoordinatorSerializer, SpeakerSerializer
from user.models import Speaker
from rest_framework import serializers

class EventTypeModelSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.EventType
        fields = '__all__'

class EventSpeakerModelSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer()

    class Meta:
        model = models.EventSpeaker
        exclude = ['event']

class AddSpeakerSerializer(serializers.ModelSerializer):
    speaker = serializers.PrimaryKeyRelatedField(queryset=Speaker.objects.all())

    class Meta:
        model = models.EventSpeaker
        exclude = ['event']

class CreateSerializer(serializers.ModelSerializer):
    speakers = AddSpeakerSerializer(many=True, required=False)

    class Meta:
        model = models.Event
        exclude = ['faculty', 'organizer', 'participants', 'created_at']  

class ListSerializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    organizer = serializers.StringRelatedField()
    student_organizer = serializers.StringRelatedField()

    class Meta:
        model = models.Event
        fields = [
            'id',
            'title', 
            'start_date', 
            'end_date', 
            'location', 
            'event_type', 
            'promotional_image',
            'organizer',
            'student_organizer',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['start_date'] = instance.start_date.strftime('%Y-%m-%d %H:%M')
        data['end_date'] = instance.end_date.strftime('%Y-%m-%d %H:%M')
        data['speakers'] = EventSpeakerModelSerializer(instance.speakers.all(), many=True).data
        return data

class DetailSerializer(serializers.ModelSerializer):
    event_type = serializers.StringRelatedField()
    organizer = CoordinatorSerializer(required=False)
    student_organizer = StudentSerializer(required=False)
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Event
        exclude = ['participants']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['start_date'] = instance.start_date.strftime('%Y-%m-%d %H:%M')
        data['end_date'] = instance.end_date.strftime('%Y-%m-%d %H:%M')
        data['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M')
        return data
