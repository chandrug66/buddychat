from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Room,Message

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        print(self.user)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        #save to DataBase
        await self.save_message(self.user, self.room_name,message)

        #Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'username': self.user.username
            }
        )


    async def chat_message(self,event):

        username = event['username']
        message = event['message']

        await self.send(text_data = json.dumps(
            {       'message' : message,
                    'username': username
            }
        ))

    @database_sync_to_async
    def save_message(self, user, room_name,content):
        room = Room.objects.get(name=room_name)
        Message.objects.create(
            user = user,
            room = room,
            content = content
        )