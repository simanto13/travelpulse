"""
Transport wrapper.

Replace the placeholder implementation below with the official MCP SDK
Streamable HTTP transport, e.g. streamablehttp_client(...), when wiring
to the deployed Weather MCP server.
"""
"""
Streamable HTTP transport for Weather MCP.

This implementation uses httpx.AsyncClient to open a streaming HTTP request to the
MCP server and iterates over newline-delimited JSON messages. It implements
connect/open, close, send, and a receive loop that dispatches parsed messages
via a callback. Reconnects use exponential backoff with jitter.

Assumptions (based on @dangahagan/weather-mcp streamable HTTP semantics):
- The MCP server exposes a long-lived HTTP endpoint that yields newline-delimited
  JSON messages (NDJSON) or "/events" style streaming responses.
- Outbound messages are posted to a separate endpoint (e.g. POST /mcp/send) or
  to the same endpoint depending on server API. Here we'll POST to
  {server_url}/outbound to send messages. Adjust if MCP docs differ.
- Authorization uses a Bearer token from env MCP_API_KEY (Authorization header).

Note: update endpoints and exact message formats after confirming the MCP docs.
"""

from __future__ import annotations

import asyncio
import json
import random
import logging
from typing import AsyncIterator, Awaitable, Callable, Optional

import httpx

from .config import MCPConfig
from app.config import settings

logger = logging.getLogger(__name__)


class MCPTransport:
    def __init__(self, config: MCPConfig):
        self.config = config
        # httpx client used for both streaming reads and outgoing posts
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(self.config.timeout))
        self._running = False
        self._receive_task: Optional[asyncio.Task] = None
        self._callback: Optional[Callable[[dict], Awaitable[None]]] = None

    async def open(self):
        # no-op for now; client created in __init__
        logger.info("MCPTransport: open client")

    async def close(self):
        logger.info("MCPTransport: closing")
        self._running = False
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
        await self._client.aclose()

    async def send(self, payload: dict) -> httpx.Response:
        """Send a message to MCP outbound endpoint.

        NOTE: This uses POST {server_url}/outbound. Update if MCP expects a
        different path.
        """
        url = self.config.server_url.rstrip("/") + "/outbound"
        headers = {}
        api_key = getattr(settings, "MCP_API_KEY", None)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        logger.debug("MCPTransport: sending payload to %s: %s", url, payload)
        resp = await self._client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp

    def _parse_stream_lines(self, byte_iter: AsyncIterator[bytes]) -> AsyncIterator[dict]:
        """Async generator that yields parsed JSON objects from a bytes iterator
        that yields chunks from the streaming response.
        """
        async def gen():
            buffer = b""
            async for chunk in byte_iter:
                buffer += chunk
                while True:
                    if b"\n" not in buffer:
                        break
                    line, buffer = buffer.split(b"\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line.decode("utf-8"))
                        yield obj
                    except Exception as exc:  # pragma: no cover - parsing errors
                        logger.exception("Failed to parse MCP stream line: %s", line)
                        continue
            # leftover
            if buffer.strip():
                try:
                    obj = json.loads(buffer.decode("utf-8"))
                    yield obj
                except Exception:
                    logger.exception("Failed to parse trailing MCP buffer")

        return gen()

    async def _stream_response_iter_bytes(self, url: str) -> AsyncIterator[bytes]:
        """Yields bytes chunks from a streaming GET response."""
        headers = {}
        api_key = getattr(settings, "MCP_API_KEY", None)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        async with self._client.stream("GET", url, headers=headers, timeout=self.config.timeout) as resp:
            resp.raise_for_status()
            async for chunk in resp.aiter_bytes():
                yield chunk

    async def _receive_loop(self):
        self._running = True
        url = self.config.server_url
        attempt = 0
        while self._running:
            try:
                logger.info("MCPTransport: opening stream to %s", url)
                byte_iter = self._stream_response_iter_bytes(url)
                async for obj in self._parse_stream_lines(byte_iter):
                    if not self._running:
                        break
                    if self._callback:
                        try:
                            await self._callback(obj)
                        except Exception:
                            logger.exception("Error in MCP message callback")
                # if stream ended normally, reset attempts and reconnect
                attempt = 0
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                logger.info("MCPTransport: receive task cancelled")
                break
            except Exception:
                attempt += 1
                backoff = min(60, (2 ** attempt) + random.random())
                logger.exception("MCPTransport: stream error, reconnecting in %.1fs", backoff)
                await asyncio.sleep(backoff)

    def start_receive(self, callback: Callable[[dict], Awaitable[None]]):
        """Start background receive loop and register callback for incoming messages."""
        if self._receive_task and not self._receive_task.done():
            raise RuntimeError("receive loop already running")
        self._callback = callback
        loop = asyncio.get_event_loop()
        self._receive_task = loop.create_task(self._receive_loop())

    def stop_receive(self):
        self._running = False
        if self._receive_task:
            self._receive_task.cancel()


