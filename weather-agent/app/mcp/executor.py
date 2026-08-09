from .exceptions import MCPToolError

class MCPExecutor:
    def __init__(self, session, registry):
        self.session = session
        self.registry = registry

    async def execute(self, tool_name: str, arguments: dict):
        if not self.session.client_session:
            raise MCPToolError("MCP session is not initialized")

        if tool_name not in self.registry.tools:
            await self.registry.refresh()

        if tool_name not in self.registry.tools:
            raise MCPToolError(f"Unknown tool: {tool_name}")

        result = await self.session.client_session.call_tool(tool_name, arguments)
        if hasattr(result, "model_dump"):
            return result.model_dump(mode="json", exclude_none=True)
        return result
