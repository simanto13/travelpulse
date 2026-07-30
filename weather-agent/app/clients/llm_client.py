from openai import AsyncOpenAI
class LLMClient:
    def __init__(self,api_key:str,model:str="gpt-5"):
        self.client=AsyncOpenAI(api_key=api_key)
        self.model=model
    async def generate(self,messages):
        # TODO: call Responses API
        return "Placeholder response"
