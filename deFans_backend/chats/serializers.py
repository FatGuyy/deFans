from rest_framework import serializers
from .models import Chat, ChatMessage

class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        # Here, creator is the content creator, not the creator of the chat
        # Both Creator or account user can make create a chat, given their subscription
        fields = ['creator', 'account']

class ChatMessageSerializer(serializers.ModelSerializer):
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = ChatMessage
        fields = ['chat', 'sender', 'receiver', 'content']