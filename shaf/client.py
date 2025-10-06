import os
import asyncio

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


async def test():
    mcp_server_config = {
        "mcpServers": {
            "docs": {  # runs locally.
                "command": "uv",
                "args": [
                    "--directory",
                    f"{os.getcwd()}\\docs",
                    "run",
                    "docs.py",
                ],
            },
            "calculator": {  # runs inside a docker container
                "command": "docker",
                "args": ["run", "--rm", "-i", "calculator-mcp-server"],
            },
            "http": {  # stellt alle MCP Tools aus dem Docker Katalog auf einmal zur Verfügung.
                "url": "http://localhost:8080/mcp"
            },  # for this to work, run this first: docker mcp gateway run --transport streaming --port 8080
        }
    }

    client = MCPClient.from_dict(mcp_server_config)

    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    # TODO: why is fetch_content disabled, what is it?
    agent = MCPAgent(
        llm=llm,
        client=client,
        disallowed_tools=[],
        use_server_manager=False,
        max_steps=30,
    )

    result = await agent.run(
        """
    Führe bitte folgende Schritte aus:
    1. add two numbers, 33 and 22.
    2. on duckduckgo, find what the capital of chile is, and how big it is. 
    """
    )

    print("Result: ", result)


if __name__ == "__main__":
    # Run the appropriate example
    asyncio.run(test())
