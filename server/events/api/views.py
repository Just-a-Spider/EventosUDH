from . import serializers
from rest_framework import status
from rest_framework.response import Response
from server.views.custom_views import CustomAuthenticatedModelViewset, CustomAuthenticatedAPIView
from events import models
from faculties.models import Faculty
from rest_framework.exceptions import PermissionDenied
from server.middleware.auth_classes import role_to_model

class EventTypeViewSet(CustomAuthenticatedModelViewset):
    serializer_class = serializers.EventTypeModelSerializer
    queryset = models.EventType.objects.all()

class EventListViewSet(CustomAuthenticatedModelViewset):
    serializer_class = serializers.SimpleEventModelSerializer
    queryset = models.Event.objects.all()

class EventCreateAPI(CustomAuthenticatedAPIView):
    serializer_class = serializers.CreateEventModelSerializer
    queryset = models.Event.objects.all()

    def post(self, request):
        if request.user.__class__ != role_to_model.get('coordinator') or not Faculty.objects.filter(coordinator=request.user).exists():
            raise PermissionDenied('You are not allowed to create events')
        new_event = models.Event.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date'],
            location=request.data['location'],
            event_type=models.EventType.objects.get(id=request.data['event_type']),
            organizer=self.request.user,
            faculty = Faculty.objects.get(coordinator=self.request.user),
        )
        new_event.save()
        return Response(
            {'message': 'Event created successfully'}, 
            status=status.HTTP_201_CREATED
        )

class EventViewSet(CustomAuthenticatedModelViewset):
    serializer_class = serializers.FullEventModelSerializer
    queryset = models.Event.objects.all()
    lookup_field = 'id'

    def add_participant(self, request, id):
        event = self.get_object()
        event.participants.add(request.user)
        return Response(
            {'message': 'You have been added to the event'},
            status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        if self.request.user.__class__ == role_to_model.get('student'):
            raise PermissionDenied('You are not allowed to update events')

        instance = self.get_object()
        validated_data = serializer.validated_data

        # Fields to update
        fields_to_update = {
            'organizer': self.request.user,
            'faculty': Faculty.objects.get(coordinator=self.request.user),
            'student_organizer': None
        }

        for field, default_value in fields_to_update.items():
            if field in validated_data:
                validated_data[field] = validated_data[field]
            elif default_value is not None:
                validated_data[field] = default_value

        serializer.update(instance, validated_data)

    def perform_destroy(self, instance):
        if self.request.user.__class__ == role_to_model.get('student'):
            raise PermissionDenied('You are not allowed to delete events')
        instance.delete()
