from backend.redis_cache.redis_server import r
from backend.redis_cache.queue_logic import match_call

# client status: waiting, ringing, on-call

def add_client(client_id, name):
    r.hset(f"client:{client_id}", mapping={
        "id": client_id,
        "name": name,
        "status": "waiting"
    })

    r.rpush("queue:clients", client_id)

    match_call()
