from pydantic import BaseModel

class MCPConfig(BaseModel):
    command: str = "node"
    args: list[str] = []
    timeout: float = 30.0
