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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollify.settings')
django.setup()


# Import necessary modules for Channels
from channels.routing import ProtocolTypeRouter, URLRouter
from pollify.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
# Create the ASGI application
application= ProtocolTypeRouter({
    "websocket" : AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
