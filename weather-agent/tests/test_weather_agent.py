import pytest

from app.core.dependencies import (
    initialize_weather_agent,
    shutdown_weather_agent,
)


@pytest.mark.anyio
async def test_current_weather():

    print("\n[1] Starting agent initialization...", flush=True)

    agent = await initialize_weather_agent()

    print("[2] Agent initialized successfully", flush=True)

    try:

        print("[3] Sending prompt to agent...", flush=True)

        response = await agent.chat(
            "What will be the weather in Chennai tomorrow?"
        )

        print("[4] Agent returned a response", flush=True)

        assert response
        assert isinstance(response, str)

        print("\n" + "=" * 70)
        print("AGENT RESPONSE")
        print("=" * 70)
        print(response)
        print("=" * 70)

    finally:

        print("[5] Shutting down agent...", flush=True)

        await shutdown_weather_agent()

        print("[6] Agent shutdown complete", flush=True)