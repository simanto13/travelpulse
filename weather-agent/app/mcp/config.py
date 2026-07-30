from pydantic import BaseModel

class MCPConfig(BaseModel):
    server_url: str = "http://weather-mcp:3000/mcp"
    timeout: float = 30.0
