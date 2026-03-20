import json
from backend.websocket.state_service import get_all_states

site_users = set()

def register(ws):
    site_users.add(ws)


def unregister(ws):
    site_users.discard(ws)

def onClose(ws):
    update_all()


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


def update_all():
    state = get_all_states()
    broadcast({"type": "state", "data": state})