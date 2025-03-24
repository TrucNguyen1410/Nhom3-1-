from django.db import models

# Create your models here.
from django.conf import settings
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(settings.MONGO_URI)
db = client["chatbotDB"]
chat_collection = db["chat_history"]

class ChatHistory:
    """Mô hình lưu lịch sử chat"""
    
    @staticmethod
    def save_chat(user_id, chat_id, user_message, bot_response):
        chat_data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response
        }
        chat_collection.insert_one(chat_data)

    @staticmethod
    def get_chats(user_id):
        """Lấy danh sách các cuộc hội thoại của user"""
        return list(chat_collection.find({"user_id": user_id}).distinct("chat_id"))

    @staticmethod
    def get_chat_detail(chat_id):
        """Lấy chi tiết cuộc hội thoại"""
        return list(chat_collection.find({"chat_id": chat_id}))
