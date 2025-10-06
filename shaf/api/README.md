### Example Request Body 

Feel free to add / remove tools depending on your local environment and see how it changes the behavior.  

```json
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
```