from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI

# Initialize FastMCP server
mcp = FastMCP("calculator", stateless_http=True, host="0.0.0.0", port=6969)


@mcp.tool()
async def add_numbers(a: float, b: float) -> str:
    """Add two numbers using the FastAPI Calculator endpoint.

    Args:
        a: First number
        b: Second number
    """
    url = "https://fastapi-calculadora.onrender.com/calculo-basico/sumar/"
    params = {"num1": a, "num2": b}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            result = data.get("resultado")
            return f"{a} + {b} = {result}"
        except Exception as e:
            return f"Error calling FastAPI Calculator: {e}"


app = FastAPI(title="Calculator", lifespan=lambda app: mcp.session_manager.run())
app.mount("/calculator", mcp.streamable_http_app())

if __name__ == "__main__":
    print("Running calculator server ...")
    mcp.run(transport="streamable-http")


# Read: https://heeki.medium.com/building-an-mcp-server-as-an-api-developer-cfc162d06a83, with the exception that it needs to listen on 0.0.0.0 to allow communication within the docker network
