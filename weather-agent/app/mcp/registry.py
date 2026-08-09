class MCPRegistry:
    def __init__(self, session):
        self.session = session
        self.tools = {}

    async def refresh(self):
        if not self.session.client_session:
            raise RuntimeError("MCP session is not initialized")

        result = await self.session.client_session.list_tools()
        self.tools = {tool.name: tool for tool in result.tools}
        return self.tools

    def get(self, name):
        return self.tools.get(name)
