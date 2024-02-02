from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .views import maps


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,self.channel_name
        )

        await self.accept()
    

    async def receive(self, text_data):
        event_data = json.loads(text_data)
        #print(event_data)
        type = event_data["type"]

        if type=="offer":
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_offer", "message": [event_data["sender"],event_data["offer"],event_data["reciever"]]}
        )
        elif type=="answer":
            
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_answer", "message": [event_data["sender"],event_data["answer"],event_data["reciever"]]}
        )
        elif type=="ice-candidate":
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_candidate", "message": [event_data["sender"],event_data["icecandidates"],event_data["reciever"]]}
        )
        elif type=="Message":

            await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_message", "message": [event_data["sender"],event_data["message"]]}
        )
        elif type=="leave":
            print(maps[0][self.room_name])
            print(event_data['leaver'])
            maps[0][self.room_name].remove(event_data["leaver"])
            await self.channel_layer.group_send(
                self.room_group_name, {"type":"send_leave","message":event_data["leaver"]}
            )
        

        # Send message to room group
      
    # Receive message from room group
    async def send_offer(self, event):
        user = event["message"][0]
        message = event["message"][1]
        reciever = event["message"][2]
        print(f"Offer Sent by {user} to {reciever}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "sender":user,
            "type":"offer",
            "offer":message,
            "reciever":reciever
        }))

    
    async def send_answer(self, event):
        user = event["message"][0]
        message = event["message"][1]
        reciever = event["message"][2]

        print(f"Sending offer from {user} to {reciever}")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "sender":user,
            "type":"answer",
            "answer":message,
            "reciever":reciever
        }))

    
    async def send_candidate(self, event):
        user = event["message"][0]
        message = event["message"][1]
        reciever = event["message"][2]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "sender":user,
            "type":"ice-candidate",
            "icecandidates":message,
            "reciever":reciever
        }))

    async def send_message(self, event):
        sender = event["message"][0]
        message = event["message"][1]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type":"Message","message": message,"sender":sender}))

    async def send_leave(self,event):
        leaver = event["message"]
        print(f"{leaver} left the room")
        await self.send(text_data=json.dumps({"type":"leave","leaver":leaver}))
    
   