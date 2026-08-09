from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPConfig(BaseSettings):
    """
    Configuration for the local Weather MCP server.
    """

    command: str = "node"

    args: list[str] = Field(
        default_factory=list
    )

    timeout: float = 30.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MCP_",
        extra="ignore",
    )