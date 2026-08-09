class WeatherAgent:

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    async def chat(
        self,
        message: str,
        conversation=None,
    ):

        return await self.orchestrator.run(
            user_message=message,
            conversation=conversation,
        )