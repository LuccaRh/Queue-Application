from backend.redis_cache.redis_server import r
from backend.redis_cache.queue_logic import match_call
from backend.websocket.state_broadcaster import update_all

# client status: waiting, ringing, on-call

def add_client(client_id, name):
    name = name or ""
    r.hset(f"client:{client_id}", mapping={
        "id": client_id,
        "name": name,
        "status": "waiting"
    })

    r.rpush("queue:clients", client_id)

    match_call()
    update_all()
