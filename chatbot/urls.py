from django.urls import path
from .views import chat, get_chats, chat_detail

urlpatterns = [
    path("chat/", chat, name="chat"),  # Gửi tin nhắn
    path("chats/", get_chats, name="get_chats"),  # Lấy danh sách chat
    path("chats/<str:chat_id>/", chat_detail, name="chat_detail"),  # GET/PATCH/DELETE theo chat_id
]
