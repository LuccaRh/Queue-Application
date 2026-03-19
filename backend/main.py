from twisted.web import server, resource
from twisted.internet import reactor
from Resources.clients import ClientResource

from redis import connect_redis
connect_redis()

root = resource.Resource()
root.putChild(b"clients", ClientResource())

site = server.Site(root)

reactor.listenTCP(8000, site)

reactor.run()