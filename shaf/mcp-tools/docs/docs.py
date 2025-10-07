import os
import json
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from fastapi import FastAPI

load_dotenv()

mcp = FastMCP("docs", stateless_http=True, host="0.0.0.0", port=3333)

USER_AGENT = "docs-app/1.0"
SERPER_URL = "https://google.serper.dev/search"

docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
}


async def search_web(query: str) -> dict | None:
    payload = json.dumps({"q": query, "num": 2})  # returns the top 2 results

    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}


async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout error"


@mcp.tool()  # Q: what does this decorator do?; A: the decorator turns the function into an actual tool compatible with the MCP protocol.
async def get_docs(query: str, library: str):
    # Q: is this docstring important? A: YES! This docstring is crucial for the LLM to überhaupt understand what the function does and what it can use. Heißt, it should also be somewhat be prompt-engineering-mäßig optimized.
    """
    Search the latest docs for a given query and library.
    Supports langchain, openai, and llama-index.

    Args:
        query: The query to search for (e.g. "Chroma DB")
        library: The library to search in (e.g. "langchain")

    Returns:
        Text from the docs
    """

    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported by this tool")

    query = f"site:{docs_urls[library]} {query}"

    results = await search_web(query)
    if len(results["organic"]) == 0:
        return "No results found"

    text = ""
    for result in results["organic"]:
        text += await fetch_url(result["link"])
    return text


app = FastAPI(title="Docs", lifespan=lambda app: mcp.session_manager.run())
app.mount("/docs", mcp.streamable_http_app())

if __name__ == "__main__":
    print("Running docs server ...")
    mcp.run(transport="streamable-http")


# Read: https://heeki.medium.com/building-an-mcp-server-as-an-api-developer-cfc162d06a83, with the exception that it needs to listen on 0.0.0.0 to allow communication within the docker network
