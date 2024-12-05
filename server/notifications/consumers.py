from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    user_channel = 'user_channel'
    
    async def connect(self): 
        user = self.scope['user']
        user_username = self.scope['url_route']['kwargs']['user_username']
        
        if user.is_anonymous or user.username != user_username:
            await self.close()
        else:
            self.user_channel = f'{user.__class__.__name__.lower()}_{user_username}_channel'
            await self.channel_layer.group_add(self.user_channel, self.channel_name)
            await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.user_channel, self.channel_name)
        await super().disconnect(code)

    async def receive(self, text_data):
        data = json.loads(text_data)

    async def echo_notification(self, event):
        await self.send(text_data=json.dumps(event))
