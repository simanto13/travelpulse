import os
import shutil

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MCP_PATH = (
    r"D:\TravelPulse\travelpulse"
    r"\weather-mcp\dist\index.js"
)


@pytest.mark.anyio
async def test_mcp_connection():

    node = shutil.which("node")

    assert node is not None, (
        "Node.js was not found in PATH"
    )

    server = StdioServerParameters(
        command=node,
        args=[MCP_PATH],
        cwd=os.path.dirname(MCP_PATH),
        env=dict(os.environ),
    )

    async with stdio_client(server) as (read, write):

        async with ClientSession(
            read,
            write,
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            assert len(tools.tools) > 0

            print("\nAvailable MCP tools:")

            for tool in tools.tools:
                print(f"  {tool.name}")