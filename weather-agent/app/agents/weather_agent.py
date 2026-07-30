class WeatherAgent:
    def __init__(self,planner,orchestrator):
        self.planner=planner
        self.orchestrator=orchestrator
    async def chat(self,question:str,conversation=None):
        plan=await self.planner.plan(question)
        return await self.orchestrator.chat(question,conversation)
