import httpx
class WeatherServiceClient:
    def __init__(self,base_url:str):
        self.client=httpx.AsyncClient(base_url=base_url)
    async def current_weather(self,city:str):
        r=await self.client.get("/weather/current",params={"city":city})
        r.raise_for_status()
        return r.json()
