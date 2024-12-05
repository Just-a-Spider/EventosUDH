from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('events', views.EventViewSet, basename='events')
router.register('event-types', views.EventTypeViewSet, basename='event_types')
router.register('speakers', views.SpeakerViewSet, basename='speakers')

urlpatterns = router.urls
