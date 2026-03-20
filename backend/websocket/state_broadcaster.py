import json
from backend.websocket.state_service import get_clients_queue
from backend.websocket.state_service import get_operators_queue
from backend.websocket.state_service import get_ringing_calls_list
from backend.websocket.state_service import get_accepted_calls_list

site_users = set()


def register(ws):
    site_users.add(ws)


def unregister(ws):
    site_users.discard(ws)


def broadcast(message):
    payload = json.dumps(message)
    dead = []

    for single_site_user in list(site_users):
        try:
            single_site_user.sendMessage(payload.encode("utf-8"))
        except Exception:
            dead.append(single_site_user)

    for single_site_user in dead:
        site_users.discard(single_site_user)


def update_clients_queue():
    state = get_clients_queue()
    broadcast({"type": "state", "data": state})

def update_operators_queue():
    state = get_operators_queue()
    broadcast({"type": "state", "data": state})

def update_ringing_calls():
    state = get_ringing_calls_list()
    broadcast({"type": "state", "data": state})

def update_accepted_calls():
    state = get_accepted_calls_list()
    broadcast({"type": "state", "data": state})

def update_all():
    update_clients_queue()
    update_operators_queue()
    update_ringing_calls()
    update_accepted_calls()