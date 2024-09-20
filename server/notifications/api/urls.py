from django.urls import path
from ..consumers import NotificationConsumer
from .views import NotificationList

urlpatterns = [
    path('student/', NotificationList.as_view({'get': 'list'}), name='student-notifications'),
]

websocket_urlpatterns = [
    path('ws/notifications/<int:user_id>/', NotificationConsumer.as_asgi()),
]
