from backend.redis_cache.redis_server import r
from backend.redis_cache.rd_ringing_calls import create_ringing_call
from backend.redis_cache.rd_ringing_calls import find_client_id_for_ringing_call
from backend.redis_cache.rd_ringing_calls import remove_ringing_call
from backend.redis_cache.rd_accepted_calls import create_accepted_call
from backend.websocket.state_broadcaster import update_all
from backend.redis_cache.rd_hangup_calls import find_operator_id_for_accepted_call
from backend.redis_cache.rd_hangup_calls import remove_accepted_call
from backend.websocket.minichat import broadcast_message

def get_next_operator(client_id):
    operators = r.lrange("queue:operators", 0, -1)
    tried = r.smembers(f"client:{client_id}:tried")

    for op in operators:
        if op not in tried:
            return op

    #if all operators have been tried, return the first one in the queue
    return operators[0] if operators else None

def match_call():
    client_id = r.lindex("queue:clients", 0)
    if client_id: 
        operator_id = get_next_operator(client_id) 
        broadcast_message(f"Call {client_id} received.")
    else: 
        return None

    if not client_id or not operator_id:
        broadcast_message(f"Call {client_id} waiting in queue.") if client_id else None
        return None
    
    broadcast_message(f"Call {client_id} ringing for operator {operator_id}.")

    r.lpop("queue:clients")
    r.lrem("queue:operators", 1, operator_id)

    create_ringing_call(client_id, operator_id)
    update_all()

    return match_call()

def answer_call(operator_id):
    client_id = find_client_id_for_ringing_call(operator_id)
    broadcast_message(f"Call {client_id} accepted by operator {operator_id}")
    create_accepted_call(client_id, operator_id)
    remove_ringing_call(operator_id)
    update_all()

def reject_call(operator_id):
    client_id = find_client_id_for_ringing_call(operator_id)
    r.lpush("queue:clients", client_id)
    r.lpush("queue:operators", operator_id)
    remove_ringing_call(operator_id)
    match_call()
    update_all()

def hangup_call_client(client_id):
    operator_id = find_operator_id_for_accepted_call(client_id)
    #If client is in call
    if operator_id:
        remove_accepted_call(operator_id, client_id)
        r.lpush("queue:operators", operator_id)
        broadcast_message(f"Call {client_id} finished. Operator {operator_id} available.")
        match_call()
    #If client is waiting
    else:
        r.lrem("queue:clients", 0, client_id)
        broadcast_message(f"Call {client_id} missed.")
    update_all()