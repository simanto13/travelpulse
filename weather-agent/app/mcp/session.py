"""
Owns the MCP ClientSession lifecycle.
"""
from typing import Optional, Callable, Awaitable
from .transport import MCPTransport

class MCPSession:
    def __init__(self, transport: MCPTransport):
        self.transport = transport
        self.client_session = None
        self.initialized = False
        self._message_callback: Optional[Callable[[dict], Awaitable[None]]] = None

    async def initialize(self, message_callback: Optional[Callable[[dict], Awaitable[None]]] = None):
        """
        Initialize the session and start the transport receive loop using the
        provided message_callback to handle incoming messages.
        """
        if self.initialized:
            return
        await self.transport.open()
        if message_callback:
            self._message_callback = message_callback
            # start receive loop which creates a background task inside transport
            self.transport.start_receive(self._message_callback)
        self.initialized = True

    async def shutdown(self):
        # stop receive loop then close transport
        self.transport.stop_receive()
        await self.transport.close()
        self.initialized = False