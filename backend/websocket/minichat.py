from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import json
from backend.websocket.state_broadcaster import site_users

class ChatServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        site_users.add(self)
        broadcast_message("Chat conectado!")

    def onClose(self, wasClean, code, reason):
        site_users.discard(self)
        broadcast_message("Chat desconectado!")

def broadcast_message(message):
    print(message)
    payload = json.dumps({"type": "chat", "message": message}).encode("utf-8")
    for c in list(site_users):
        try:
            c.sendMessage(payload)
        except:
            site_users.discard(c)