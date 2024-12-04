from django.urls import path, include

urlpatterns = [
    path('auth/', include('user.api.urls', namespace='local')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('chats/', include('chat.api.urls')),
    path('notifications/', include('notifications.api.urls')),
    path('', include('events.api.urls')),
]
