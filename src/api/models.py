import os
from typing import Any, Dict, Optional, List

from pydantic import BaseModel, Field


class MCPServerConfig(BaseModel):
    """Configuration structure for MCP servers."""

    mcpServers: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            # "docs": {
            #     "command": "uv",
            #     "args": [
            #         "--directory",
            #         f"{os.getcwd()}\\..\\mcp-tools\\docs",
            #         "run",
            #         "docs.py",
            #     ],
            # },
            # "calculator": {
            #     # "command": "docker",
            #     # "args": ["run", "--rm", "-i", "calculator-mcp-server"],
            #     "url": "http://localhost:6969"
            # },
            "calculator": {
                "url": os.environ.get("CALCULATOR_MCP_SERVER", "http://localhost:6969/mcp")
            },
            "docs": {
                "url": os.environ.get("DOCS_MCP_SERVER", "http://localhost:3333/mcp")
            },
            "http": {
                "url": os.environ.get("DOCKER_MCP_GATEWAY_URL", "http://localhost:8080/mcp")
            },
        },
        description="Dictionary defining the MCP server configuration.",
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


class QueryRequest(BaseModel):
    """Model for the query request, combining all expected inputs."""

    query: str
    mcp_server_config: Optional[MCPServerConfig] = None
    agent_config: Optional[MCPAgentConfig] = None
    api_key: Optional[str] = (
        None  # Note: I understand the api_key should probably be passed securely in the header and not in the body, but for this demo example, I'm too lazy to bother with that.
    )

    # The example body shown in swagger.
    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "Answer the following questions: 1. Add 33 and 36 together. 2. Use duckduckgo to find the capital of Chile and its population. 3. Find out how to initialize a chat model using langchain and python."
            }
        }
    }
