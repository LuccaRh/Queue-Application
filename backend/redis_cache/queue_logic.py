from backend.redis_cache.redis_server import r
from backend.redis_cache.rd_ringing_calls import create_ringing_call
from backend.redis_cache.rd_ringing_calls import find_client_id_for_ringing_call
from backend.redis_cache.rd_ringing_calls import remove_ringing_call
from backend.redis_cache.rd_accepted_calls import create_accepted_call
from backend.redis_cache.rd_accepted_calls import find_accepted_call_for_operator

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
    operator_id = get_next_operator(client_id) if client_id else None

    print(f"Call {client_id} received.")

    if not client_id or not operator_id:
        print(f"Call {client_id} waiting in line") if not operator_id else None
        return None
    
    print(f"Call {client_id} ringing for operator {operator_id}.")

    r.lpop("queue:clients")
    r.lpop("queue:operators") 

    create_ringing_call(client_id, operator_id) 

    return match_call()

def answer_call(operator_id):
    client_id = find_client_id_for_ringing_call(operator_id)
    create_accepted_call(client_id, operator_id)
    remove_ringing_call(operator_id)

def reject_call(operator_id):
    client_id = find_client_id_for_ringing_call(operator_id)
    r.lpush("queue:clients", client_id)
    r.lpush("queue:operators", operator_id)
    remove_ringing_call(operator_id)
    match_call()

#def hangup_call(client_id):
