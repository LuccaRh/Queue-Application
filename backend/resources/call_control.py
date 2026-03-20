from twisted.web import server
import json
from .base_resource import BaseResource
from backend.redis_cache.queue_logic import answer_call, hangup_call_client, reject_call
from .db_conection import dbpool
from backend.redis_cache.redis_server import r
from datetime import datetime


class AcceptResource(BaseResource):
    def render_POST(self, request):
        self._set_cors_headers(request)
        data = json.loads(request.content.read())
        operator_id = data.get("operator")

        if not operator_id:
            request.setResponseCode(400)
            return json.dumps({"error": "operator is required"}).encode()

        try:
            answer_call(operator_id)
            request.setHeader(b"content-type", b"application/json")
            request.write(json.dumps({"status": "ok", "message": "call accepted"}).encode())
        except Exception as e:
            request.setResponseCode(500)
            request.write(json.dumps({"error": str(e)}).encode())

        request.finish()
        return server.NOT_DONE_YET

class RejectResource(BaseResource):
    def render_POST(self, request):
        self._set_cors_headers(request)
        data = json.loads(request.content.read())
        operator_id = data.get("operator")

        if not operator_id:
            request.setResponseCode(400)
            return json.dumps({"error": "operator is required"}).encode()

        try:
            reject_call(operator_id)
            request.setHeader(b"content-type", b"application/json")
            request.write(json.dumps({"status": "ok", "message": "call rejected"}).encode())
        except Exception as e:
            request.setResponseCode(500)
            request.write(json.dumps({"error": str(e)}).encode())

        request.finish()
        return server.NOT_DONE_YET
    
class HangupClientResource(BaseResource):

    def render_POST(self, request):
        self._set_cors_headers(request)
        data = json.loads(request.content.read())
        client_id = data.get("client")
    
        if not client_id:
            request.setResponseCode(400)
            return json.dumps({"error": "client is required"}).encode()

        try:
            hangup_call_client(client_id)
            request.setHeader(b"content-type", b"application/json")
            request.write(json.dumps({"status": "ok", "message": "call rejected"}).encode())
        except Exception as e:
            request.setResponseCode(500)
            request.write(json.dumps({"error": str(e)}).encode())

        request.finish()
        return server.NOT_DONE_YET

def insert_finished_call(txn, data):   
    txn.execute("INSERT INTO logs (client_id, operator_id, created_at) VALUES (%s, %s, %s)", (data["client_id"], data["operator_id"], data["created_at"],))
    
class HangupOperatorResource(BaseResource):

    def render_POST(self, request):
        self._set_cors_headers(request)
        data = json.loads(request.content.read())
        client_id = data.get("client")
        accepted_call_id = r.hget(f"client:{client_id}", "accepted_call_id")
        operator_id = r.hget(f"accepted:{accepted_call_id}", "operator_id")
        created_at = r.hget(f"accepted:{accepted_call_id}", "created_at")

        call_data = {
            "client_id": int(client_id),
            "operator_id": int(operator_id),
            "created_at": created_at
        }
        d = dbpool.runInteraction(insert_finished_call, call_data)
        
        def success(_):
            request.setHeader(b"content-type", b"application/json")
            request.write(json.dumps({"status": "ok", "message": "log"}).encode())
            hangup_call_client(client_id)
            request.finish()
        def error(err):
            request.setResponseCode(500)
            request.write(json.dumps({"error": str(err), "message": "erro"}).encode())
            request.finish()

        d.addCallback(success)
        d.addErrback(error)

        return server.NOT_DONE_YET