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
        self.repo = config_dict.get('repo')  # Optional default repo in owner/repo format
        self.mode = config_dict['mode']

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.token}',
            'Content-Type': 'application/json'
        })

        logger.info(f"Gitea client initialized in {self.mode} mode")

    def _parse_repo(self, repo: Optional[str] = None) -> tuple:
        """Parse owner/repo from input. Always requires 'owner/repo' format."""
        target = repo or self.repo
        if not target or '/' not in target:
            raise ValueError("Use 'owner/repo' format (e.g. 'bandit/support-claude-mktplace')")
        parts = target.split('/', 1)
        return parts[0], parts[1]

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
            repo: Repository in 'owner/repo' format

        Returns:
            List of issue dictionaries
        """
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues"
        params = {'state': state}
        if labels:
            params['labels'] = ','.join(labels)
        logger.info(f"Listing issues from {owner}/{target_repo} with state={state}")
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_issue(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> Dict:
        """Get specific issue details."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{issue_number}"
        logger.info(f"Getting issue #{issue_number} from {owner}/{target_repo}")
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
        """Create a new issue in Gitea."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues"
        data = {'title': title, 'body': body}
        if labels:
            label_ids = self._resolve_label_ids(labels, owner, target_repo)
            data['labels'] = label_ids
        logger.info(f"Creating issue in {owner}/{target_repo}: {title}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _resolve_label_ids(self, label_names: List[str], owner: str, repo: str) -> List[int]:
        """Convert label names to label IDs."""
        org_labels = self.get_org_labels(owner)
        repo_labels = self.get_labels(f"{owner}/{repo}")
        all_labels = org_labels + repo_labels
        label_map = {label['name']: label['id'] for label in all_labels}
        label_ids = []
        for name in label_names:
            if name in label_map:
                label_ids.append(label_map[name])
            else:
                logger.warning(f"Label '{name}' not found, skipping")
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
        """Update existing issue. Repo must be 'owner/repo' format."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{issue_number}"
        data = {}
        if title is not None:
            data['title'] = title
        if body is not None:
            data['body'] = body
        if state is not None:
            data['state'] = state
        if labels is not None:
            data['labels'] = labels
        logger.info(f"Updating issue #{issue_number} in {owner}/{target_repo}")
        response = self.session.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def add_comment(
        self,
        issue_number: int,
        comment: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Add comment to issue. Repo must be 'owner/repo' format."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{issue_number}/comments"
        data = {'body': comment}
        logger.info(f"Adding comment to issue #{issue_number} in {owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_labels(self, repo: Optional[str] = None) -> List[Dict]:
        """Get all labels from repository. Repo must be 'owner/repo' format."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/labels"
        logger.info(f"Getting labels from {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_org_labels(self, org: str) -> List[Dict]:
        """Get organization-level labels. Org is the organization name."""
        url = f"{self.base_url}/orgs/{org}/labels"
        logger.info(f"Getting organization labels for {org}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_repos(self, org: str) -> List[Dict]:
        """List all repositories in organization. Org is the organization name."""
        url = f"{self.base_url}/orgs/{org}/repos"
        logger.info(f"Listing all repositories for organization {org}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def aggregate_issues(
        self,
        org: str,
        state: str = 'open',
        labels: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """Fetch issues across all repositories in org."""
        repos = self.list_repos(org)
        aggregated = {}
        logger.info(f"Aggregating issues across {len(repos)} repositories")
        for repo in repos:
            repo_name = repo['name']
            try:
                issues = self.list_issues(
                    state=state,
                    labels=labels,
                    repo=f"{org}/{repo_name}"
                )
                if issues:
                    aggregated[repo_name] = issues
                    logger.info(f"Found {len(issues)} issues in {repo_name}")
            except Exception as e:
                logger.error(f"Error fetching issues from {repo_name}: {e}")

        return aggregated
