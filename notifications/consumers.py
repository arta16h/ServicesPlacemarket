import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f"notifications_{self.user_id}"

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # دریافت پیام از کلاینت (اختیاری)
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message': f"پیام شما دریافت شد: {data}"
        }))

    async def send_notification(self, event):
        # ارسال نوتیف به کلاینت
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
