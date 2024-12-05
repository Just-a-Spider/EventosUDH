from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from server.middleware.auth_classes import role_to_model
from faculties.models import Faculty
from events import models
from events.api import serializers
from user.api.serializers import StudentSerializer, SpeakerSerializer
from user.models import Speaker
    
from server.permissions import IsCoordinator
from rest_framework.permissions import IsAuthenticated

class EventTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventTypeModelSerializer
    permission_classes = [IsAuthenticated, IsCoordinator]

    def get_queryset(self):
        return models.EventType.objects.filter(faculty=self.request.user.faculty)
    
    def perform_create(self, serializer):
        serializer.save(faculty=self.request.user.faculty)
    
class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [IsAuthenticated, IsCoordinator]

    def perform_create(self, serializer):
        serializer.save(password='1234')
    
    def perform_update(self, serializer):
        instance = self.get_object()
        validated_data = serializer.validated_data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
    
    def perform_destroy(self, instance):
        instance.delete()

class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    lookup_field = 'id'
    pagination_class = LimitOffsetPagination

    # Methods
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'my_events':
            return serializers.ListSerializer
        elif self.action == 'create' or self.action == 'update' :
            return serializers.CreateSerializer
        return serializers.DetailSerializer
    
    def perform_create(self, serializer):
        if (
            self.request.user.__class__ != role_to_model.get('coordinator') 
        ):
            raise PermissionDenied('You are not allowed to create events')
        serializer.save(
            organizer=self.request.user,
            faculty = self.request.user.faculty,
        )
        return Response(
            {'message': 'Event created successfully'},
            status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        event = self.get_object()

        if (
            self.request.user.__class__ != role_to_model.get('coordinator')
            or not
            self.request.user == event.organizer
        ):
            raise PermissionDenied('You are not allowed to update events')

        instance = self.get_object()
        validated_data = serializer.validated_data
        print(validated_data)

        serializer.update(instance, validated_data)

    def perform_destroy(self, instance):
        if self.request.user.__class__ != role_to_model.get('coordinator'):
            raise PermissionDenied('You are not allowed to delete events')
        instance.delete()

    # Custom actions 
    @action(detail=True, methods=['get'], url_path='join-event')
    def join_event(self, request, id):
        event = self.get_object()

        if event.participants.filter(id=request.user.id).exists():
            return Response(
                {'message': 'You are already in the event'},
                status=status.HTTP_400_BAD_REQUEST
            )

        event.participants.add(request.user)
        return Response(
            {'message': 'You have been added to the event'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'], url_path='leave-event')
    def leave_event(self, request, id):
        event = self.get_object()

        if not event.participants.filter(id=request.user.id).exists():
            return Response(
                {'message': 'You are not in the event'},
                status=status.HTTP_400_BAD_REQUEST
            )

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
    
    @action(detail=False, methods=['get'], url_path='my-events')
    def my_events(self, request):
        events = models.Event.objects.filter(participants=request.user)
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = serializers.ListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = serializers.ListSerializer(events, many=True, context={'request': request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
