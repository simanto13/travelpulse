import logging
from typing import Optional

from .config import MCPConfig
from .transport import MCPTransport
from .session import MCPSession
from .registry import MCPRegistry
from .executor import MCPExecutor

logger = logging.getLogger(__name__)

class MCPManager:
    def __init__(self, config: MCPConfig | None = None):
        self.config = config or MCPConfig()
        self.transport = MCPTransport(self.config)
        self.session = MCPSession(self.transport)
        self.registry = MCPRegistry(self.session)
        self.executor = MCPExecutor(self.session, self.registry)
        self._running = False

    async def start(self):
        """
        Start the session and register the incoming message handler so the transport
        receive loop will call back into handle_message for each message.
        """
        await self.session.initialize(message_callback=self.handle_message)
        await self.registry.refresh()
        self._running = True
        logger.info("MCPManager started and connected to %s", self.config.server_url)

    async def stop(self):
        self._running = False
        await self.session.shutdown()
        logger.info("MCPManager stopped")

    async def handle_message(self, msg: dict):
        """
        Basic inbound message handler.
        Expected minimal message form (adjust to MCP docs):
          { "type": "invoke_tool", "tool": "tool_name", "arguments": {...}, "id": "<msg-id>" }

        On invoke_tool: calls executor.execute and posts a tool_result back to MCP.
        """
        try:
            logger.debug("MCPManager received message: %s", msg)
            msg_type = msg.get("type")
            if msg_type == "invoke_tool":
                tool_name = msg.get("tool")
                args = msg.get("arguments", {})
                msg_id = msg.get("id")
                logger.info("Invoking tool %s (msg_id=%s)", tool_name, msg_id)
                result = await self.executor.execute(tool_name, args)
                # Build result envelope per MCP expectations (adjust as needed)
                payload = {
                    "type": "tool_result",
                    "id": msg_id,
                    "tool": tool_name,
                    "result": result,
                }
                try:
                    await self.transport.send(payload)
                    logger.info("Sent tool_result for msg_id=%s", msg_id)
                except Exception:
                    logger.exception("Failed to send tool_result for msg_id=%s", msg_id)
            elif msg_type == "ping" or msg_type == "heartbeat":
                # Simple heartbeat handling (you can expand)
                logger.debug("Received %s from MCP", msg_type)
            else:
                logger.debug("Unhandled MCP message type: %s", msg_type)
        except Exception:
            logger.exception("Error while handling MCP message")

    @property
    def connected(self) -> bool:
        # Transport manages its own _running flag; expose simple connected state
        return getattr(self.transport, "_running", False) and self.session.initialized