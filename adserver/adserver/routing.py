from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.middlewares import DialogueMiddleWare

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': DialogueMiddleWare(
        URLRouter(websocket_urlpatterns)
    )
})