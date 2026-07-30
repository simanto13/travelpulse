from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    OPENAI_MODEL:str="gpt-5"
    DATABASE_URL:str=""
    WEATHER_SERVICE_URL:str="http://weather-service:8000"
    MCP_SERVER_URL:str="http://weather-mcp:3000"
    MCP_TIMEOUT: float = 30.0
    MCP_RETRY_ATTEMPTS: int = 5

    class Config:
        env_file=".env"
settings=Settings()
