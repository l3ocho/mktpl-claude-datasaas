# MCP Server Patterns Skill

Standard patterns for building Python MCP servers compatible with Claude Code.

## Directory Structure

```
mcp-servers/<name>/
├── mcp_server/
│   ├── __init__.py           # Package marker
│   ├── config.py             # Configuration loader
│   ├── server.py             # Entry point (MCP server setup)
│   └── tools/
│       ├── __init__.py       # Tool registration
│       └── <category>.py     # Tool implementations grouped by domain
├── tests/
│   ├── __init__.py
│   └── test_tools.py
├── requirements.txt
└── README.md
```

## FastMCP Pattern (Recommended)

The FastMCP decorator pattern provides the simplest server implementation:

```python
# server.py
from mcp.server.fastmcp import FastMCP
from .config import load_config

mcp = FastMCP("server-name")
config = load_config()

# Import tools to register them
from .tools import category  # noqa: F401

if __name__ == "__main__":
    mcp.run()
```

```python
# tools/category.py
from ..server import mcp, config

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result for {param}"
```

## Configuration Loader Pattern

```python
# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

def load_config() -> dict:
    # System-level config
    sys_config = Path.home() / ".config" / "claude" / "<name>.env"
    if sys_config.exists():
        load_dotenv(sys_config)

    # Project-level overrides
    project_env = Path.cwd() / ".env"
    if project_env.exists():
        load_dotenv(project_env, override=True)

    config = {
        "api_url": os.getenv("<NAME>_API_URL"),
        "api_token": os.getenv("<NAME>_API_TOKEN"),
    }

    # Validate required
    missing = [k for k, v in config.items() if v is None]
    if missing:
        raise ValueError(f"Missing config: {', '.join(missing)}")

    return config
```

## Entry Point Configuration

In `.mcp.json`:

```json
{
  "mcpServers": {
    "<name>": {
      "command": "mcp-servers/<name>/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "mcp-servers/<name>"
    }
  }
}
```

The `-m` flag runs the module as a script, using `__main__.py` or the `if __name__ == "__main__"` block.

## Requirements

Minimum dependencies for an MCP server:

```
mcp>=1.0.0
python-dotenv>=1.0.0
```

For HTTP-based integrations add:
```
httpx>=0.24.0
```

## Testing Pattern

```python
# tests/test_tools.py
import pytest
from mcp_server.tools.category import my_tool

def test_my_tool():
    result = my_tool("test")
    assert "test" in result
```

## Startup Logging

Always log initialization status to stderr:

```python
import sys

def log(msg):
    print(msg, file=sys.stderr)

log(f"MCP Server '{name}' initialized: {len(tools)} tools registered")
```
