"""
Данный модуль содержит список URL-шаблонов для WebSocket соединений.
используется регулярное выражение для создания динамических URL-адресов, 
которые могут содержать идентификаторы пользователей user1_id и user2_id.
"""

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<user1_id>\d+)/(?P<user2_id>\d+)/$",
        consumers.ChatConsumer.as_asgi(),
    ),
]
