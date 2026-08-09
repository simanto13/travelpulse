import asyncio
from typing import Any


class MCPRegistry:
    """Discovers and caches tools exposed by the MCP server."""

    def __init__(self, session):
        self.session = session
        self.tools: dict[str, Any] = {}

    async def refresh(self) -> dict[str, Any]:

        response = await asyncio.wait_for(
            self.session.list_tools(),
            timeout=30,
        )

        self.tools = {
            tool.name: tool
            for tool in response.tools
        }

        return self.tools

    def get(self, name: str) -> Any | None:
        """Return an MCP tool by name."""
        return self.tools.get(name)

    def get_all(self) -> list[Any]:
        """Return all discovered MCP tools."""
        return list(self.tools.values())

    def get_openai_tools(self) -> list[dict[str, Any]]:
        """
        Convert MCP tool definitions into OpenAI function tools.

        The MCP server remains the source of truth for the
        tool name, description, and input schema.
        """

        openai_tools = []

        for tool in self.tools.values():

            openai_tools.append(
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema,
                }
            )

        return openai_tools