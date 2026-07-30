"""
Owns the MCP ClientSession lifecycle.

TODO: create the official ClientSession using the transport's streams and
call initialize().
"""
from .transport import MCPTransport

class MCPSession:
    def __init__(self, transport:MCPTransport):
        self.transport=transport
        self.client_session=None
        self.initialized=False

    async def initialize(self):
        if self.initialized:
            return
        await self.transport.open()
        self.initialized=True

    async def shutdown(self):
        await self.transport.close()
