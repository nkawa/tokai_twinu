"""
ASGI config for twinu_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import socketio_app.routing  # ルーティングファイルをインポート


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twinu_web.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            socketio_app.routing.websocket_urlpatterns  # WebSocket用のURLルーティング
        )
    ),
})


