"""
Gitea API client for interacting with Gitea API.

Provides synchronous methods for:
- Issue CRUD operations
- Label management
- Repository operations
- PMO multi-repo aggregation
"""
import requests
import logging
from typing import List, Dict, Optional
from .config import GiteaConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GiteaClient:
    """Client for interacting with Gitea API"""

    def __init__(self):
        """Initialize Gitea client with configuration"""
        config = GiteaConfig()
        config_dict = config.load()

        self.base_url = config_dict['api_url']
        self.token = config_dict['api_token']
        self.owner = config_dict['owner']
        self.repo = config_dict.get('repo')  # Optional for PMO
        self.mode = config_dict['mode']

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.token}',
            'Content-Type': 'application/json'
        })

        logger.info(f"Gitea client initialized for {self.owner} in {self.mode} mode")

    def list_issues(
        self,
        state: str = 'open',
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        List issues from Gitea repository.

        Args:
            state: Issue state (open, closed, all)
            labels: Filter by labels
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            List of issue dictionaries

        Raises:
            ValueError: If repository not specified
            requests.HTTPError: If API request fails
        """
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues"
        params = {'state': state}

        if labels:
            params['labels'] = ','.join(labels)

        logger.info(f"Listing issues from {self.owner}/{target_repo} with state={state}")
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_issue(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Get specific issue details.

        Args:
            issue_number: Issue number
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Issue dictionary

        Raises:
            ValueError: If repository not specified
            requests.HTTPError: If API request fails
        """
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues/{issue_number}"
        logger.info(f"Getting issue #{issue_number} from {self.owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a new issue in Gitea.

        Args:
            title: Issue title
            body: Issue description
            labels: List of label names (will be converted to IDs)
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Created issue dictionary

        Raises:
            ValueError: If repository not specified
            requests.HTTPError: If API request fails
        """
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues"
        data = {
            'title': title,
            'body': body
        }

        if labels:
            # Convert label names to IDs (Gitea expects integer IDs, not strings)
            label_ids = self._resolve_label_ids(labels, target_repo)
            data['labels'] = label_ids

        logger.info(f"Creating issue in {self.owner}/{target_repo}: {title}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _resolve_label_ids(self, label_names: List[str], repo: str) -> List[int]:
        """
        Convert label names to label IDs.

        Args:
            label_names: List of label names (e.g., ['Type/Feature', 'Priority/High'])
            repo: Repository name

        Returns:
            List of label IDs
        """
        # Fetch all available labels (org + repo)
        org_labels = self.get_org_labels()
        repo_labels = self.get_labels(repo)
        all_labels = org_labels + repo_labels

        # Build name -> ID mapping
        label_map = {label['name']: label['id'] for label in all_labels}

        # Resolve IDs
        label_ids = []
        for name in label_names:
            if name in label_map:
                label_ids.append(label_map[name])
            else:
                logger.warning(f"Label '{name}' not found in Gitea, skipping")

        return label_ids

    def update_issue(
        self,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Update existing issue.

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
            ValueError: If repository not specified
            requests.HTTPError: If API request fails
        """
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues/{issue_number}"
        data = {}

        if title is not None:
            data['title'] = title
        if body is not None:
            data['body'] = body
        if state is not None:
            data['state'] = state
        if labels is not None:
            data['labels'] = labels

        logger.info(f"Updating issue #{issue_number} in {self.owner}/{target_repo}")
        response = self.session.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def add_comment(
        self,
        issue_number: int,
        comment: str,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Add comment to issue.

        Args:
            issue_number: Issue number
            comment: Comment text
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            Created comment dictionary

        Raises:
            ValueError: If repository not specified
            requests.HTTPError: If API request fails
        """
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues/{issue_number}/comments"
        data = {'body': comment}

        logger.info(f"Adding comment to issue #{issue_number} in {self.owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_labels(
        self,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        Get all labels from repository.

        Args:
            repo: Override configured repo (for PMO multi-repo)

        Returns:
            List of label dictionaries

        Raises:
            ValueError: If repository not specified
            requests.HTTPError: If API request fails
        """
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/labels"
        logger.info(f"Getting labels from {self.owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_org_labels(self) -> List[Dict]:
        """
        Get organization-level labels.

        Returns:
            List of organization label dictionaries

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/orgs/{self.owner}/labels"
        logger.info(f"Getting organization labels for {self.owner}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    # PMO-specific methods

    def list_repos(self) -> List[Dict]:
        """
        List all repositories in organization (PMO mode).

        Returns:
            List of repository dictionaries

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.base_url}/orgs/{self.owner}/repos"
        logger.info(f"Listing all repositories for organization {self.owner}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def aggregate_issues(
        self,
        state: str = 'open',
        labels: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Fetch issues across all repositories (PMO mode).
        Returns dict keyed by repository name.

        Args:
            state: Issue state (open, closed, all)
            labels: Filter by labels

        Returns:
            Dictionary mapping repository names to issue lists

        Raises:
            requests.HTTPError: If API request fails
        """
        repos = self.list_repos()
        aggregated = {}

        logger.info(f"Aggregating issues across {len(repos)} repositories")

        for repo in repos:
            repo_name = repo['name']
            try:
                issues = self.list_issues(
                    state=state,
                    labels=labels,
                    repo=repo_name
                )
                if issues:
                    aggregated[repo_name] = issues
                    logger.info(f"Found {len(issues)} issues in {repo_name}")
            except Exception as e:
                # Log error but continue with other repos
                logger.error(f"Error fetching issues from {repo_name}: {e}")

        return aggregated
