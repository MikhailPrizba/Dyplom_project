from django.urls import path
from . import views


app_name = 'chat'


urlpatterns = [
    path('room/<int:user1_id>/<int:user2_id>/', views.chat,
         name='chat_room'),
]