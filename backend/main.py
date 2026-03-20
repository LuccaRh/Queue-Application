from twisted.web import server, resource
from twisted.internet import reactor
from backend.resources.clients import ClientResource
from backend.resources.operators import OperatorResource
from backend.redis_cache.redis_server import connect_redis
import os
from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from backend.websocket.ws import QueueWSProtocol
from backend.websocket.minichat import ChatServerProtocol
from backend.resources.call_control import HangupClientResource, HangupOperatorResource
from backend.resources.call_control import AcceptResource, RejectResource

if os.getenv("DEBUG") == "1":
    import debugpy
    print("DEBUG ATIVO")
    debugpy.listen(("0.0.0.0", 5678))
    print("ESPERANDO DEBUGGER")
    debugpy.wait_for_client()
    print("DEBUG CONECTADO")

connect_redis()


root = resource.Resource()
root.putChild(b"clients", ClientResource())
root.putChild(b"operators", OperatorResource())
root.putChild(b"accept", AcceptResource())
root.putChild(b"reject", RejectResource())
root.putChild(b"hangup_client", HangupClientResource())
root.putChild(b"hangup_operator", HangupOperatorResource())

ws_factory = WebSocketServerFactory("ws://localhost:8000/ws")
ws_factory.protocol = QueueWSProtocol
root.putChild(b"ws", WebSocketResource(ws_factory))

ws_factory_chat = WebSocketServerFactory("ws://localhost:8000/chat")
ws_factory_chat.protocol = ChatServerProtocol
root.putChild(b"chat", WebSocketResource(ws_factory_chat))

site = server.Site(root)

reactor.listenTCP(8000, site)

reactor.run()