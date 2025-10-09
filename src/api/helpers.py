import os

from fastapi import HTTPException
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient

from .models import MCPAgentConfig, MCPServerConfig, QueryRequest


load_dotenv()


async def process_agent_query(request: QueryRequest) -> str:
    """
    This function contains the core business logic for running the MCPAgent.
    """
    # Configuration Setup with Defaults
    final_server_config = request.mcp_server_config or MCPServerConfig()
    final_agent_config = request.agent_config or MCPAgentConfig(
        max_steps=30, use_server_manager=False
    )

    # Initialize necessary components
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY and not request.api_key:
        raise HTTPException(
            status_code=500,
            detail="An Anthropic API KEY was not passed!",
        )

    if request.api_key is not None:
        ANTHROPIC_API_KEY = request.api_key

    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514"
    )  # TODO: hardcoded. wobei, keine Ahnung auf welche Modelle ich grad Zugriff hab mit meinem Abo.

    # Initialize MCPClient from the (default or provided) server config
    client = MCPClient.from_dict(final_server_config.model_dump())

    # Initialize MCPAgent
    agent_kwargs = final_agent_config.model_dump(exclude_none=True)
    agent = MCPAgent(llm=llm, client=client, **agent_kwargs)

    # Run the Agent
    response = await agent.run(request.query)
    return response[0]["text"]
