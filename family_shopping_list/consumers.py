from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ShoppingConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # All clients join this group
        self.group_name = "shopping_list_updates"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # This removes the current channel from the shopping_list_updates group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        list_item_id = data['list_item_id']
        bought = data['bought']
        cancelled = data['cancelled']
        user = data['user']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'list_item_update',
                'list_item_id': list_item_id,
                'bought': bought,
                'cancelled': cancelled,
                'user': user
            }
        )

    async def list_item_update(self, event):
        await self.send(text_data=json.dumps({
            'list_item_id': event['list_item_id'],
            'bought': event['bought'],
            'cancelled': event['cancelled'],
            'user': event['user']
        }))
