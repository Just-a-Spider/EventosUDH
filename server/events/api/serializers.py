from events import models
from user.api.serializers import StudentSerializer, CoordinatorSerializer, SpeakerSerializer
from user.models import Speaker
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

def add_speaker_to_event(event, speaker_data):
    email = speaker_data['email']
    username = speaker_data['email'].split('@')[0]
    first_name = speaker_data['first_name']
    last_name = speaker_data['last_name']
    subject = speaker_data['subject']

    to_be_password = first_name

    speaker, _ = Speaker.objects.get_or_create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        defaults={
            'password': make_password(to_be_password),
            'bio': 'Sin bio',
            'phone': 'Sin num',
        }
    )

    event_speaker = models.EventSpeaker.objects.create(
        event=event,
        speaker=speaker,
        subject=subject
    )

    return event_speaker

def modify_speakers(event, speakers_data):
    # Get the speakers that are already in the event
    event_speakers_emails = event.event_speakers.values_list('speaker__email', flat=True)

    # Delete the speakers that are not in the new list
    for event_speaker in event.event_speakers.all():
        if event_speaker.speaker.email not in [speaker_data['email'] for speaker_data in speakers_data]:
            event_speaker.delete()

    for speaker_data in speakers_data:
        speaker_email = speaker_data.get('email', None)
        if speaker_email and speaker_email not in event_speakers_emails:
            add_speaker_to_event(event, speaker_data)
        elif speaker_email:
            event_speakers = models.EventSpeaker.objects.filter(
                event=event,
                speaker__email=speaker_email
            )
            for event_speaker in event_speakers:
                event_speaker.subject = speaker_data['subject']
                event_speaker.save()

class EventTypeModelSerializer(serializers.ModelSerializer):
    faculty = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.EventType
        fields = '__all__'

class EventSpeakerModelSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer()

    class Meta:
        model = models.EventSpeaker
        fields = ['speaker', 'subject']

class CreateSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    speakers =serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = models.Event
        exclude = ['faculty', 'organizer', 'participants', 'created_at']  

    def create(self, validated_data):
        speakers_data = validated_data.pop('speakers', [])

        # Data cleaning
        location = validated_data.pop('location', None)
        student_organizer = validated_data.pop('student_organizer', None)
        if student_organizer == '':
            student_organizer = None
        if location == '':
            location = None

        validated_data['location'] = location
        validated_data['student_organizer'] = student_organizer

        # Instance Creation
        event = models.Event.objects.create(**validated_data)

        # Speakers Creation or Update
        if speakers_data.__len__() > 0:
            for speaker_data in speakers_data:
                modify_speakers(event, speaker_data)

        return event
    
    def update(self, instance, validated_data):
        speakers_data = validated_data.pop('speakers', [])
        location = validated_data.pop('location', None)
        student_organizer = validated_data.pop('student_organizer', None)
        if student_organizer == '':
            student_organizer = None
        if location == '':
            location = None

        instance.location = location
        instance.student_organizer = student_organizer
        instance.title = validated_data.get('title', instance.title)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.event_type = validated_data.get('event_type', instance.event_type)
        instance.promotional_image = validated_data.get('promotional_image', instance.promotional_image)
        instance.save()

        # Speakers Creation or Update
        if speakers_data.__len__() > 0:
            modify_speakers(instance, speakers_data)
        else:
            instance.event_speakers.all().delete()

        return instance
    
    def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['speakers'] = SpeakerSerializer(instance.speakers.all(), many=True).data
            return representation

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
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            if instance.promotional_image:
                promotional_image_url = instance.promotional_image.url
                representation['promotional_image'] = request.build_absolute_uri(promotional_image_url)
            else:
                representation['promotional_image'] = None
        return representation

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
        data['speakers'] = EventSpeakerModelSerializer(instance.event_speakers.all(), many=True).data
        data['is_participant'] = instance.participants.filter(id=self.context['request'].user.id).exists()
        return data
