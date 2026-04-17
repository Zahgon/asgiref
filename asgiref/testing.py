import asyncio
import contextvars
import time

from .compatibility import guarantee_single_callable
from .timeout import timeout as async_timeout


class ApplicationCommunicator:
    """
    Runs an ASGI application in a test mode, allowing sending of
    messages to it and retrieval of messages it sends.
    """

    def __init__(self, application, scope):
        self._future = None
        self.application = guarantee_single_callable(application)
        self.scope = scope
        self._input_queue = None
        self._output_queue = None

    # For Python 3.9 we need to lazily bind the queues, on 3.10+ they bind the
    # event loop lazily.
    @property
    def input_queue(self):
        pass

    @property
    def output_queue(self):
        pass

    @property
    def future(self):
        pass

    async def wait(self, timeout=1):
        """
        Waits for the application to stop itself and returns any exceptions.
        """
        pass

    def stop(self, exceptions=True):
        pass

    def __del__(self):
        # Clean up on deletion
        try:
            self.stop(exceptions=False)
        except RuntimeError:
            # Event loop already stopped
            pass

    async def send_input(self, message):
        """
        Sends a single message to the application
        """
        pass

    async def receive_output(self, timeout=1):
        """
        Receives a single message from the application, with optional timeout.
        """
        pass

    async def receive_nothing(self, timeout=0.1, interval=0.01):
        """
        Checks that there is no message to receive in the given time.
        """
        pass
