from django.urls import path
from .consumers import NotificationsConsumer

websockets = [
    path("/ws/notifications", NotificationsConsumer.as_asgi(), name="ws-notifications"),
]
