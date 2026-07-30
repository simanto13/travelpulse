class MCPRegistry:
    def __init__(self, session):
        self.session=session
        self.tools={}

    async def refresh(self):
        """
        TODO:
        tools = await self.session.client_session.list_tools()
        self.tools = {t.name:t for t in tools}
        """
        return self.tools

    def get(self,name):
        return self.tools.get(name)
