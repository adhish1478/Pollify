"""
ASGI config for pollify project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollify.settings")
django.setup()


# Import necessary modules for Channels
import polls.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from polls.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
# Create the ASGI application
application= ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests
    "websocket" : AuthMiddlewareStack(
        URLRouter(polls.routing.websocket_urlpatterns)
    ),
})
