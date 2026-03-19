from twisted.web import server
import json
from .base_resource import BaseResource
from .db_conection import dbpool
from ..redis_cache.rd_operators import add_operator

def insert_operator(txn, name):
    txn.execute("INSERT INTO operators (name) VALUES (%s) RETURNING id", (name,))
    return txn.fetchone()[0]

class OperatorResource(BaseResource):
    
    def render_POST(self, request):
        self._set_cors_headers(request)

        data = json.loads(request.content.read())
        name = data.get("name")

        d = dbpool.runInteraction(insert_operator, name)

        def success(operator_id):
            request.setHeader(b"content-type", b"application/json")
            request.write(json.dumps({"status": "ok", "message": "nome nome nome!"}).encode())
            add_operator(operator_id, name)
            request.finish()

        def error(err):
            request.setResponseCode(500)
            request.write(json.dumps({"error": str(err), "message": "erro"}).encode())
            request.finish()

        d.addCallback(success)
        d.addErrback(error)

        return server.NOT_DONE_YET
