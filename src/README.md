# MCP Multi-Tool Agent

## Introduction

This project demonstrates how to build a multi-tool "AI" agent using the **Multi-Container Protocol (MCP)** with Docker. It's a modular system where each tool (like a calculator or a documentation searcher) runs in its own isolated Docker container as an MCP server. A central FastAPI application manages an agent that can intelligently choose and use these tools to answer complex user queries using the MCP tools at hand.

---
### Prerequisites

- **Docker and Docker Compose**: Make sure you have Docker installed and running. 
- **API Keys**: You will need API keys from the following services. Basic, free-tier keys are sufficient.
    * [**Anthropic**](https://console.anthropic.com/): For the language model.
    * [**Serper**](https://serper.dev/): For the documentation search tool.

---
### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shafwanur/mcp.git
    cd mcp/shaf
    ```

2.  **Add the aforementioned API keys to the `.env` file in the root directory:**
    ```env
    SERPER_API_KEY=""
    ANTHROPIC_API_KEY=""
    ```

3.  **Launch the application:**
    ```bash
    docker compose up --build
    ```

---
### API Reference
**Endpoint:** `POST /api/query`

Once all containers are running, the main API is accessible at **[http://localhost:8000](http://localhost:8000)**. 

You can also view the interactive Swagger UI documentation at **[http://localhost:8000/docs](http://localhost:8000/docs)**.


**Tweaking the Request Body:**

The endpoint accepts a JSON object with a single required field, `query`.

```json
{
  "query": "According to the latest OpenAI documentation, how do I generate text with gpt-5?"
}
```

You can also include optional objects to customize the agent's behavior (`agent_config`) or the tools it connects to (`mcp_server_config`).

**Customizing Agent Behavior**

You can control the agent's internal settings by passing an `agent_config` object. For example, you can give it a specific persona with a `system_prompt`, make its thinking process visible with `verbose`, or limit the number of steps it can take with `max_steps`.

Example: Make the agent verbose and limit it to 3 steps.

```json
{
  "query": "What is the sum of 55 and 45, and then what is the capital of Germany?",
  "agent_config": {
    "verbose": true,
    "max_steps": 3,
    "system_prompt": "You are a helpful and concise assistant."
  }
}
```

**Disabling Tools**

If you want to prevent the agent from using a specific tool for a particular query, you can add its name to the `disallowed_tools` list within `agent_config`.

Example: Ask a question that requires a web search, but forbid the agent from using the get_docs tool.

```json
{
  "query": "According to the latest Langchain documentation, how do I create a model and pass a basic prompt to it?",
  "agent_config": {
    "disallowed_tools": ["get_docs"]
  }
}
```

Here, you won't actually get a response with the latest documentation, as the `get_docs` tool was disallowed. 

**Overriding Tool Server Configuration**

The `mcp_server_config` object allows you to change the endpoints of the tools the agent uses. 

Example: Tell the agent the calculator tool is running on port 9999 instead of the default, or straight up remove the docs tool.

```json
{
  "query": "What is 123 + 456?",
  "mcp_server_config": {
    "mcpServers": {
      "calculator": {
        "url": "http://calculator:9999/mcp"
      },
      /* none of the tools available in docs will be available to the agent. 
      "docs": {
        "url": "http://docs:3333/mcp"
      },
      */
      "http": {
        "url": "http://docker-mcp-toolkit:8080/mcp"
      }
    }
  }
}
```