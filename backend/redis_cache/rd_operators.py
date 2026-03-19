from backend.redis_cache.redis_server import r
from backend.redis_cache.queue_logic import match_call

#operator status: available, ringing, on-call

def add_operator(operator_id, name):
    r.hset(f"operator:{operator_id}", mapping={
        "id": operator_id,
        "name": name,
        "status": "available",
        "ringing_call_id": "",
        "accepted_call_id": ""
    })
    r.rpush("queue:operators", operator_id)
    match_call()