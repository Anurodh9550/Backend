import json

from channels.generic.websocket import AsyncWebsocketConsumer


class HealthConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {"type": "connection", "message": "WebSocket connected successfully"}
            )
        )

    async def receive(self, text_data=None, bytes_data=None):
        payload = {"type": "echo", "message": text_data or ""}
        await self.send(text_data=json.dumps(payload))
