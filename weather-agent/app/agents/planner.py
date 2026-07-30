from pydantic import BaseModel
class WeatherPlan(BaseModel):
    intent:str
    location:str|None=None
    date:str|None=None
class Planner:
    def __init__(self,llm):
        self.llm=llm
    async def plan(self,question:str)->WeatherPlan:
        # TODO: call Responses API with structured output
        return WeatherPlan(intent="CURRENT")
