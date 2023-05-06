from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.models import ChatRoom

@login_required
def chat(request, user1_id, user2_id):
    user1 = get_object_or_404(User, id=user1_id)
    user2 = get_object_or_404(User, id=user2_id)
    
    return render(request, 'chat/chat.html', {
        'user1': user1,
        'user2': user2,

    })
