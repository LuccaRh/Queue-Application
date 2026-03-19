from redis_server import r

def create_ringing_call(client_id, operator_id):
    r.hset(f"client:{client_id}", "status", "ringing")
    r.hset(f"operator:{operator_id}", "status", "ringing")

    r.sadd(f"client:{client_id}:tried", operator_id)
    
    r.hset(f"client:{client_id}:tried", mapping={operator_id: True})
    call_id = r.incr("ringing_call:id")
    
    r.rpush("list:ringing_calls", call_id)

    r.hset(f"ringing:{call_id}", mapping={
        "operator_id": operator_id,
        "client_id": client_id
    })

    r.hset(f"operator:{operator_id}", mapping={
        "ringing_call_id": call_id
    })


def find_client_id_for_ringing_call(operator_id):
    ringing_call_id = r.get(f"operator:{operator_id}:ringing_call_id")
    return r.get(f"ringing:{ringing_call_id}:client_id")


def remove_ringing_call(operator_id):
    call_id = r.get(f"operator:{operator_id}:ringing_call_id")

    r.lrem("list:ringing_calls", 0, call_id)
    r.delete(f"ringing-{call_id}")

    r.hset(f"operator:{operator_id}", mapping={
        "ringing_call_id": None
    })
