from openai import AsyncOpenAI

from app.config import settings


class LLMClient:

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key
        )

        self.model = settings.openai_model

    async def create_response(
        self,
        input,
        tools=None,
        instructions=None,
    ):

        return await self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=input,
            tools=tools or [],
        )