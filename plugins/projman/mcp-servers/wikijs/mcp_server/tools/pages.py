"""
MCP tools for Wiki.js page management.
"""
from typing import Dict, Any, List, Optional
from mcp.server import Tool
from ..wikijs_client import WikiJSClient
import logging

logger = logging.getLogger(__name__)


def create_page_tools(client: WikiJSClient) -> List[Tool]:
    """
    Create MCP tools for page management.

    Args:
        client: WikiJSClient instance

    Returns:
        List of MCP tools
    """

    async def search_pages(
        query: str,
        tags: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search Wiki.js pages by keywords and tags.

        Args:
            query: Search query string
            tags: Comma-separated list of tags to filter by
            limit: Maximum number of results (default: 20)

        Returns:
            List of matching pages with path, title, description, and tags
        """
        try:
            tag_list = [t.strip() for t in tags.split(',')] if tags else None
            results = await client.search_pages(query, tag_list, limit)

            return {
                'success': True,
                'count': len(results),
                'pages': results
            }
        except Exception as e:
            logger.error(f"Error searching pages: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def get_page(path: str) -> Dict[str, Any]:
        """
        Get a specific page by path.

        Args:
            path: Page path (can be relative to project or absolute)

        Returns:
            Page data including content, metadata, and tags
        """
        try:
            page = await client.get_page(path)

            if page:
                return {
                    'success': True,
                    'page': page
                }
            else:
                return {
                    'success': False,
                    'error': f'Page not found: {path}'
                }
        except Exception as e:
            logger.error(f"Error getting page: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def create_page(
        path: str,
        title: str,
        content: str,
        description: str = "",
        tags: Optional[str] = None,
        publish: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new Wiki.js page.

        Args:
            path: Page path relative to project/base (e.g., 'documentation/api')
            title: Page title
            content: Page content in markdown format
            description: Page description (optional)
            tags: Comma-separated list of tags (optional)
            publish: Whether to publish immediately (default: True)

        Returns:
            Created page data
        """
        try:
            tag_list = [t.strip() for t in tags.split(',')] if tags else []

            page = await client.create_page(
                path=path,
                title=title,
                content=content,
                description=description,
                tags=tag_list,
                is_published=publish
            )

            return {
                'success': True,
                'page': page
            }
        except Exception as e:
            logger.error(f"Error creating page: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def update_page(
        page_id: int,
        content: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[str] = None,
        publish: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update an existing Wiki.js page.

        Args:
            page_id: Page ID (from get_page or search_pages)
            content: New content (optional)
            title: New title (optional)
            description: New description (optional)
            tags: New comma-separated tags (optional)
            publish: New publish status (optional)

        Returns:
            Updated page data
        """
        try:
            tag_list = [t.strip() for t in tags.split(',')] if tags else None

            page = await client.update_page(
                page_id=page_id,
                content=content,
                title=title,
                description=description,
                tags=tag_list,
                is_published=publish
            )

            return {
                'success': True,
                'page': page
            }
        except Exception as e:
            logger.error(f"Error updating page: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def list_pages(path_prefix: str = "") -> Dict[str, Any]:
        """
        List pages under a specific path.

        Args:
            path_prefix: Path prefix to filter by (relative to project/base)

        Returns:
            List of pages under the specified path
        """
        try:
            pages = await client.list_pages(path_prefix)

            return {
                'success': True,
                'count': len(pages),
                'pages': pages
            }
        except Exception as e:
            logger.error(f"Error listing pages: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    # Define MCP tools
    tools = [
        Tool(
            name="search_pages",
            description="Search Wiki.js pages by keywords and tags",
            function=search_pages
        ),
        Tool(
            name="get_page",
            description="Get a specific Wiki.js page by path",
            function=get_page
        ),
        Tool(
            name="create_page",
            description="Create a new Wiki.js page with content and metadata",
            function=create_page
        ),
        Tool(
            name="update_page",
            description="Update an existing Wiki.js page",
            function=update_page
        ),
        Tool(
            name="list_pages",
            description="List pages under a specific path",
            function=list_pages
        )
    ]

    return tools
