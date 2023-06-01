"""В модуле определен класс ChatConsumer, который наследуется от
AsyncWebsocketConsumer.

Модуль импортирует необходимые библиотеки и классы: json,
asgiref.sync.async_to_sync, asgiref.sync.sync_to_async,
database_sync_to_async, AsyncWebsocketConsumer, User, timezone,
ChatMessage, ChatRoom. В классе ChatConsumer определены четыре метода:
connect, disconnect, receive, chat_message.
"""

import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils import timezone

from .models import ChatMessage, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    """Класс ChatConsumer реализует WebSocket для обработки чата между двумя
    пользователями."""

    async def connect(self):
        """Получение пользователей и названия чата."""
        self.user: User = self.scope["user"]
        self.user1_id: str = self.scope["url_route"]["kwargs"]["user1_id"]
        self.user2_id: str = self.scope["url_route"]["kwargs"]["user2_id"]
        self.chat_room_name: str = f"chat_{self.user1_id}_{self.user2_id}"
        self.room_group_name: str = "chat_%s" % self.chat_room_name
        self.seller: User = await sync_to_async(User.objects.get)(id=self.user1_id)
        self.buyer: User = await sync_to_async(User.objects.get)(id=self.user2_id)
        # получение объекта чата и добавление в группу
        self.chat_room: ChatRoom = await sync_to_async(ChatRoom.objects.get)(
            seller=self.seller, buyer=self.buyer
        )

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Удаление пользователя из группы и сброс непрочитанных сообщений."""

        await database_sync_to_async(self.chat_room.clean_unread_messages_count)(
            self.user
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data: str):
        """Обработка получения сообщения."""
        # декодирование полученного текстового сообщения
        text_data_json: dict = json.loads(text_data)
        message: str = text_data_json["message"]
        now: timezone = timezone.now()
        # получение объекта чата и создание нового сообщения
        chat_room: ChatRoom = await sync_to_async(ChatRoom.objects.get)(
            seller=self.seller, buyer=self.buyer
        )

        chat_message: ChatMessage = ChatMessage(
            chat_room=self.chat_room, user=self.user, message=message
        )
        # сохранение сообщения и обновление счетчика непрочитанных сообщений
        await database_sync_to_async(chat_message.save)()
        await database_sync_to_async(self.chat_room.update_unread_messages_count)(
            self.user
        )

        # отправка сообщения в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
            },
        )

    async def chat_message(self, event):
        """Отправка сообщения в WebSocket."""
        await self.send(text_data=json.dumps(event))
    
    
