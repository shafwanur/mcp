import os
import dotenv 
import asyncio

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

async def test():
    mcp_server_config = {
    "mcpServers": {
        "docs": { # this one runs locally. 
        "command": "C:\\Users\\kazirahman\\.local\\bin\\uv",
        "args": [
            "--directory",
            "C:\\Users\\kazirahman\\Documents\\mcp-research-noah\\shaf",
            "run",
            "docs.py"
        ]
        },
        "calculator": { # TODO: change to run inside a docker container. 
        "command": "C:\\Users\\kazirahman\\.local\\bin\\uv",
        "args": [
            "--directory",
            "C:\\Users\\kazirahman\\Documents\\mcp-research-noah\\shaf",
            "run",
            "calculator.py"
        ]
        }
    }
    }

    client = MCPClient.from_dict(mcp_server_config)

    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    # TODO: why is fetch_content disabled, what is it? 
    agent = MCPAgent(llm=llm, client=client, disallowed_tools=["fetch_content"], use_server_manager=False, max_steps=30)

    result = await agent.run(
            """
    Führe bitte folgende Schritte aus:
    1. add two numbers, 33 and 22.

    """
    )

if __name__ == "__main__":
    # Run the appropriate example
    asyncio.run(test())