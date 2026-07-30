from fastapi import FastAPI
import logging
from app.api.weather_chat import router as weather_router
from app.config import settings
from app.mcp.config import MCPConfig
from app.mcp.manager import MCPManager

logger = logging.getLogger(__name__)

app = FastAPI(title="TravelPulse Weather Agent")
app.include_router(weather_router)

# Create MCPManager using configuration from global settings
mcp_config = MCPConfig(server_url=settings.MCP_SERVER_URL, timeout=settings.MCP_TIMEOUT)
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
        "mcp_server_url": settings.MCP_SERVER_URL,
    }