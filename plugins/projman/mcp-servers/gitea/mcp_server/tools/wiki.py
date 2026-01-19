"""
Wiki management tools for MCP server.

Provides async wrappers for wiki operations to support lessons learned:
- Page CRUD operations
- Lessons learned creation and search
"""
import asyncio
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WikiTools:
    """Async wrappers for Gitea wiki operations"""

    def __init__(self, gitea_client):
        """
        Initialize wiki tools.

        Args:
            gitea_client: GiteaClient instance
        """
        self.gitea = gitea_client

    async def list_wiki_pages(self, repo: Optional[str] = None) -> List[Dict]:
        """List all wiki pages in repository."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.list_wiki_pages(repo)
        )

    async def get_wiki_page(
        self,
        page_name: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Get a specific wiki page by name."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.get_wiki_page(page_name, repo)
        )

    async def create_wiki_page(
        self,
        title: str,
        content: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Create a new wiki page."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.create_wiki_page(title, content, repo)
        )

    async def update_wiki_page(
        self,
        page_name: str,
        content: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Update an existing wiki page."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.update_wiki_page(page_name, content, repo)
        )

    async def delete_wiki_page(
        self,
        page_name: str,
        repo: Optional[str] = None
    ) -> bool:
        """Delete a wiki page."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.delete_wiki_page(page_name, repo)
        )

    async def search_wiki_pages(
        self,
        query: str,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """Search wiki pages by title."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.search_wiki_pages(query, repo)
        )

    async def create_lesson(
        self,
        title: str,
        content: str,
        tags: List[str],
        category: str = "sprints",
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a lessons learned entry in the wiki.

        Args:
            title: Lesson title (e.g., "Sprint 16 - Prevent Infinite Loops")
            content: Lesson content in markdown
            tags: List of tags for categorization
            category: Category (sprints, patterns, architecture, etc.)
            repo: Repository in owner/repo format

        Returns:
            Created wiki page
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.create_lesson(title, content, tags, category, repo)
        )

    async def search_lessons(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        Search lessons learned from previous sprints.

        Args:
            query: Search query (optional)
            tags: Tags to filter by (optional)
            limit: Maximum results (default 20)
            repo: Repository in owner/repo format

        Returns:
            List of matching lessons
        """
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: self.gitea.search_lessons(query, tags, repo)
        )
        return results[:limit]
