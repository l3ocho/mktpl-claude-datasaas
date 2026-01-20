"""
Milestone management tools for MCP server.

Provides async wrappers for milestone operations:
- CRUD operations for milestones
- Milestone-sprint relationship tracking
"""
import asyncio
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MilestoneTools:
    """Async wrappers for Gitea milestone operations"""

    def __init__(self, gitea_client):
        """
        Initialize milestone tools.

        Args:
            gitea_client: GiteaClient instance
        """
        self.gitea = gitea_client

    async def list_milestones(
        self,
        state: str = 'open',
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        List all milestones in repository.

        Args:
            state: Milestone state (open, closed, all)
            repo: Repository in owner/repo format

        Returns:
            List of milestone dictionaries
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.list_milestones(state, repo)
        )

    async def get_milestone(
        self,
        milestone_id: int,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Get a specific milestone by ID.

        Args:
            milestone_id: Milestone ID
            repo: Repository in owner/repo format

        Returns:
            Milestone dictionary
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.get_milestone(milestone_id, repo)
        )

    async def create_milestone(
        self,
        title: str,
        description: Optional[str] = None,
        due_on: Optional[str] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a new milestone.

        Args:
            title: Milestone title (e.g., "v2.0 Release", "Sprint 17")
            description: Milestone description
            due_on: Due date in ISO 8601 format (e.g., "2025-02-01T00:00:00Z")
            repo: Repository in owner/repo format

        Returns:
            Created milestone dictionary
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.create_milestone(title, description, due_on, repo)
        )

    async def update_milestone(
        self,
        milestone_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
        due_on: Optional[str] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Update an existing milestone.

        Args:
            milestone_id: Milestone ID
            title: New title (optional)
            description: New description (optional)
            state: New state - 'open' or 'closed' (optional)
            due_on: New due date (optional)
            repo: Repository in owner/repo format

        Returns:
            Updated milestone dictionary
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.update_milestone(
                milestone_id, title, description, state, due_on, repo
            )
        )

    async def delete_milestone(
        self,
        milestone_id: int,
        repo: Optional[str] = None
    ) -> bool:
        """
        Delete a milestone.

        Args:
            milestone_id: Milestone ID
            repo: Repository in owner/repo format

        Returns:
            True if deleted successfully
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.delete_milestone(milestone_id, repo)
        )
