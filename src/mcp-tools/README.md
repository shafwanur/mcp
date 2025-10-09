# Custom MCP Tool Servers

This directory contains individual, containerized tool servers built to be compatible with the **Multi-Container Protocol (MCP)**. Each sub-folder represents a distinct microservice that exposes one or more tools for an MCP agent to use.

These servers are built with `FastAPI` and the `mcp[cli]` library, and they are designed to be run as part of a larger `docker-compose` setup. This collection currently offers **2 distinct tools**.

***
##  Calculator (`/calculator`)

This service provides a simple tool for performing addition.

* **Purpose:** To add two numbers together.
* **Tool Signature:** `add_numbers(a: float, b: float)`
* **Implementation:** The tool makes an external API call to a public FastAPI calculator service to perform the addition.
* **Container Port:** Exposes port `6969`.

***
## Documentation Search (`/docs`)

This service provides a powerful tool for searching the official documentation of popular AI libraries.

* **Purpose:** To find relevant documentation pages for a given query within a specific library.
* **Tool Signature:** `get_docs(query: str, library: str)`
* **Supported Libraries:** `langchain`, `openai`, and `llama-index`.
* **Implementation:** The tool uses the Serper API for a site-specific Google search and then scrapes the content from the top results.
* **Dependencies:** This tool requires a **`SERPER_API_KEY`** environment variable to be set in its environment to function correctly.
* **Container Port:** Exposes port `3333`.

---
### How to Use
Please refer to the `docker-compose.yaml` file and the main `README.md` in the root directory for instructions on how to build and run the entire application stack.