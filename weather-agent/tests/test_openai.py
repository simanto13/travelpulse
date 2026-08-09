import pytest

from app.clients.llm_client import LLMClient


@pytest.mark.anyio
async def test_openai_connection():

    client = LLMClient()

    response = await client.create_response(
        input="Say hello to TravelPulse in one sentence."
    )

    assert response.output_text

    print(response.output_text)