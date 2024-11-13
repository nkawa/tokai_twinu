from django.apps import AppConfig

from channels.generic.websocket import AsyncWebsocketConsume
import json

class SocketioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socketio_app'