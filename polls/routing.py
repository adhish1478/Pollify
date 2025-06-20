from django.urls import re_path, include
from .consumers import PollVoteConsumer

websocket_urlpatterns = [
    re_path(r'ws/polls/(?P<poll_id>\d+)/$', PollVoteConsumer.as_asgi()),
]