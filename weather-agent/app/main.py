from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
from app.api.weather_chat import router as weather_router
from app.config import settings
from app.mcp.config import MCPConfig
from app.mcp.manager import MCPManager

logger = logging.getLogger(__name__)

app = FastAPI(title="TravelPulse Weather Agent")
app.include_router(weather_router)


def _parse_mcp_args(raw_args: str) -> list[str]:
    return [segment.strip() for segment in raw_args.split(",") if segment.strip()]


# Create MCPManager using configuration from global settings
mcp_config = MCPConfig(
    command=settings.MCP_COMMAND,
    args=_parse_mcp_args(settings.MCP_ARGS),
    timeout=settings.MCP_TIMEOUT,
)
mcp_manager = MCPManager(config=mcp_config)

@app.on_event("startup")
async def on_startup():
    logger.info("Starting TravelPulse Weather Agent")
    # Start MCP manager (registers receive callback etc.)
    try:
        await mcp_manager.start()
    except Exception:
        logger.exception("Failed to start MCPManager")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down TravelPulse Weather Agent")
    try:
        await mcp_manager.stop()
    except Exception:
        logger.exception("Failed to stop MCPManager cleanly")

@app.get("/")
async def root():
    return {"service": "TravelPulse Weather Agent", "status": "ok"}

@app.get("/mcp/status")
async def mcp_status():
    """
    Returns a simple MCP connectivity status useful for health checks / debugging.
    """
    return {
        "mcp_connected": mcp_manager.connected,
        "mcp_command": settings.MCP_COMMAND,
        "mcp_args": _parse_mcp_args(settings.MCP_ARGS),
    }


class MCPToolRequest(BaseModel):
    tool: str
    arguments: dict = {}


@app.post("/mcp/tool")
async def invoke_mcp_tool(request: MCPToolRequest):
    if not mcp_manager.connected:
        raise HTTPException(status_code=503, detail="MCP manager is not connected")

    try:
        result = await mcp_manager.executor.execute(request.tool, request.arguments)
        return {"tool": request.tool, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))