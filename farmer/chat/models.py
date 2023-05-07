from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chat_rooms')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_chat_rooms')
    

    def __str__(self):
        return f"{self.buyer.username}'s chat with {self.seller.username}"


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chat_messages')
    
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username}'s chat with {self.seller.username}: {self.message}"
    