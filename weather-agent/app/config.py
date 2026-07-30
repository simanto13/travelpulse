from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    OPENAI_API_KEY:str="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"
    OPENAI_MODEL:str="gpt-5"
    DATABASE_URL:str=""
    WEATHER_SERVICE_URL:str="http://weather-service:8000"
    MCP_SERVER_URL:str="http://weather-mcp:3000"
    MCP_TIMEOUT: float = 30.0
    MCP_RETRY_ATTEMPTS: int = 5

    class Config:
        env_file=".env"
settings=Settings()
