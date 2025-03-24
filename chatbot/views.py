from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests
from bson.objectid import ObjectId
from pymongo import MongoClient

# Kết nối MongoDB
client = settings.MONGO_CLIENT if hasattr(settings, "MONGO_CLIENT") else MongoClient("mongodb://localhost:27017/")
db = client["chatbotDB"]
collection = db["chat_history"]

# API Key từ settings.py
API_KEY = settings.GEMINI_API_KEY

def call_gemini_api(user_message):
    """Gọi API Gemini và trả về phản hồi của chatbot"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": user_message}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        bot_response = response.json()

        # Trích xuất nội dung phản hồi từ API Gemini
        candidates = bot_response.get("candidates", [])
        if candidates and "content" in candidates[0]:
            reply_parts = candidates[0]["content"].get("parts", [])
            return "\n".join([part.get("text", "") for part in reply_parts if "text" in part])
        return "Không có phản hồi từ AI."

    except requests.exceptions.RequestException as e:
        return f"Lỗi khi gọi API: {str(e)}"

@api_view(["POST"])
@permission_classes([AllowAny])
def chat(request):
    """Nhận tin nhắn, gọi AI và lưu lịch sử"""
    user_message = request.data.get("message")
    chat_id = request.data.get("chat_id", str(ObjectId()))  # Nếu không có, tạo chat_id mới

    if not user_message:
        return Response({"error": "Vui lòng nhập tin nhắn."}, status=400)

    bot_reply = call_gemini_api(user_message)

    # Lưu lịch sử chat vào MongoDB
    chat_data = {
        "chat_id": chat_id,
        "user_message": user_message,
        "bot_response": bot_reply
    }
    collection.insert_one(chat_data)

    return Response({"response": bot_reply, "chat_id": chat_id})

@api_view(["GET"])
@permission_classes([AllowAny])
def get_chats(request):
    """Lấy danh sách các cuộc hội thoại"""
    chats = list(collection.find({}, {"_id": 0}))
    return Response({"chats": chats})

@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def chat_detail(request, chat_id):
    """Lấy, cập nhật hoặc xóa cuộc hội thoại theo chat_id"""
    
    if request.method == "GET":
        # Lấy chi tiết chat
        messages = list(collection.find({"chat_id": chat_id}, {"_id": 0}))
        if not messages:
            return Response({"error": "Không tìm thấy chat này."}, status=404)
        return Response({"chat_id": chat_id, "messages": messages})
    
    elif request.method == "PATCH":
        # Cập nhật tin nhắn
        update_data = {}
        new_user_message = request.data.get("message")
        
        if new_user_message:
            update_data["user_message"] = new_user_message
            update_data["bot_response"] = call_gemini_api(new_user_message)  # Gọi lại AI
        
        if not update_data:
            return Response({"error": "Không có dữ liệu nào để cập nhật."}, status=400)
        
        result = collection.update_one(
            {"chat_id": chat_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return Response({"error": "Không tìm thấy chat hoặc không có thay đổi nào."}, status=404)
        
        return Response({"message": "Cập nhật thành công.", "updated_data": update_data}, status=200)
    
    elif request.method == "DELETE":
        # Xóa cuộc hội thoại
        result = collection.delete_many({"chat_id": chat_id})

        if result.deleted_count == 0:
            return Response({"error": "Không tìm thấy cuộc chat."}, status=404)

        return Response({"message": "Xóa thành công."}, status=200)

@api_view(["GET"])
@permission_classes([AllowAny])
def chat_api(request):
    """API test đơn giản"""
    return JsonResponse({"message": "Hello from chatbot API!"})
