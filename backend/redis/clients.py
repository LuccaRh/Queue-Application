from redis_server import r

def add_client(client_id, name):
    r.hset(f"client:{client_id}", mapping={
        "name": name,
        "status": "waiting",
        "tried_operators": []
    })

    r.rpush("queue:clients", client_id)
    match_call()

def set_operator_available(operator_id, name):
    r.hset(f"operator:{operator_id}", mapping={
        "name": name,
        "status": "available",
    })
    r.rpush("queue:operators", operator_id)
    match_call()

def match_call():
    client_id = r.lindex("queue:clients", 0)
    operator_id = r.lindex("queue:operators", 0)

    print(f"Call {client_id} received.")

    if not client_id or not operator_id:
        print(f"Call {client_id} waiting in line") if not client_id else None
        return None
    
    print(f"Call {client_id} ringing for operator {operator_id}.")

    r.lpop("queue:clients")
    r.lpop("queue:operators")

    r.hset(f"client:{client_id}", "status", "ringing")
    r.hset(f"operator:{operator_id}", "status", "ringing")

    r.rpush("calls:ringing", [client_id, operator_id])

    return match_call()

def answer_call(operator_id):
    call = r.lindex("calls:ringing", 0)
    if not call:
        print(f"No calls ringing for operator {operator_id}.")
        return None
    
    client_id, op_id = call
    if op_id != operator_id:
        print(f"Operator {operator_id} is not assigned to this call.")
        return None
    
    print(f"Call {client_id} answered by operator {operator_id}.")

    r.lpop("calls:ringing")

    r.hset(f"client:{client_id}", "status", "in_call")
    r.hset(f"operator:{operator_id}", "status", "in_call")

def reject_call(operator_id):
    call = r.lindex("calls:ringing", 0)
    if not call:
        print(f"No calls ringing for operator {operator_id}.")
        return None
    
    client_id, op_id = call
    if op_id != operator_id:
        print(f"Operator {operator_id} is not assigned to this call.")
        return None
    
    print(f"Call {client_id} rejected by operator {operator_id}.")

    r.lpop("calls:ringing")

    r.hset(f"client:{client_id}", "status", "waiting")
    r.hset(f"operator:{operator_id}", "status", "available")

    r.rpush("queue:clients", client_id)
    r.rpush("queue:operators", operator_id)

    return match_call()

def hangup_call(client_id):
    call = r.lindex("calls:ringing", 0)
    if not call:
        print(f"No calls ringing for client {client_id}.")
        return None
    
    cli_id, operator_id = call
    if cli_id != client_id:
        print(f"Client {client_id} is not assigned to this call.")
        return None
    
    print(f"Call {client_id} hung up.")

    r.lpop("calls:ringing")

    r.hset(f"client:{client_id}", "status", "waiting")
    r.hset(f"operator:{operator_id}", "status", "available")

    r.rpush("queue:clients", client_id)
    r.rpush("queue:operators", operator_id)

    return match_call()
