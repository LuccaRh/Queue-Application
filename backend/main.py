from twisted.web import server, resource
from twisted.internet import reactor
from backend.resources.clients import ClientResource
from backend.resources.operators import OperatorResource
from backend.redis_cache.redis_server import connect_redis
import os

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

site = server.Site(root)

reactor.listenTCP(8000, site)

reactor.run()