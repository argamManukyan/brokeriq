"""
ASGI config for brokers project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from core.routing import ws_patterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brokers.settings')

application = ProtocolTypeRouter({

    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(URLRouter(ws_patterns))

})

