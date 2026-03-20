from .base_resource import BaseResource
from backend.websocket.state_service import get_state
import json


class StateResource(BaseResource):
    def render_GET(self, request):
        self._set_cors_headers(request)
        request.setHeader(b"content-type", b"application/json")
        return json.dumps(get_state()).encode("utf-8")
