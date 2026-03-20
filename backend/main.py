from twisted.web import server, resource
from twisted.internet import reactor
from backend.resources.clients import ClientResource
from backend.resources.operators import OperatorResource
from backend.redis_cache.redis_server import connect_redis
import os
from autobahn.twisted.resource import WebSocketResource
from autobahn.twisted.websocket import WebSocketServerFactory
from backend.websocket.ws import QueueWSProtocol

if os.getenv("DEBUG") == "1":
    import debugpy
    print("DEBUG ATIVO")
    debugpy.listen(("0.0.0.0", 5678))
    print("ESPERANDO DEBUGGER")
    debugpy.wait_for_client()
    print("DEBUG CONECTADO")

connect_redis()

from backend.resources.state import StateResource
from backend.resources.call_control import AcceptResource, RejectResource

root = resource.Resource()
root.putChild(b"clients", ClientResource())
root.putChild(b"operators", OperatorResource())
root.putChild(b"state", StateResource())
root.putChild(b"accept", AcceptResource())
root.putChild(b"reject", RejectResource())

ws_factory = WebSocketServerFactory("ws://localhost:8000/ws")
ws_factory.protocol = QueueWSProtocol
root.putChild(b"ws", WebSocketResource(ws_factory))

site = server.Site(root)

reactor.listenTCP(8000, site)

reactor.run()