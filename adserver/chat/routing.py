from .consumers import MessageConsumer
from django.urls import path


websocket_urlpatterns = [
    path('ws/dialogue/<int:dialogue_id>', MessageConsumer),
]