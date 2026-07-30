from .config import MCPConfig
from .transport import MCPTransport
from .session import MCPSession
from .registry import MCPRegistry
from .executor import MCPExecutor

class MCPManager:
    def __init__(self, config:MCPConfig|None=None):
        self.config=config or MCPConfig()
        self.transport=MCPTransport(self.config)
        self.session=MCPSession(self.transport)
        self.registry=MCPRegistry(self.session)
        self.executor=MCPExecutor(self.session,self.registry)

    async def start(self):
        await self.session.initialize()
        await self.registry.refresh()

    async def stop(self):
        await self.session.shutdown()
