"""StdIO MCP transport for the local Weather MCP server."""

from __future__ import annotations

import logging
import os
from typing import Any, Callable, Awaitable, Optional

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.shared.message import SessionMessage

from .config import MCPConfig

logger = logging.getLogger(__name__)


def _parse_args(value: str | None) -> list[str]:
    if not value:
        return []
    return [segment.strip() for segment in value.split(",") if segment.strip()]


def _build_process_env() -> dict[str, str] | None:
    env: dict[str, str] = {}
    for key, value in os.environ.items():
        if key.startswith("MCP_ENV_"):
            env_name = key[len("MCP_ENV_") :]
            env[env_name] = value
    return env or None


class MCPTransport:
    def __init__(self, config: MCPConfig):
        self.config = config
        self._stdio_context = None
        self._client_session: Optional[ClientSession] = None
        self._message_handler: Optional[Callable[[Any], Awaitable[None]]] = None
        self._running = False

    @property
    def client_session(self) -> Optional[ClientSession]:
        return self._client_session

    @property
    def connected(self) -> bool:
        return self._running and self._client_session is not None

    def _server_parameters(self) -> StdioServerParameters:
        if not self.config.command:
            raise RuntimeError(
                "MCP_COMMAND is required for the stdio MCP transport. "
                "Set MCP_COMMAND to `npx` or `node`, then configure MCP_ARGS."
            )

        env = _build_process_env()

        return StdioServerParameters(
            command=self.config.command,
            args=self.config.args,
            env=env,
        )

    async def open(self):
        if self._running:
            return

        server_parameters = self._server_parameters()
        self._stdio_context = stdio_client(server_parameters)
        read_stream, write_stream = await self._stdio_context.__aenter__()

        self._client_session = ClientSession(
            read_stream,
            write_stream,
            message_handler=self._message_handler,
        )
        await self._client_session.__aenter__()

        # Complete the MCP initialization handshake.
        await self._client_session.initialize()

        self._running = True
        logger.info(
            "MCPTransport: started MCP subprocess %s %s",
            server_parameters.command,
            server_parameters.args,
        )

    async def close(self):
        if self._client_session is not None:
            try:
                await self._client_session.__aexit__(None, None, None)
            except Exception:
                logger.exception("Error closing MCP client session")
            finally:
                self._client_session = None

        if self._stdio_context is not None:
            try:
                await self._stdio_context.__aexit__(None, None, None)
            except Exception:
                logger.exception("Error shutting down MCP subprocess context")
            finally:
                self._stdio_context = None

        self._running = False
        logger.info("MCPTransport: closed")

    def set_message_handler(self, callback: Callable[[Any], Awaitable[None]]):
        self._message_handler = callback

    async def send(self, payload: dict) -> None:
        raise RuntimeError(
            "Raw transport send is not supported for stdio MCP clients. "
            "Use MCPExecutor.execute() to call tools through the MCP session."
        )


