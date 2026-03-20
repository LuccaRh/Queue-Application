import json
from autobahn.twisted.websocket import WebSocketServerProtocol
from backend.websocket.state_broadcaster import register, unregister
from backend.websocket.state_service import get_clients_queue

class QueueWSProtocol(WebSocketServerProtocol):
    def onOpen(self):
        register(self)
        self.sendMessage(json.dumps({"type": "state", "data": get_clients_queue()}).encode("utf-8"))

    def onClose(self, wasClean, code, reason):
        unregister(self)

    def onMessage(self, payload, isBinary):
        pass
