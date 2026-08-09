import asyncio
from dataclasses import dataclass
@dataclass
class WeatherAgentResult:
    answer:str
    weather:dict
    metadata:dict
    sources:list
class WeatherOrchestrator:
    def __init__(self,planner=None,mcp=None,weather_service=None,llm=None):
        self.planner=planner
        self.mcp=mcp
        self.weather_service=weather_service
        self.llm=llm
    async def chat(self,question:str,conversation=None):
        # TODO: invoke planner then execute MCP/weather tasks concurrently.
        return WeatherAgentResult(
            answer="Orchestrator scaffold ready.",
            weather={},
            metadata={"question":question},
            sources=[]
        )
