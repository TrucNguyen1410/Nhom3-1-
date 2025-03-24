from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from .models import User
from .serializers import UserSerializer  # Thêm dòng này

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbotDB"]
collection = db["users"]

# API lấy danh sách user
def get_users(request):
    users = list(User.objects.all().values("username", "email"))  # Lấy dữ liệu từ Django Model
    return JsonResponse(users, safe=False)

# API thao tác với user
class UserAPI(APIView):
    def get(self, request):
        users = list(collection.find({}, {"_id": 0}))  # Lấy danh sách user từ MongoDB
        return Response(users, status=status.HTTP_200_OK)

class UserAPI(APIView):
    def post(self, request):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                collection.insert_one(serializer.validated_data)  # Thêm user vào MongoDB
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class UserDetailAPI(APIView):
    def get(self, request, email):
        user = collection.find_one({"email": email}, {"_id": 0})
        if user:
            return Response(user, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, email):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            collection.update_one({"email": email}, {"$set": serializer.validated_data})  # Cập nhật toàn bộ user
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, email):
        collection.update_one({"email": email}, {"$set": request.data})  # Cập nhật một phần
        return Response({"message": "User updated"}, status=status.HTTP_200_OK)

    def delete(self, request, email):
        collection.delete_one({"email": email})  # Xóa user
        return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
def add_user_page(request):
    return render(request, "add_user.html")