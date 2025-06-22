import json
from channels.generic.websocket import AsyncWebsocketConsumer
from votes.models import Vote
from asgiref.sync import sync_to_async
from polls.models import Poll, PollOption
from django.db.models import Count

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

    async def receive(self, text_data):
        # parse the incoming message into a Python dictionary
        data= json.loads(text_data)
        user= self.scope['user']  # Get the user from the WebSocket scope
        option_id= data.get('option_id')

        try:
            poll= await sync_to_async(Poll.objects.get)(id= self.poll_id)
            option= await sync_to_async(PollOption.objects.get)(id= option_id, poll=poll)
            # Check if the user has already voted in this poll
            existing_vote= await sync_to_async(
                lambda: Vote.objects.filter(user=user, poll=poll).exists()
            )()
            if existing_vote:
                return await self.send(text_data=json.dumps({
                    'error': 'You have already voted in this poll.'
                }))
            # Save the vote
            await sync_to_async(Vote.objects.create)(user= user, poll=poll, option=option)
            # Increment the vote count for the selected option
            option.number_of_votes += 1
            await sync_to_async(option.save)()

            # Prepare updated vote counts
            updated_counts= await sync_to_async(list)(
                PollOption.objects.filter(poll=poll)
                .annotate(votes_count= Count('votes'))
                .values('id', 'option_text', 'votes_count')
            )
            # Broadcast the vote update to all users watching this poll
            await self.channel_layer.group_send(
                self.room_group_name,  # which Group to broadcast to (e.g., "poll_5")
                {
                    'type': 'send_vote_update',
                    'data': updated_counts,  # send the updated vote counts
                }
            )
        except Exception as e:
            print('Vote error:', e)

        # Broadcast vote to all users watching this poll
        ''' await self.channel_layer.group_send(
            self.room_group_name, # which Group to broadcast to (e.g., "poll_5")
            {
                'type': 'vote_update', # Custom event name → handled by vote_update()
                'option_id': option_id, # send the voted option ID
            }
        )
        '''
    async def send_vote_update(self, event):
        # Send the vote update to this WebSocket client
        await self.send(text_data=json.dumps({
            'results': event['data'],  # The option that was voted for
        }))