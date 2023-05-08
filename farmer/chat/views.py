from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import ChatMessage, ChatRoom


@login_required
def chat(request: HttpRequest, user1_id: int, user2_id: int) -> HttpResponse:
    # получаем объекты пользователей или возвращаем 404 ошибку, если не существуют
    user1 = get_object_or_404(User, id=user1_id)
    user2 = get_object_or_404(User, id=user2_id)
    # получаем объект чат-комнаты или создаем новый, если не существует
    chatroom, created = ChatRoom.objects.get_or_create(seller=user1, buyer=user2)
    # получаем сообщения чата, относящиеся к данной комнате и сортируем по времени
    messages = ChatMessage.objects.filter(chat_room=chatroom.id).order_by("timestamp")

    return render(
        request,
        "chat/chat.html",
        {
            "user1": user1,
            "user2": user2,
            "messages": messages,
        },
    )


@login_required
def chat_rooms(request: HttpRequest, user1_id: int) -> HttpResponse:
    # получаем объект пользователя или возвращаем 404 ошибку, если не существует
    user1 = get_object_or_404(User, id=user1_id)
    # получаем чат-комнаты, в которых участвует данный пользователь в качестве продавца или покупателя
    if user1.groups.filter(name="Sellers").exists():
        chatrooms = ChatRoom.objects.filter(seller=user1)
    else:
        chatrooms = ChatRoom.objects.filter(buyer=user1)

    return render(
        request,
        "chat/rooms.html",
        {
            "user1": user1,
            "chatrooms": chatrooms,
        },
    )
