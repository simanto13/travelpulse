from .exceptions import MCPToolError

class MCPExecutor:
    def __init__(self, session, registry):
        self.session=session
        self.registry=registry

    async def execute(self, tool_name:str, arguments:dict):
        if tool_name not in self.registry.tools:
            raise MCPToolError(f"Unknown tool: {tool_name}")
        """
        TODO:
        return await self.session.client_session.call_tool(
            tool_name,
            arguments
        )
        """
        return {"tool":tool_name,"arguments":arguments}
