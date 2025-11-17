"""
MCP Server entry point for Wiki.js integration.

Provides Wiki.js tools to Claude Code via JSON-RPC 2.0 over stdio.
"""
import asyncio
import logging
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import WikiJSConfig
from .wikijs_client import WikiJSClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikiJSMCPServer:
    """MCP Server for Wiki.js integration"""

    def __init__(self):
        self.server = Server("wikijs-mcp")
        self.config = None
        self.client = None

    async def initialize(self):
        """
        Initialize server and load configuration.

        Raises:
            Exception: If initialization fails
        """
        try:
            config_loader = WikiJSConfig()
            self.config = config_loader.load()

            self.client = WikiJSClient(
                api_url=self.config['api_url'],
                api_token=self.config['api_token'],
                base_path=self.config['base_path'],
                project=self.config.get('project')
            )

            logger.info(f"Wiki.js MCP Server initialized in {self.config['mode']} mode")
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
                    name="search_pages",
                    description="Search Wiki.js pages by keywords and tags",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query string"
                            },
                            "tags": {
                                "type": "string",
                                "description": "Comma-separated tags to filter by (optional)"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "description": "Maximum results to return"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_page",
                    description="Get a specific page by path",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Page path (relative or absolute)"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="create_page",
                    description="Create a new Wiki.js page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Page path relative to project/base"
                            },
                            "title": {
                                "type": "string",
                                "description": "Page title"
                            },
                            "content": {
                                "type": "string",
                                "description": "Page content (markdown)"
                            },
                            "description": {
                                "type": "string",
                                "description": "Page description (optional)"
                            },
                            "tags": {
                                "type": "string",
                                "description": "Comma-separated tags (optional)"
                            },
                            "publish": {
                                "type": "boolean",
                                "default": True,
                                "description": "Publish immediately"
                            }
                        },
                        "required": ["path", "title", "content"]
                    }
                ),
                Tool(
                    name="update_page",
                    description="Update an existing Wiki.js page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_id": {
                                "type": "integer",
                                "description": "Page ID"
                            },
                            "content": {
                                "type": "string",
                                "description": "New content (optional)"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description (optional)"
                            },
                            "tags": {
                                "type": "string",
                                "description": "New comma-separated tags (optional)"
                            },
                            "publish": {
                                "type": "boolean",
                                "description": "New publish status (optional)"
                            }
                        },
                        "required": ["page_id"]
                    }
                ),
                Tool(
                    name="list_pages",
                    description="List pages under a specific path",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path_prefix": {
                                "type": "string",
                                "default": "",
                                "description": "Path prefix to filter by"
                            }
                        }
                    }
                ),
                Tool(
                    name="create_lesson",
                    description="Create a lessons learned entry to prevent repeating mistakes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Lesson title (e.g., 'Sprint 16 - Prevent Infinite Loops')"
                            },
                            "content": {
                                "type": "string",
                                "description": "Lesson content (markdown with problem, solution, prevention)"
                            },
                            "tags": {
                                "type": "string",
                                "description": "Comma-separated tags for categorization"
                            },
                            "category": {
                                "type": "string",
                                "default": "sprints",
                                "description": "Category (sprints, patterns, architecture, etc.)"
                            }
                        },
                        "required": ["title", "content", "tags"]
                    }
                ),
                Tool(
                    name="search_lessons",
                    description="Search lessons learned from previous sprints to avoid known pitfalls",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (optional)"
                            },
                            "tags": {
                                "type": "string",
                                "description": "Comma-separated tags to filter by (optional)"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 20,
                                "description": "Maximum results"
                            }
                        }
                    }
                ),
                Tool(
                    name="tag_lesson",
                    description="Add or update tags on a lessons learned entry",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_id": {
                                "type": "integer",
                                "description": "Lesson page ID"
                            },
                            "tags": {
                                "type": "string",
                                "description": "Comma-separated tags"
                            }
                        },
                        "required": ["page_id", "tags"]
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
                # Route to appropriate client method
                if name == "search_pages":
                    tags = arguments.get('tags')
                    tag_list = [t.strip() for t in tags.split(',')] if tags else None
                    results = await self.client.search_pages(
                        query=arguments['query'],
                        tags=tag_list,
                        limit=arguments.get('limit', 20)
                    )
                    result = {'success': True, 'count': len(results), 'pages': results}

                elif name == "get_page":
                    page = await self.client.get_page(arguments['path'])
                    if page:
                        result = {'success': True, 'page': page}
                    else:
                        result = {'success': False, 'error': f"Page not found: {arguments['path']}"}

                elif name == "create_page":
                    tags = arguments.get('tags')
                    tag_list = [t.strip() for t in tags.split(',')] if tags else []
                    page = await self.client.create_page(
                        path=arguments['path'],
                        title=arguments['title'],
                        content=arguments['content'],
                        description=arguments.get('description', ''),
                        tags=tag_list,
                        is_published=arguments.get('publish', True)
                    )
                    result = {'success': True, 'page': page}

                elif name == "update_page":
                    tags = arguments.get('tags')
                    tag_list = [t.strip() for t in tags.split(',')] if tags else None
                    page = await self.client.update_page(
                        page_id=arguments['page_id'],
                        content=arguments.get('content'),
                        title=arguments.get('title'),
                        description=arguments.get('description'),
                        tags=tag_list,
                        is_published=arguments.get('publish')
                    )
                    result = {'success': True, 'page': page}

                elif name == "list_pages":
                    pages = await self.client.list_pages(
                        path_prefix=arguments.get('path_prefix', '')
                    )
                    result = {'success': True, 'count': len(pages), 'pages': pages}

                elif name == "create_lesson":
                    tag_list = [t.strip() for t in arguments['tags'].split(',')]
                    lesson = await self.client.create_lesson(
                        title=arguments['title'],
                        content=arguments['content'],
                        tags=tag_list,
                        category=arguments.get('category', 'sprints')
                    )
                    result = {
                        'success': True,
                        'lesson': lesson,
                        'message': f"Lesson learned captured: {arguments['title']}"
                    }

                elif name == "search_lessons":
                    tags = arguments.get('tags')
                    tag_list = [t.strip() for t in tags.split(',')] if tags else None
                    lessons = await self.client.search_lessons(
                        query=arguments.get('query'),
                        tags=tag_list,
                        limit=arguments.get('limit', 20)
                    )
                    result = {
                        'success': True,
                        'count': len(lessons),
                        'lessons': lessons,
                        'message': f"Found {len(lessons)} relevant lessons"
                    }

                elif name == "tag_lesson":
                    tag_list = [t.strip() for t in arguments['tags'].split(',')]
                    lesson = await self.client.tag_lesson(
                        page_id=arguments['page_id'],
                        new_tags=tag_list
                    )
                    result = {'success': True, 'lesson': lesson, 'message': 'Tags updated'}

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
                    text=json.dumps({'success': False, 'error': str(e)}, indent=2)
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
    server = WikiJSMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
