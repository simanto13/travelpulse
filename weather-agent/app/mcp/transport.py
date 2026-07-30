"""
Transport wrapper.

Replace the placeholder implementation below with the official MCP SDK
Streamable HTTP transport, e.g. streamablehttp_client(...), when wiring
to the deployed Weather MCP server.
"""
import httpx
from .config import MCPConfig

class MCPTransport:
    def __init__(self, config:MCPConfig):
        self.config=config
        self.client=httpx.AsyncClient(timeout=config.timeout)

    async def open(self):
        return self.client

    async def close(self):
        await self.client.aclose()
