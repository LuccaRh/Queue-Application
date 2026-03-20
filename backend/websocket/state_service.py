from backend.redis_cache.redis_server import r


def get_clients_queue():
    clients_queue = r.lrange("queue:clients", 0, -1) or []
    
    clients_data = []
    for client_id in clients_queue:
        client_info = r.hgetall(f"client:{client_id}")
        tried_operators = r.smembers(f"client:{client_id}:tried") or []
        
        clients_data.append({
            "id": client_id,
            "name": client_info.get("name", ""),
            "status": client_info.get("status", ""),
            "tried_operators": list(tried_operators)
        })

    return {
        "clients_queue": clients_data
    }

def get_operators_queue():
    operators_queue = r.lrange("queue:operators", 0, -1) or []
    
    operators_data = []
    for operator_id in operators_queue:
        operator_info = r.hgetall(f"operator:{operator_id}")
        
        operators_data.append({
            "id": operator_id,
            "name": operator_info.get("name", ""),
            "ringing_call_id": operator_info.get("ringing_call_id", ""),
            "accepted_call_id": operator_info.get("accepted_call_id", "")
        })

    return {
        "operators_queue": operators_data
    }

def get_ringing_calls_list():
    ringing_calls_ids = r.lrange("list:ringing_calls", 0, -1) or []
    
    ringing_calls_data = []
    for call_id in ringing_calls_ids:
        call_info = r.hgetall(f"ringing:{call_id}")
        client_id = call_info.get("client_id", "")
        operator_id = call_info.get("operator_id", "")
        
        client_info = r.hgetall(f"client:{client_id}")
        operator_info = r.hgetall(f"operator:{operator_id}")
        
        ringing_calls_data.append({
            "id": call_id,
            "client": {
                "id": client_id,
                "name": client_info.get("name", "")
            },
            "operator": {
                "id": operator_id,
                "name": operator_info.get("name", "")
            }
        })

    return {
        "ringing_calls": ringing_calls_data
    }


def get_accepted_calls_list():
    accepted_calls_ids = r.lrange("list:accepted_calls", 0, -1) or []
    
    accepted_calls_data = []
    for call_id in accepted_calls_ids:
        call_info = r.hgetall(f"accepted:{call_id}")
        client_id = call_info.get("client_id", "")
        operator_id = call_info.get("operator_id", "")
        
        client_info = r.hgetall(f"client:{client_id}")
        operator_info = r.hgetall(f"operator:{operator_id}")
        
        accepted_calls_data.append({
            "id": call_id,
            "client": {
                "id": client_id,
                "name": client_info.get("name", "")
            },
            "operator": {
                "id": operator_id,
                "name": operator_info.get("name", "")
            }
        })

    return {
        "accepted_calls": accepted_calls_data
    }


def get_state():
    state = {}
    state.update(get_clients_queue())
    state.update(get_operators_queue())
    state.update(get_ringing_calls_list())
    state.update(get_accepted_calls_list())
    return state    