from django.urls import path
from rest_framework.routers import DefaultRouter
from ..consumers import NotificationConsumer
from .views import NotificationList

router = DefaultRouter()
router.register(r'', NotificationList, basename='notifications')

urlpatterns = router.urls

websocket_urlpatterns = [
    path('ws/notifications/<str:user_username>/', NotificationConsumer.as_asgi()),
]
