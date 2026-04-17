import sys
from collections import defaultdict
from tempfile import SpooledTemporaryFile

from asgiref.sync import AsyncToSync, sync_to_async


class WsgiToAsgi:
    """
    Wraps a WSGI application to make it into an ASGI application.
    """

    def __init__(self, wsgi_application, duplicate_header_limit=100):
        self.wsgi_application = wsgi_application
        self.duplicate_header_limit = duplicate_header_limit

    async def __call__(self, scope, receive, send):
        """
        ASGI application instantiation point.
        We return a new WsgiToAsgiInstance here with the WSGI app
        and the scope, ready to respond when it is __call__ed.
        """
        await WsgiToAsgiInstance(self.wsgi_application, self.duplicate_header_limit)(
            scope, receive, send
        )


class WsgiToAsgiInstance:
    """
    Per-socket instance of a wrapped WSGI application
    """

    def __init__(self, wsgi_application, duplicate_header_limit=100):
        self.wsgi_application = wsgi_application
        self.duplicate_header_limit = duplicate_header_limit
        self.response_started = False
        self.response_content_length = None

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            raise ValueError("WSGI wrapper received a non-HTTP scope")
        self.scope = scope
        with SpooledTemporaryFile(max_size=65536) as body:
            # Alright, wait for the http.request messages
            while True:
                message = await receive()
                if message["type"] != "http.request":
                    raise ValueError("WSGI wrapper received a non-HTTP-request message")
                body.write(message.get("body", b""))
                if not message.get("more_body"):
                    break
            body.seek(0)
            # Wrap send so it can be called from the subthread
            self.sync_send = AsyncToSync(send)
            # Call the WSGI app
            await self.run_wsgi_app(body)

    def build_environ(self, scope, body):
        """
        Builds a scope and request body into a WSGI environ object.
        """
        pass

    def start_response(self, status, response_headers, exc_info=None):
        """
        WSGI start_response callable.
        """
        pass

    @sync_to_async
    def run_wsgi_app(self, body):
        """
        Called in a subthread to run the WSGI app. We encapsulate like
        this so that the start_response callable is called in the same thread.
        """
        pass
