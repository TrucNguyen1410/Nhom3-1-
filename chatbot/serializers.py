from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    chat_id = serializers.CharField()
    user_message = serializers.CharField()
    bot_response = serializers.CharField()
