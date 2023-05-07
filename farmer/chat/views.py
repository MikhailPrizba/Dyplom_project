from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.models import ChatRoom, ChatMessage


@login_required
def chat(request, user1_id, user2_id):
    user1 = get_object_or_404(User, id=user1_id)
    user2 = get_object_or_404(User, id=user2_id)
    
    chatroom, created = ChatRoom.objects.get_or_create(seller=user1, buyer=user2)
    messages = ChatMessage.objects.filter(chat_room=chatroom.id).order_by('timestamp')
    
 
    return render(request, 'chat/chat.html', {
        'user1': user1,
        'user2': user2,
        'messages': messages,
    })
    


@login_required
def chat_rooms(request, user1_id):
    user1 = get_object_or_404(User, id=user1_id)
    if user1.groups.filter(name='Sellers').exists():
        chatrooms = ChatRoom.objects.filter(seller=user1)
    else:
        chatrooms = ChatRoom.objects.filter(buyer=user1)
    return render(request, 'chat/rooms.html', {
        'user1': user1,
        'chatrooms': chatrooms,
    })
    
