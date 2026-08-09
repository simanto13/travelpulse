from pydantic import BaseModel
from typing import Any

class MCPToolResult(BaseModel):
    tool:str
    content:Any|None=None
