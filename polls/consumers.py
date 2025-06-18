import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PollVoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the poll_id from the URL (e.g., /ws/polls/5/)
        self.poll_id= self.scope['url_route']['kwargs']['poll_id']
        # Define a unique group name for this poll
        self.room_group_name= f"poll_{self.poll_id}"

        # Add this WebSocket connection to the group (room)
        await self.channel_layer.group_add(
            self.room_group_name, # Group name (e.g., "poll_5")
            self.channel_name  # Channel name (unique identifier for this WebSocket connection)
        )
        await self.accept() # Accept the WebSocket connection

    async def disconnect(self, close_code):
        # Remove this WebSocket connection from the group (room)
        await self.channel_layer.group_discard(
            self.room_group_name, # Group name (e.g., "poll_5")
            self.channel_name  # Channel name (unique identifier for this WebSocket connection)
        )

    async def recieve(self, text_data):
        # parse the incoming message into a Python dictionary
        data= json.loads(text_data)
        option_id= data['option_id']  # Get which option the user voted for 

        # In real-world: save vote in DB here

        # Broadcast vote to all users watching this poll
        await self.channel_layer.group_send(
            self.room_group_name, # which Group to broadcast to (e.g., "poll_5")
            {
                'type': 'vote_update', # Custom event name → handled by vote_update()
                'option_id': option_id, # send the voted option ID
            }
        )

    async def vote_update(self, event):
        # Send the vote update to this WebSocket client
        await self.send(text_data=json.dumps({
            'option_id': event['option_id'],  # The option that was voted for
        }))