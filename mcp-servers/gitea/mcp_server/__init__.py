"""
Gitea MCP Server package.

Provides MCP tools for Gitea integration via JSON-RPC 2.0.

For external consumers (e.g., HTTP transport), use:
    from mcp_server import get_tool_definitions, create_tool_dispatcher, GiteaClient

    # Get tool schemas
    tools = get_tool_definitions()

    # Create dispatcher bound to a client
    client = GiteaClient()
    dispatch = create_tool_dispatcher(client)
    result = await dispatch("list_issues", {"state": "open"})
"""

__version__ = "1.0.0"

from .tool_registry import get_tool_definitions, create_tool_dispatcher
from .gitea_client import GiteaClient
from .config import GiteaConfig

__all__ = [
    "__version__",
    "get_tool_definitions",
    "create_tool_dispatcher",
    "GiteaClient",
    "GiteaConfig",
]
