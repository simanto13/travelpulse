"""
Owns the MCP ClientSession lifecycle.
"""
from typing import Optional, Callable, Awaitable, Any
from .transport import MCPTransport
from mcp.client.session import ClientSession

class MCPSession:
    def __init__(self, transport: MCPTransport):
        self.transport = transport
        self.client_session: Optional[ClientSession] = None
        self.initialized = False

    async def initialize(self, message_callback: Optional[Callable[[Any], Awaitable[None]]] = None):
        """
        Initialize the MCP session by opening the stdio transport and setting
        up the MCP client session.
        """
        if self.initialized:
            return

        if message_callback is not None:
            self.transport.set_message_handler(message_callback)

        await self.transport.open()
        self.client_session = self.transport.client_session
        self.initialized = True

    async def shutdown(self):
        await self.transport.close()
        self.client_session = None
        self.initialized = False