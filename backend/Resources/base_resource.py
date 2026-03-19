from twisted.web.resource import Resource

class BaseResource(Resource):
    isLeaf = True

    def _set_cors_headers(self, request):
        request.setHeader(b"Access-Control-Allow-Origin", b"*")
        request.setHeader(b"Access-Control-Allow-Methods", b"GET, POST, OPTIONS")
        request.setHeader(b"Access-Control-Allow-Headers", b"Content-Type")

    def render_OPTIONS(self, request):
        self._set_cors_headers(request)
        request.setResponseCode(200)
        return b""