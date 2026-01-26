"""
MCP Server entry point for viz-platform integration.

Provides Dash Mantine Components validation, charting, layout, theming, and page tools
to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import VizPlatformConfig

# Suppress noisy MCP validation warnings on stderr
logging.basicConfig(level=logging.INFO)
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class VizPlatformMCPServer:
    """MCP Server for visualization platform integration"""

    def __init__(self):
        self.server = Server("viz-platform-mcp")
        self.config = None
        # Tool handlers will be added in subsequent issues
        # self.dmc_tools = None
        # self.chart_tools = None
        # self.layout_tools = None
        # self.theme_tools = None
        # self.page_tools = None

    async def initialize(self):
        """Initialize server and load configuration."""
        try:
            config_loader = VizPlatformConfig()
            self.config = config_loader.load()

            # Log available capabilities
            caps = []
            if self.config.get('dmc_available'):
                caps.append(f"DMC {self.config.get('dmc_version')}")
            else:
                caps.append("DMC (not installed)")

            logger.info(f"viz-platform MCP Server initialized with: {', '.join(caps)}")

        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            tools = []

            # DMC validation tools (Issue #172)
            # - list_components
            # - get_component_props
            # - validate_component

            # Chart tools (Issue #173)
            # - chart_create
            # - chart_configure_interaction

            # Layout tools (Issue #174)
            # - layout_create
            # - layout_add_filter
            # - layout_set_grid

            # Theme tools (Issue #175)
            # - theme_create
            # - theme_extend
            # - theme_validate
            # - theme_export_css

            # Page tools (Issue #176)
            # - page_create
            # - page_add_navbar
            # - page_set_auth

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool invocation."""
            try:
                # Tool routing will be added as tools are implemented
                # DMC tools
                # if name == "list_components":
                #     result = await self.dmc_tools.list_components(**arguments)
                # ...

                raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Tool {name} failed: {e}")
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]

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
    server = VizPlatformMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
