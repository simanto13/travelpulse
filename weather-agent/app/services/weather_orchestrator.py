import json
from typing import Any

from app.agents.prompts import SYSTEM_PROMPT


class WeatherOrchestrator:
    """
    Coordinates OpenAI and the Weather MCP server.
    """

    MAX_TOOL_ROUNDS = 5

    def __init__(
        self,
        llm,
        registry,
        executor,
    ):
        self.llm = llm
        self.registry = registry
        self.executor = executor

    async def run(
        self,
        user_message: str,
        conversation: list[dict[str, Any]] | None = None,
    ) -> str:

        # Discover MCP tools if required.
        if not self.registry.tools:
            await self.registry.refresh()

        tools = self.registry.get_openai_tools()

        input_items: list[Any] = []

        if conversation:
            input_items.extend(conversation)

        input_items.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = await self.llm.create_response(
            input=input_items,
            tools=tools,
            instructions=SYSTEM_PROMPT,
        )

        for _ in range(self.MAX_TOOL_ROUNDS):

            function_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not function_calls:
                return response.output_text

            tool_outputs = []

            for call in function_calls:

                try:
                    arguments = json.loads(
                        call.arguments
                    )

                except json.JSONDecodeError as exc:

                    raise ValueError(
                        f"Invalid arguments returned by "
                        f"model for tool '{call.name}': "
                        f"{call.arguments}"
                    ) from exc

                result = await self.executor.execute(
                    call.name,
                    arguments,
                )

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                )

            # Keep the model's previous output in the
            # conversation before supplying tool results.
            input_items.extend(response.output)

            input_items.extend(tool_outputs)

            response = await self.llm.create_response(
                input=input_items,
                tools=tools,
                instructions=SYSTEM_PROMPT,
            )

        raise RuntimeError(
            "Maximum MCP tool execution rounds exceeded"
        )