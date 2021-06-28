import json
from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer

class NotifyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('connect')
        await self.channel_layer.group_add('notify',self.channel_name)
        await self.accept()
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard('notify',self.channel_name)
    
    async def send_data(self,event):
        new_data = event.get('text')
        await self.send(json.dumps(new_data))

  