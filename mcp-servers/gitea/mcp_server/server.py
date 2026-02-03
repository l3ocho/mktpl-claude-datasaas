"""
MCP Server entry point for Gitea integration.

Provides Gitea tools to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import GiteaConfig
from .gitea_client import GiteaClient
from .tool_registry import get_tool_definitions, create_tool_dispatcher

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class GiteaMCPServer:
    """MCP Server for Gitea integration"""

    def __init__(self):
        self.server = Server("gitea-mcp")
        self.config = None
        self.client = None
        self._dispatcher = None

    async def initialize(self):
        """
        Initialize server and load configuration.

        Raises:
            Exception: If initialization fails
        """
        try:
            config_loader = GiteaConfig()
            self.config = config_loader.load()

            self.client = GiteaClient()
            self._dispatcher = create_tool_dispatcher(self.client)

            logger.info(f"Gitea MCP Server initialized in {self.config['mode']} mode")
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            return get_tool_definitions()

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """
            Handle tool invocation.

            Args:
                name: Tool name
                arguments: Tool arguments

            Returns:
                List of TextContent with results
            """
            return await self._dispatcher(name, arguments)

    async def run(self):
        """Run the MCP server"""
        await self.initialize()
        self.setup_tools()

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = GiteaMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
