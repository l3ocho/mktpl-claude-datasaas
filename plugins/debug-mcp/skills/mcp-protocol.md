# MCP Protocol Skill

Model Context Protocol (MCP) specification reference for debugging and development.

## Protocol Overview

MCP uses JSON-RPC 2.0 over stdio (standard input/output) for communication between Claude Code and MCP servers.

### Transport Types

| Transport | Description | Use Case |
|-----------|-------------|----------|
| **stdio** | JSON-RPC over stdin/stdout | Default for Claude Code |
| **SSE** | Server-Sent Events over HTTP | Remote servers |

## Tool Definitions

Tools are the primary way MCP servers expose functionality.

### Tool Registration

```python
@mcp.tool()
def list_issues(state: str = "open", labels: list[str] = None) -> str:
    """List issues from the repository.

    Args:
        state: Issue state filter (open, closed, all)
        labels: Filter by label names
    """
    # implementation
```

### Tool Schema (JSON)

```json
{
  "name": "list_issues",
  "description": "List issues from the repository",
  "inputSchema": {
    "type": "object",
    "properties": {
      "state": {
        "type": "string",
        "enum": ["open", "closed", "all"],
        "default": "open",
        "description": "Issue state filter"
      },
      "labels": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Filter by label names"
      }
    },
    "required": []
  }
}
```

## Resource Definitions

Resources expose data that can be read by the client.

```python
@mcp.resource("config://settings")
def get_settings() -> str:
    """Return current configuration."""
    return json.dumps(config)
```

## Prompt Definitions

Prompts provide reusable prompt templates.

```python
@mcp.prompt()
def analyze_issue(issue_number: int) -> str:
    """Generate a prompt to analyze a specific issue."""
    return f"Analyze issue #{issue_number} and suggest solutions."
```

## JSON-RPC Message Format

### Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_issues",
    "arguments": {"state": "open"}
  }
}
```

### Response (Success)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{"type": "text", "text": "..."}]
  }
}
```

### Response (Error)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error (invalid JSON) |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
