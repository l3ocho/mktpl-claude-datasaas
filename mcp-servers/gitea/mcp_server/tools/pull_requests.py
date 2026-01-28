"""
Pull request management tools for MCP server.

Provides async wrappers for PR operations with:
- Branch-aware security
- PMO multi-repo support
- Comprehensive error handling
"""
import asyncio
import os
import subprocess
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PullRequestTools:
    """Async wrappers for Gitea pull request operations with branch detection"""

    def __init__(self, gitea_client):
        """
        Initialize pull request tools.

        Args:
            gitea_client: GiteaClient instance
        """
        self.gitea = gitea_client

    def _get_project_directory(self) -> Optional[str]:
        """
        Get the user's project directory from environment.

        Returns:
            Project directory path or None if not set
        """
        return os.environ.get('CLAUDE_PROJECT_DIR')

    def _get_current_branch(self) -> str:
        """
        Get current git branch from user's project directory.

        Uses CLAUDE_PROJECT_DIR environment variable to determine the correct
        directory for git operations, avoiding the bug where git runs from
        the installed plugin directory instead of the user's project.

        Returns:
            Current branch name or 'unknown' if not in a git repo
        """
        try:
            project_dir = self._get_project_directory()
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True,
                cwd=project_dir  # Run git in project directory, not plugin directory
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"

    def _check_branch_permissions(self, operation: str) -> bool:
        """
        Check if operation is allowed on current branch.

        Args:
            operation: Operation name (list_prs, create_review, etc.)

        Returns:
            True if operation is allowed, False otherwise
        """
        branch = self._get_current_branch()

        # Read-only operations allowed everywhere
        read_ops = ['list_pull_requests', 'get_pull_request', 'get_pr_diff', 'get_pr_comments']

        # Production branches (read-only)
        if branch in ['main', 'master'] or branch.startswith('prod/'):
            return operation in read_ops

        # Staging branches (read-only for PRs, can comment)
        if branch == 'staging' or branch.startswith('stage/'):
            return operation in read_ops + ['add_pr_comment']

        # Development branches (full access)
        # Include all common feature/fix branch patterns
        dev_prefixes = (
            'feat/', 'feature/', 'dev/',
            'fix/', 'bugfix/', 'hotfix/',
            'chore/', 'refactor/', 'docs/', 'test/'
        )
        if branch in ['development', 'develop'] or branch.startswith(dev_prefixes):
            return True

        # Unknown branch - be restrictive
        return operation in read_ops

    async def list_pull_requests(
        self,
        state: str = 'open',
        sort: str = 'recentupdate',
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        List pull requests from repository (async wrapper).

        Args:
            state: PR state (open, closed, all)
            sort: Sort order
            labels: Filter by labels
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            List of pull request dictionaries

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('list_pull_requests'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot list PRs on branch '{branch}'. "
                f"Switch to a development branch."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.list_pull_requests(state, sort, labels, repo)
        )

    async def get_pull_request(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Get specific pull request details (async wrapper).

        Args:
            pr_number: Pull request number
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Pull request dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('get_pull_request'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot get PR on branch '{branch}'. "
                f"Switch to a development branch."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.get_pull_request(pr_number, repo)
        )

    async def get_pr_diff(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> str:
        """
        Get pull request diff (async wrapper).

        Args:
            pr_number: Pull request number
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Diff as string

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('get_pr_diff'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot get PR diff on branch '{branch}'. "
                f"Switch to a development branch."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.get_pr_diff(pr_number, repo)
        )

    async def get_pr_comments(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        Get comments on a pull request (async wrapper).

        Args:
            pr_number: Pull request number
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            List of comment dictionaries

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('get_pr_comments'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot get PR comments on branch '{branch}'. "
                f"Switch to a development branch."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.get_pr_comments(pr_number, repo)
        )

    async def create_pr_review(
        self,
        pr_number: int,
        body: str,
        event: str = 'COMMENT',
        comments: Optional[List[Dict]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a review on a pull request (async wrapper with branch check).

        Args:
            pr_number: Pull request number
            body: Review body/summary
            event: Review action (APPROVE, REQUEST_CHANGES, COMMENT)
            comments: Optional list of inline comments
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Created review dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('create_pr_review'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot create PR review on branch '{branch}'. "
                f"Switch to a development branch to review PRs."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.create_pr_review(pr_number, body, event, comments, repo)
        )

    async def add_pr_comment(
        self,
        pr_number: int,
        body: str,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Add a general comment to a pull request (async wrapper with branch check).

        Args:
            pr_number: Pull request number
            body: Comment text
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Created comment dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('add_pr_comment'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot add PR comment on branch '{branch}'. "
                f"Switch to a development or staging branch to comment on PRs."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.add_pr_comment(pr_number, body, repo)
        )

    async def create_pull_request(
        self,
        title: str,
        body: str,
        head: str,
        base: str,
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a new pull request (async wrapper with branch check).

        Args:
            title: PR title
            body: PR description/body
            head: Source branch name (the branch with changes)
            base: Target branch name (the branch to merge into)
            labels: Optional list of label names
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Created pull request dictionary

        Raises:
            PermissionError: If operation not allowed on current branch
        """
        if not self._check_branch_permissions('create_pull_request'):
            branch = self._get_current_branch()
            raise PermissionError(
                f"Cannot create PR on branch '{branch}'. "
                f"Switch to a development or feature branch to create PRs."
            )

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.gitea.create_pull_request(title, body, head, base, labels, repo)
        )
