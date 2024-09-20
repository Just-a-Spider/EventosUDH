import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from server.asgi import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

WS_PREFIX = 'ws/notifications/'

@database_sync_to_async
def create_users(username, email, password, username_2, email_2, password_2):
    user = get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    user_2 = get_user_model().objects.create_user(
        username=username_2,
        email=email_2,
        password=password_2,
    )
    
    token = AccessToken.for_user(user)
    return user, token

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True) 
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_users(
            'jonedoe', 'test.user@gmail.com', 'Test0116p',
            'janedoe', 'test.user2@gmail.com','Test0116p1'
        )
        communicator = WebsocketCommunicator(application, f'{WS_PREFIX}{user.id}/')
        communicator.scope['headers'].append(
            (b'cookie', f'access_token={access}'.encode())
        )
        
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_receive_notifications(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_users(
            'jonedoe', 'test.user@gmail.com', 'Test0116p',
            'janedoe', 'test.user2@gmail.com','Test0116p1'
        )
        communicator = WebsocketCommunicator(application, f'{WS_PREFIX}{user.id}/')
        communicator.scope['headers'].append(
            (b'cookie', f'access_token={access}'.encode())
        )
        connected, _ = await communicator.connect()
        assert connected is True
        # Send a notification message to the group
        message = {
            'type': 'echo.notification',
            'data': 'This is a test notification.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(f'user_{user.id}_channel', message)
        # Receive the message from the WebSocket
        response = await communicator.receive_json_from()
        assert response == message
        # Disconnect the WebSocket
        await communicator.disconnect()
        

    async def test_cannot_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_users(
            'jonedoe', 'test.user@gmail.com', 'Test0116p',
            'janedoe', 'test.user2@gmail.com','Test0116p1'
        )
        communicator = WebsocketCommunicator(application, f'{WS_PREFIX}{user.id}/')
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()
