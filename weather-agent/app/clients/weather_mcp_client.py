class WeatherMCPClient:
    def __init__(self,manager):
        self.manager=manager
    async def execute(self,tool:str,args:dict):
        return await self.manager.executor.execute(tool,args)
