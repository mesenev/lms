from django.urls import path
from wsnotifications.consumers import NotificationsConsumer

websockets = [
    path("ws/notifications", NotificationsConsumer.as_asgi(), name="ws-notifications"),
]
