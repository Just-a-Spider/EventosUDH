from django.urls import path
from . import views

urlpatterns = [
    path(
        'types/', 
        views.EventTypeViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='event-types-list'
    ),
    path(
        '', 
        views.EventListViewSet.as_view({'get': 'list'}),
        name='events-list'
    ),
    path(
        'create/', 
        views.EventCreateAPI.as_view(),
        name='event-create'
    ),
    path(
        '<uuid:id>/', 
        views.EventViewSet.as_view({
            'get': 'retrieve', 
            'patch': 'update', 
            'delete': 'destroy'
        }),
        name='event-detail'
    ),
    path(
        '<uuid:id>/add-participant/', 
        views.EventViewSet.as_view({'post': 'add_participant'}),
        name='event-add-participant'
    ),
]
