"""
Issue management tools for MCP server.

Provides async wrappers for issue CRUD operations with:
- Branch-aware security
- PMO multi-repo support
- Comprehensive error handling
"""
import asyncio
import subprocess
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IssueTools:
    """Async wrappers for Gitea issue operations with branch detection"""

    def __init__(self, gitea_client):
        """
        Initialize issue tools.

        Args:
            gitea_client: GiteaClient instance
        """
        self.gitea = gitea_client

    def _get_current_branch(self) -> str:
        """
        Get current git branch.

        Returns:
            Current branch name or 'unknown' if not in a git repo
        """
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"

    def _check_branch_permissions(self, operation: str) -> bool:
        """
        Check if operation is allowed on current branch.

        Args:
            operation: Operation name (list_issues, create_issue, etc.)

        Returns:
            True if operation is allowed, False otherwise
        """
        branch = self._get_current_branch()

        # Production branches (read-only except incidents)
        if branch in ['main', 'master'] or branch.startswith('prod/'):
            return operation in ['list_issues', 'get_issue', 'get_labels']

        # Staging branches (read-only for code)
        if branch == 'staging' or branch.startswith('stage/'):
            return operation in ['list_issues', 'get_issue', 'get_labels', 'create_issue']

        # Development branches (full access)
        if branch in ['development', 'develop'] or branch.startswith(('feat/', 'feature/', 'dev/')):
            return True

        # Unknown branch - be restrictive
        return False

    async def list_issues(
        self,
        state: str = 'open',
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        List issues from repository (async wrapper).

        Args:
            state: Issue state (open, closed, all)
            labels: Filter by labels
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            List of issue dictionaries

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('list_issues'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot list issues on branch '{branch}'. "
                f"Switch to a development branch."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.list_issues(state, labels, repo)
        )

    async def get_issue(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Get specific issue details (async wrapper).

        Args:
            issue_number: Issue number
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Issue dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('get_issue'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot get issue on branch '{branch}'. "
                f"Switch to a development branch."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.get_issue(issue_number, repo)
        )

    async def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create new issue (async wrapper with branch check).

        Args:
            title: Issue title
            body: Issue description
            labels: List of label names
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Created issue dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('create_issue'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot create issues on branch '{branch}'. "
                f"Switch to a development branch to create issues."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.create_issue(title, body, labels, repo)
        )

    async def update_issue(
        self,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Update existing issue (async wrapper with branch check).

        Args:
            issue_number: Issue number
            title: New title (optional)
            body: New body (optional)
            state: New state - 'open' or 'closed' (optional)
            labels: New labels (optional)
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Updated issue dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('update_issue'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot update issues on branch '{branch}'. "
                f"Switch to a development branch to update issues."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.update_issue(issue_number, title, body, state, labels, repo)
        )

    async def add_comment(
        self,
        issue_number: int,
        comment: str,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Add comment to issue (async wrapper with branch check).

        Args:
            issue_number: Issue number
            comment: Comment text
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Created comment dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('add_comment'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot add comments on branch '{branch}'. "
                f"Switch to a development branch to add comments."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.add_comment(issue_number, comment, repo)
        )

    async def aggregate_issues(
        self,
        state: str = 'open',
        labels: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Aggregate issues across all repositories (PMO mode, async wrapper).

        Args:
            state: Issue state (open, closed, all)
            labels: Filter by labels

        Returns:
            Dictionary mapping repository names to issue lists

        Raises:
            ValueError: If not in company mode
            PermissionError: If operation not allowed on current branch
        """
        if self.gitea.mode != 'company':
            raise ValueError("aggregate_issues only available in company mode")

        if not self._check_branch_permissions('aggregate_issues'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot aggregate issues on branch '{branch}'. "
                f"Switch to a development branch."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.aggregate_issues(state, labels)
        )
