"""
MCP Server entry point for Gitea integration.

Provides Gitea tools to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import GiteaConfig
from .gitea_client import GiteaClient
from .tools.issues import IssueTools
from .tools.labels import LabelTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GiteaMCPServer:
    """MCP Server for Gitea integration"""

    def __init__(self):
        self.server = Server("gitea-mcp")
        self.config = None
        self.client = None
        self.issue_tools = None
        self.label_tools = None

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
            self.issue_tools = IssueTools(self.client)
            self.label_tools = LabelTools(self.client)

            logger.info(f"Gitea MCP Server initialized in {self.config['mode']} mode")
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise

    def setup_tools(self):
        """Register all available tools with the MCP server"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            return [
                Tool(
                    name="list_issues",
                    description="List issues from Gitea repository",
                    inputSchema={
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
                                "items": {"type": "string"},
                                "description": "Filter by labels"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name (for PMO mode)"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_issue",
                    description="Get specific issue details",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "issue_number": {
                                "type": "integer",
                                "description": "Issue number"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name (for PMO mode)"
                            }
                        },
                        "required": ["issue_number"]
                    }
                ),
                Tool(
                    name="create_issue",
                    description="Create a new issue in Gitea",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Issue title"
                            },
                            "body": {
                                "type": "string",
                                "description": "Issue description"
                            },
                            "labels": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of label names"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name (for PMO mode)"
                            }
                        },
                        "required": ["title", "body"]
                    }
                ),
                Tool(
                    name="update_issue",
                    description="Update existing issue",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "issue_number": {
                                "type": "integer",
                                "description": "Issue number"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title"
                            },
                            "body": {
                                "type": "string",
                                "description": "New body"
                            },
                            "state": {
                                "type": "string",
                                "enum": ["open", "closed"],
                                "description": "New state"
                            },
                            "labels": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "New labels"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name (for PMO mode)"
                            }
                        },
                        "required": ["issue_number"]
                    }
                ),
                Tool(
                    name="add_comment",
                    description="Add comment to issue",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "issue_number": {
                                "type": "integer",
                                "description": "Issue number"
                            },
                            "comment": {
                                "type": "string",
                                "description": "Comment text"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name (for PMO mode)"
                            }
                        },
                        "required": ["issue_number", "comment"]
                    }
                ),
                Tool(
                    name="get_labels",
                    description="Get all available labels (org + repo)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo": {
                                "type": "string",
                                "description": "Repository name (for PMO mode)"
                            }
                        }
                    }
                ),
                Tool(
                    name="suggest_labels",
                    description="Analyze context and suggest appropriate labels",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "context": {
                                "type": "string",
                                "description": "Issue title + description or sprint context"
                            }
                        },
                        "required": ["context"]
                    }
                ),
                Tool(
                    name="aggregate_issues",
                    description="Fetch issues across all repositories (PMO mode)",
                    inputSchema={
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
                                "items": {"type": "string"},
                                "description": "Filter by labels"
                            }
                        }
                    }
                )
            ]

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
            try:
                # Route to appropriate tool handler
                if name == "list_issues":
                    result = await self.issue_tools.list_issues(**arguments)
                elif name == "get_issue":
                    result = await self.issue_tools.get_issue(**arguments)
                elif name == "create_issue":
                    result = await self.issue_tools.create_issue(**arguments)
                elif name == "update_issue":
                    result = await self.issue_tools.update_issue(**arguments)
                elif name == "add_comment":
                    result = await self.issue_tools.add_comment(**arguments)
                elif name == "get_labels":
                    result = await self.label_tools.get_labels(**arguments)
                elif name == "suggest_labels":
                    result = await self.label_tools.suggest_labels(**arguments)
                elif name == "aggregate_issues":
                    result = await self.issue_tools.aggregate_issues(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]

            except Exception as e:
                logger.error(f"Tool {name} failed: {e}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
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
    server = GiteaMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
