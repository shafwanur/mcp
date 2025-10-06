# agent_service.py

import os
import json
from typing import Any, Dict, Optional, List

from fastapi import HTTPException
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient

# You'll need to move the Pydantic models here as well, or import them 
# from a central models.py file. For simplicity, we'll redefine them here.
from pydantic import BaseModel, Field

# --- Pydantic Models ---
# It's best practice to move these to their own 'models.py' file
# and import them in both agent_service.py and your router file.

class MCPServerConfig(BaseModel):
    """Configuration structure for MCP servers."""
    mcpServers: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "docs": {
                "command": "uv",
                "args": [
                    "--directory",
                    f"{os.getcwd()}\\mcp-tools\\docs",
                    "run",
                    "docs.py",
                ],
            },
            "calculator": {
                "command": "docker",
                "args": ["run", "--rm", "-i", "calculator-mcp-server"],
            },
            "http": {
                "url": "http://localhost:8080/mcp"
            },
        },
        description="Dictionary defining different MCP server configurations."
    )

class MCPAgentConfig(BaseModel):
    """Configuration structure for the MCPAgent, including its __init__ parameters."""
    max_steps: int = 5
    auto_initialize: bool = False
    memory_enabled: bool = True
    system_prompt: Optional[str] = None
    system_prompt_template: Optional[str] = None
    additional_instructions: Optional[str] = None
    disallowed_tools: List[str] = Field(default_factory=list)
    tools_used_names: Optional[List[str]] = None
    use_server_manager: bool = False
    verbose: bool = False
    agent_id: Optional[str] = None
    base_url: str = "https://cloud.mcp-use.com"
    callbacks: Optional[List[Any]] = None
    chat_id: Optional[str] = None
    retry_on_error: bool = True
    max_retries_per_step: int = 2


# --- Core Business Logic ---

# Load environment variables once
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

async def process_agent_query(
    query: str,
    agent_config: Optional[MCPAgentConfig] = None,
    server_config: Optional[MCPServerConfig] = None
) -> str:
    """
    This function contains the core business logic for running the MCPAgent.
    It's moved from the API endpoint to be more modular and testable.
    """
    # 1. Configuration Setup with Defaults
    final_server_config = server_config or MCPServerConfig()
    final_agent_config = agent_config or MCPAgentConfig(max_steps=30, use_server_manager=False)

    # 2. Initialize necessary components
    
    # Initialize LLM (server-side)
    if not ANTHROPIC_API_KEY:
        # Raise an exception that the API layer can catch and handle.
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY is not set in environment variables.")
    
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    # Initialize MCPClient from the (default or provided) server config
    client = MCPClient.from_dict(final_server_config.model_dump())

    # 3. Initialize MCPAgent
    agent_kwargs = final_agent_config.model_dump(exclude_none=True)
    
    agent = MCPAgent(
        llm=llm,
        client=client,
        **agent_kwargs
    )
    
    # 4. Run the Agent
    response = await agent.run(query)

    # 5. Extract and Return Final Text
    final_output = ""
    if response and isinstance(response, list):
        last_step = response[-1]
        
        if 'text' in last_step and isinstance(last_step['text'], str):
            final_output = last_step['text']
        elif 'final_answer' in last_step and isinstance(last_step['final_answer'], str):
            final_output = last_step['final_answer']
        else:
            final_output = json.dumps(response, indent=2)
    
    return final_output