from backend.redis_cache.redis_server import r

def find_operator_id_for_accepted_call(client_id):
    accepted_call_id = r.hget(f"client:{client_id}", "accepted_call_id")
    return r.hget(f"accepted:{accepted_call_id}", "operator_id")

def remove_accepted_call(operator_id, client_id):
    call_id = r.hget(f"operator:{operator_id}", "accepted_call_id")

    r.lrem("list:accepted_calls", 0, call_id)
    r.delete(f"accepted:{call_id}")

    r.hdel(f"operator:{operator_id}", "accepted_call_id")
    r.delete(f"client:{client_id}")
    r.delete(f"client:{client_id}:tried")