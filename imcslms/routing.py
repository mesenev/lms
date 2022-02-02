from channels.routing import ProtocolTypeRouter, URLRouter
from wsnotifications.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})
