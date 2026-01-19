"""
Issue dependency management tools for MCP server.

Provides async wrappers for issue dependency operations:
- List/create/remove dependencies
- Build dependency graphs for parallel execution
"""
import asyncio
import logging
from typing import List, Dict, Optional, Set, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DependencyTools:
    """Async wrappers for Gitea issue dependency operations"""

    def __init__(self, gitea_client):
        """
        Initialize dependency tools.

        Args:
            gitea_client: GiteaClient instance
        """
        self.gitea = gitea_client

    async def list_issue_dependencies(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        List all dependencies for an issue (issues that block this one).

        Args:
            issue_number: Issue number
            repo: Repository in owner/repo format

        Returns:
            List of issues that this issue depends on
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.list_issue_dependencies(issue_number, repo)
        )

    async def create_issue_dependency(
        self,
        issue_number: int,
        depends_on: int,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a dependency between issues.

        Args:
            issue_number: The issue that will depend on another
            depends_on: The issue that blocks issue_number
            repo: Repository in owner/repo format

        Returns:
            Created dependency information
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.create_issue_dependency(issue_number, depends_on, repo)
        )

    async def remove_issue_dependency(
        self,
        issue_number: int,
        depends_on: int,
        repo: Optional[str] = None
    ) -> bool:
        """
        Remove a dependency between issues.

        Args:
            issue_number: The issue that currently depends on another
            depends_on: The issue being depended on
            repo: Repository in owner/repo format

        Returns:
            True if removed successfully
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.remove_issue_dependency(issue_number, depends_on, repo)
        )

    async def list_issue_blocks(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        List all issues that this issue blocks.

        Args:
            issue_number: Issue number
            repo: Repository in owner/repo format

        Returns:
            List of issues blocked by this issue
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.list_issue_blocks(issue_number, repo)
        )

    async def build_dependency_graph(
        self,
        issue_numbers: List[int],
        repo: Optional[str] = None
    ) -> Dict[int, List[int]]:
        """
        Build a dependency graph for a list of issues.

        Args:
            issue_numbers: List of issue numbers to analyze
            repo: Repository in owner/repo format

        Returns:
            Dictionary mapping issue_number -> list of issues it depends on
        """
        graph = {}
        for issue_num in issue_numbers:
            try:
                deps = await self.list_issue_dependencies(issue_num, repo)
                graph[issue_num] = [
                    d.get('number') or d.get('index')
                    for d in deps
                    if (d.get('number') or d.get('index')) in issue_numbers
                ]
            except Exception as e:
                logger.warning(f"Could not fetch dependencies for #{issue_num}: {e}")
                graph[issue_num] = []
        return graph

    async def get_ready_tasks(
        self,
        issue_numbers: List[int],
        completed: Set[int],
        repo: Optional[str] = None
    ) -> List[int]:
        """
        Get tasks that are ready to execute (no unresolved dependencies).

        Args:
            issue_numbers: List of all issue numbers in sprint
            completed: Set of already completed issue numbers
            repo: Repository in owner/repo format

        Returns:
            List of issue numbers that can be executed now
        """
        graph = await self.build_dependency_graph(issue_numbers, repo)
        ready = []

        for issue_num in issue_numbers:
            if issue_num in completed:
                continue

            deps = graph.get(issue_num, [])
            # Task is ready if all its dependencies are completed
            if all(dep in completed for dep in deps):
                ready.append(issue_num)

        return ready

    async def get_execution_order(
        self,
        issue_numbers: List[int],
        repo: Optional[str] = None
    ) -> List[List[int]]:
        """
        Get a parallelizable execution order for issues.

        Returns batches of issues that can be executed in parallel.
        Each batch contains issues with no unresolved dependencies.

        Args:
            issue_numbers: List of all issue numbers
            repo: Repository in owner/repo format

        Returns:
            List of batches, where each batch can be executed in parallel
        """
        graph = await self.build_dependency_graph(issue_numbers, repo)
        completed: Set[int] = set()
        remaining = set(issue_numbers)
        batches = []

        while remaining:
            # Find all tasks with no unresolved dependencies
            batch = []
            for issue_num in remaining:
                deps = graph.get(issue_num, [])
                if all(dep in completed for dep in deps):
                    batch.append(issue_num)

            if not batch:
                # Circular dependency detected
                logger.error(f"Circular dependency detected! Remaining: {remaining}")
                batch = list(remaining)  # Force include remaining to avoid infinite loop

            batches.append(batch)
            completed.update(batch)
            remaining -= set(batch)

        return batches
