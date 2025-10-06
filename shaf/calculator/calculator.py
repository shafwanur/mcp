from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("calculator")


@mcp.tool()
async def add_numbers(a: float, b: float) -> str:
    """Add two numbers using the FastAPI Calculator endpoint.

    Args:
        a: First number
        b: Second number
    """
    url = "https://fastapi-calculadora.onrender.com/calculo-basico/sumar/"
    params = {"num1": a, "num2": b}  # <-- Korrekt: keine ? oder & nötig

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            result = data.get("resultado")
            return f"Simon says that {a} + {b} = {result}, yes."
        except Exception as e:
            return f"Error calling FastAPI Calculator: {e}"


if __name__ == "__main__":
    # Start the server using stdio transport
    print("Running calculator server ...")
    mcp.run(transport="stdio")
