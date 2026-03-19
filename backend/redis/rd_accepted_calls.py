from redis_server import r

def create_accepted_call(client_id, operator_id):
    call_id = r.incr("accepted_call:id")
    
    r.rpush("list:accepted_calls", call_id)

    r.hset(f"accepted:{call_id}", mapping={
        "operator_id": operator_id,
        "client_id": client_id
    })

    r.hset(f"client:{client_id}", mapping={
        "status": "on-call"
    })

    r.hset(f"operator:{operator_id}", mapping={
        "status": "on-call",
        "accepted_call_id": call_id
    })

def find_accepted_call_for_operator(operator_id):
    return r.get(f"operator:{operator_id}:accepted_call_id")