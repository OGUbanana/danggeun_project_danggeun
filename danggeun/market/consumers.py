import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, ChatMessage
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.load_previous_messages()  # 이전 메시지를 로드하고 전송하는 메서드를 호출

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Save the message to the database
        
        saved_message = await self.save_message(username, message)
        timestamp = saved_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "timestamp": timestamp
            }
        )

    @database_sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        chat_room = ChatRoom.objects.get(room_number=self.room_name)
        return ChatMessage.objects.create(
            chatroom=chat_room,
            author=user,
            content=message
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "timestamp": timestamp
        }))

    @database_sync_to_async
    def load_previous_messages(self):
        chat_room = ChatRoom.objects.get(room_number=self.room_name)
        messages = chat_room.messages.all()
        return [(message.content, message.author.username, message.timestamp.strftime('%Y-%m-%d %H:%M:%S')) for message in messages]

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        previous_messages = await self.load_previous_messages()
        for message_content, username, timestamp in previous_messages:
            await self.send(text_data=json.dumps({
                "message": message_content,
                "username": username,
                "timestamp": timestamp
            }))