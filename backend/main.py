from twisted.web import server, resource
from twisted.internet import reactor
from twisted.enterprise import adbapi
import json
import os

# 🔹 conexão DB
dbpool = adbapi.ConnectionPool(
    "psycopg2",
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "db"),
    port=int(os.getenv("POSTGRES_PORT", 5432))
)

def insert_user(txn, name):
    txn.execute("INSERT INTO clients (name) VALUES (%s)", (name,))

class ClientResource(resource.Resource):
    isLeaf = True

    def _set_cors_headers(self, request):
        request.setHeader(b"Access-Control-Allow-Origin", b"*")
        request.setHeader(b"Access-Control-Allow-Methods", b"GET, POST, OPTIONS")
        request.setHeader(b"Access-Control-Allow-Headers", b"Content-Type")

    def render_OPTIONS(self, request):

        self._set_cors_headers(request)
        request.setResponseCode(200)
        return b""
    
    def render_POST(self, request):
        self._set_cors_headers(request)

        data = json.loads(request.content.read())
        name = data.get("name")

        d = dbpool.runInteraction(insert_user, name)

        def success(_):
            request.setHeader(b"content-type", b"application/json")
            request.write(json.dumps({"status": "ok"}).encode())
            request.finish()

        def error(err):
            request.setResponseCode(500)
            request.write(json.dumps({"error": str(err)}).encode())
            request.finish()

        d.addCallback(success)
        d.addErrback(error)

        return server.NOT_DONE_YET

# 🔹 servidor HTTP
root = resource.Resource()
root.putChild(b"clients", ClientResource())

site = server.Site(root)

reactor.listenTCP(8000, site)
print("API rodando em http://localhost:8000")

reactor.run()