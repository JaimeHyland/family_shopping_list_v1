from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ShoppingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.shop_name = self.scope["url_route"]["kwargs"]["shop_name"]
        self.shop_group_name = f"shop_{self.shop_name}"
        await self.channel_layer.group_add(
            self.shop_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.shop_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.shop_group_name, {
                "type": "shop.message",
                "message": message
            }
        )

        # self.send(text_data=json.dumps({"message": message}))

    async def shop_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "message": message
        }))