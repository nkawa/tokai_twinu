# chat/routing.py
from django.urls import path

#urlpatterns = [
#    path('', views.index, name='index'),
#]


from . import consumers

websocket_urlpatterns = [
    path(r'^socket.io/', consumers.app),
    path('socket.io/', consumers.app),
]