from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import the business logic function from your new service file
from .helpers import process_agent_query, MCPServerConfig, MCPAgentConfig

router = APIRouter(prefix="/api", tags=["api"])


# --- Model for the request body ---
# This model now just defines the shape of the incoming JSON.
class QueryRequest(BaseModel):
    """Model for the query request, combining all expected inputs."""
    query: str
    mcp_server_config: Optional[MCPServerConfig] = None
    agent_config: Optional[MCPAgentConfig] = None

    # This example for the docs remains unchanged.
    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "What is the current time in Deggendorf?"
            }
        }
    }


# --- Simplified API Endpoint ---

@router.post("/query")
async def handle_query(request: QueryRequest) -> str:
    """
    Executes a query by delegating to the agent processing service.

    This endpoint is now thin and only handles the HTTP interaction.
    """
    try:
        # Delegate the actual work to the helper function.
        result = await process_agent_query(
            query=request.query,
            agent_config=request.agent_config,
            server_config=request.mcp_server_config,
        )
        return result
    except HTTPException as e:
        # Re-raise known HTTP exceptions from the service layer.
        raise e
    except Exception as e:
        # Catch any other unexpected errors and return a generic 500 error.
        print(f"An unexpected error occurred: {e}") # Optional: for logging
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

"""
example Request Body: 
{
  "query": "Add 2 and 5 together and tell me the answer. Later, let me know what the temperature in Deggendorf is.",
  "mcp_server_config": {
    "mcpServers": {
      "docs": {
        "command": "uv",
        "args": [
          "--directory",
          "C:\\Users\\kazirahman\\Documents\\mcp-research-noah\\shaf\\mcp-tools\\docs",
          "run",
          "docs.py"
        ]
      },
      "calculator": {
        "command": "docker",
        "args": [
          "run",
          "--rm",
          "-i",
          "calculator-mcp-server"
        ]
      }
    }
  }
}
"""