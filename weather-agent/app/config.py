from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    OPENAI_API_KEY:str=""
    OPENAI_MODEL:str="gpt-5"
    DATABASE_URL:str=""
    WEATHER_SERVICE_URL:str="http://weather-service:8000"
    MCP_SERVER_URL:str="http://weather-mcp:3000"
    class Config:
        env_file=".env"
settings=Settings()
