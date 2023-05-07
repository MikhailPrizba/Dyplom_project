import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from django.utils import timezone
from django.contrib.auth.models import User
from .models import ChatMessage, ChatRoom
from channels.db import database_sync_to_async

def save_chat_room(chat_room):
    chat_room.save()
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.user1_id = self.scope['url_route']['kwargs']['user1_id']
        self.user2_id = self.scope['url_route']['kwargs']['user2_id']
        self.chat_room_name = f'chat_{self.user1_id}_{self.user2_id}'
        self.room_group_name = 'chat_%s' % self.chat_room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        
        seller = await sync_to_async(User.objects.get)(id=self.user1_id)
        buyer = await sync_to_async(User.objects.get)(id=self.user2_id)
        chat_room = await sync_to_async(ChatRoom.objects.get)(seller=seller, buyer=buyer)

        chat_message = ChatMessage(chat_room = chat_room, user=self.user ,message=message)
        
        await database_sync_to_async(save_chat_room)(chat_message)    
        
        
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))