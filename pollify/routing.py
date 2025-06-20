from django.urls import path, include
from polls.consumers import PollVoteConsumer

websocket_urlpatterns = [
    path('ws/polls/<int:poll_id>/', PollVoteConsumer.as_asgi()),
]