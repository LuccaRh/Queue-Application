from redis_server import r
from queue_logic import match_call

#operator status: available, ringing, on-call

def set_operator_available(operator_id, name):
    r.hset(f"operator:{operator_id}", mapping={
        "id": operator_id,
        "name": name,
        "status": "available",
        "ringing_call_id": None,
        "accepted_call_id": None
    })
    r.rpush("queue:operators", operator_id)
    match_call()