import asyncio

from app.agents.weather_agent import WeatherAgent


async def main():

    agent = WeatherAgent(...)

    response = await agent.chat(
        "What is the weather forecast for Chennai tomorrow?"
    )

    print("\nAgent:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())