from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from server.middleware.auth_classes import role_to_model
from faculties.models import Faculty
from events import models
from events.api import serializers
from user.api.serializers import StudentSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    lookup_field = 'id'
    pagination_class = LimitOffsetPagination
    
    # Methods
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SimpleEventModelSerializer
        elif self.action == 'create' or self.action == 'update' :
            return serializers.SimpleEventModelSerializer
        return serializers.FullEventModelSerializer
    
    def perform_create(self, serializer):
        if (
            self.request.user.__class__ != role_to_model.get('coordinator') 
            or not 
            Faculty.objects.filter(coordinator=self.request.user).exists()
        ):
            raise PermissionDenied('You are not allowed to create events')
        serializer.save(
            organizer=self.request.user,
            faculty = Faculty.objects.get(coordinator=self.request.user),
        )

    def perform_update(self, serializer):
        if self.request.user.__class__ != role_to_model.get('coordinator'):
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
        if self.request.user.__class__ != role_to_model.get('coordinator'):
            raise PermissionDenied('You are not allowed to delete events')
        instance.delete()

    # Custom actions 
    @action(detail=True, methods=['get'], url_path='join-event')
    def join_event(self, request, id):
        event = self.get_object()
        event.participants.add(request.user)
        return Response(
            {'message': 'You have been added to the event'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'], url_path='leave-event')
    def leave_event(self, request, id):
        event = self.get_object()
        event.participants.remove(request.user)
        return Response(
            {'message': 'You have been removed from the event'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'], url_path='participants')
    def get_participants(self, request, id):
        event = self.get_object()
        participants = event.participants.all()
        serializer = StudentSerializer(participants, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
from server.permissions import IsCoordinator
from rest_framework.permissions import IsAuthenticated

class EventTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventTypeModelSerializer
    permission_classes = [IsAuthenticated, IsCoordinator]
