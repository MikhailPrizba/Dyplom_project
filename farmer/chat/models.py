"""
Модуль содержит два класса: ChatRoom и ChatMessage.
Оба класса отвечают за моделирование данных, используемых в чат-приложении
"""
from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    """моделирует комнату чата между двумя пользователями"""

    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer_chat_rooms"
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_chat_rooms"
    )
    seller_unread_messages_count = models.PositiveIntegerField(default=0)
    buyer_unread_messages_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.buyer.username}'s chat with {self.seller.username}"

    def update_unread_messages_count(self, user):
        """обновление счетчика непрочитанных сообщений"""
        if self.buyer == user:
            self.seller_unread_messages_count += 1
        elif self.seller == user:
            self.buyer_unread_messages_count += 1
        self.save()

    def clean_unread_messages_count(self, user):
        """сбрасывание счетчика непрочитанных сообщений"""
        if self.seller == user:
            self.seller_unread_messages_count = 0
        elif self.buyer == user:
            self.buyer_unread_messages_count = 0
        self.save()


class ChatMessage(models.Model):
    """моделирует сообщения, отправляемые в чате"""

    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="chat_messages"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer_chat_messages"
    )

    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.buyer.username}'s chat with {self.seller.username}: {self.message}"
        )
