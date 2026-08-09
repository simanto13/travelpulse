import asyncio
from app.agents.weather_agent import WeatherAgent
from app.clients.llm_client import LLMClient
from app.mcp.config import MCPConfig
from app.mcp.executor import MCPExecutor
from app.mcp.registry import MCPRegistry
from app.mcp.session import MCPSession
from app.mcp.transport import MCPTransport
from app.services.weather_orchestrator import WeatherOrchestrator


class WeatherAgentContainer:
    """
    Owns the lifecycle of the Weather Agent and its dependencies.
    """

    def __init__(self):
        self.transport: MCPTransport | None = None
        self.session: MCPSession | None = None
        self.registry: MCPRegistry | None = None
        self.executor: MCPExecutor | None = None
        self.llm: LLMClient | None = None
        self.orchestrator: WeatherOrchestrator | None = None
        self.agent: WeatherAgent | None = None

    async def initialize(self) -> WeatherAgent:

        print("[INIT 1] Creating MCP configuration", flush=True)

        config = MCPConfig()

        print(
            f"[INIT 2] MCP command: {config.command}",
            flush=True,
        )
        print(
            f"[INIT 3] MCP args: {config.args}",
            flush=True,
        )

        print("[INIT 4] Creating MCP transport", flush=True)

        self.transport = MCPTransport(config)

        print("[INIT 5] Creating MCP session", flush=True)

        self.session = MCPSession(
            transport=self.transport
        )

        print(
            "[INIT 6] Starting MCP session...",
            flush=True,
        )

        await asyncio.wait_for(
            self.session.initialize(),
            timeout=30,
        )

        print(
            "[INIT 7] MCP session initialized",
            flush=True,
        )

        if self.session.client_session is None:
            raise RuntimeError(
                "MCP ClientSession was not initialized"
            )

        print(
            "[INIT 8] Creating MCP registry",
            flush=True,
        )

        self.registry = MCPRegistry(
            self.session.client_session
        )

        print(
            "[INIT 9] Discovering MCP tools...",
            flush=True,
        )

        await asyncio.wait_for(
            self.registry.refresh(),
            timeout=30,
        )

        print(
            f"[INIT 10] Discovered {len(self.registry.tools)} MCP tools",
            flush=True,
        )

        self.executor = MCPExecutor(
            self.session,
            self.registry,
        )

        print(
            "[INIT 11] Creating OpenAI client",
            flush=True,
        )

        self.llm = LLMClient()

        print(
            "[INIT 12] Creating orchestrator",
            flush=True,
        )

        self.orchestrator = WeatherOrchestrator(
            llm=self.llm,
            registry=self.registry,
            executor=self.executor,
        )

        print(
            "[INIT 13] Creating WeatherAgent",
            flush=True,
        )

        self.agent = WeatherAgent(
            orchestrator=self.orchestrator
        )

        print(
            "[INIT 14] WeatherAgent ready",
            flush=True,
        )

        return self.agent

    async def shutdown(self):

        if self.session is not None:
            await self.session.shutdown()

        self.agent = None
        self.orchestrator = None
        self.llm = None
        self.executor = None
        self.registry = None
        self.session = None
        self.transport = None


_container: WeatherAgentContainer | None = None


async def initialize_weather_agent() -> WeatherAgent:
    """
    Initialize and return the singleton WeatherAgent.
    """

    global _container

    if _container is None:

        _container = WeatherAgentContainer()

        return await _container.initialize()

    if _container.agent is None:

        return await _container.initialize()

    return _container.agent


async def shutdown_weather_agent():
    """
    Shutdown the WeatherAgent and MCP server.
    """

    global _container

    if _container is not None:

        await _container.shutdown()

        _container = None