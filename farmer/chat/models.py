from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chat_rooms')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_chat_rooms')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username}'s chat with {self.seller.username}"
