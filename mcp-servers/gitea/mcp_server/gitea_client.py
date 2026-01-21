"""
Gitea API client for interacting with Gitea API.

Provides synchronous methods for:
- Issue CRUD operations
- Label management
- Repository operations
- PMO multi-repo aggregation
- Wiki operations (lessons learned)
- Milestone management
- Issue dependencies
"""
import requests
import logging
import re
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
            raise ValueError("Use 'owner/repo' format (e.g. 'org/repo-name')")
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
        full_repo = f"{owner}/{repo}"

        # Only fetch org labels if repo belongs to an organization
        org_labels = []
        if self.is_org_repo(full_repo):
            org_labels = self.get_org_labels(owner)

        repo_labels = self.get_labels(full_repo)
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

    # ========================================
    # WIKI OPERATIONS (Lessons Learned)
    # ========================================

    def list_wiki_pages(self, repo: Optional[str] = None) -> List[Dict]:
        """List all wiki pages in repository."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/wiki/pages"
        logger.info(f"Listing wiki pages from {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_wiki_page(
        self,
        page_name: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Get a specific wiki page by name."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/wiki/page/{page_name}"
        logger.info(f"Getting wiki page '{page_name}' from {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_wiki_page(
        self,
        title: str,
        content: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Create a new wiki page."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/wiki/new"
        data = {
            'title': title,
            'content_base64': self._encode_base64(content)
        }
        logger.info(f"Creating wiki page '{title}' in {owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def update_wiki_page(
        self,
        page_name: str,
        content: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Update an existing wiki page."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/wiki/page/{page_name}"
        data = {
            'content_base64': self._encode_base64(content)
        }
        logger.info(f"Updating wiki page '{page_name}' in {owner}/{target_repo}")
        response = self.session.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete_wiki_page(
        self,
        page_name: str,
        repo: Optional[str] = None
    ) -> bool:
        """Delete a wiki page."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/wiki/page/{page_name}"
        logger.info(f"Deleting wiki page '{page_name}' from {owner}/{target_repo}")
        response = self.session.delete(url)
        response.raise_for_status()
        return True

    def _encode_base64(self, content: str) -> str:
        """Encode content to base64 for wiki API."""
        import base64
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')

    def _decode_base64(self, content: str) -> str:
        """Decode base64 content from wiki API."""
        import base64
        return base64.b64decode(content.encode('utf-8')).decode('utf-8')

    def search_wiki_pages(
        self,
        query: str,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """Search wiki pages by content (client-side filtering)."""
        pages = self.list_wiki_pages(repo)
        results = []
        query_lower = query.lower()
        for page in pages:
            if query_lower in page.get('title', '').lower():
                results.append(page)
        return results

    def create_lesson(
        self,
        title: str,
        content: str,
        tags: List[str],
        category: str = "sprints",
        repo: Optional[str] = None
    ) -> Dict:
        """Create a lessons learned entry in the wiki."""
        # Sanitize title for wiki page name
        page_name = f"lessons/{category}/{self._sanitize_page_name(title)}"

        # Add tags as metadata at the end of content
        full_content = f"{content}\n\n---\n**Tags:** {', '.join(tags)}"

        return self.create_wiki_page(page_name, full_content, repo)

    def search_lessons(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """Search lessons learned by query and/or tags."""
        pages = self.list_wiki_pages(repo)
        results = []

        for page in pages:
            title = page.get('title', '')
            # Filter to only lessons (pages starting with lessons/)
            if not title.startswith('lessons/'):
                continue

            # If query provided, check if it matches title
            if query:
                if query.lower() not in title.lower():
                    continue

            # Get full page content for tag matching if tags provided
            if tags:
                try:
                    full_page = self.get_wiki_page(title, repo)
                    content = self._decode_base64(full_page.get('content_base64', ''))
                    # Check if any tag is in the content
                    if not any(tag.lower() in content.lower() for tag in tags):
                        continue
                except Exception:
                    continue

            results.append(page)

        return results

    def _sanitize_page_name(self, title: str) -> str:
        """Convert title to valid wiki page name."""
        # Replace spaces with hyphens, remove special chars
        name = re.sub(r'[^\w\s-]', '', title)
        name = re.sub(r'[\s]+', '-', name)
        return name.lower()

    # ========================================
    # MILESTONE OPERATIONS
    # ========================================

    def list_milestones(
        self,
        state: str = 'open',
        repo: Optional[str] = None
    ) -> List[Dict]:
        """List all milestones in repository."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/milestones"
        params = {'state': state}
        logger.info(f"Listing milestones from {owner}/{target_repo}")
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_milestone(
        self,
        milestone_id: int,
        repo: Optional[str] = None
    ) -> Dict:
        """Get a specific milestone by ID."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/milestones/{milestone_id}"
        logger.info(f"Getting milestone #{milestone_id} from {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_milestone(
        self,
        title: str,
        description: Optional[str] = None,
        due_on: Optional[str] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """Create a new milestone."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/milestones"
        data = {'title': title}
        if description:
            data['description'] = description
        if due_on:
            data['due_on'] = due_on
        logger.info(f"Creating milestone '{title}' in {owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def update_milestone(
        self,
        milestone_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
        due_on: Optional[str] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """Update an existing milestone."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/milestones/{milestone_id}"
        data = {}
        if title is not None:
            data['title'] = title
        if description is not None:
            data['description'] = description
        if state is not None:
            data['state'] = state
        if due_on is not None:
            data['due_on'] = due_on
        logger.info(f"Updating milestone #{milestone_id} in {owner}/{target_repo}")
        response = self.session.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete_milestone(
        self,
        milestone_id: int,
        repo: Optional[str] = None
    ) -> bool:
        """Delete a milestone."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/milestones/{milestone_id}"
        logger.info(f"Deleting milestone #{milestone_id} from {owner}/{target_repo}")
        response = self.session.delete(url)
        response.raise_for_status()
        return True

    # ========================================
    # ISSUE DEPENDENCY OPERATIONS
    # ========================================

    def list_issue_dependencies(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """List all dependencies for an issue (issues that block this one)."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{issue_number}/dependencies"
        logger.info(f"Listing dependencies for issue #{issue_number} in {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_issue_dependency(
        self,
        issue_number: int,
        depends_on: int,
        repo: Optional[str] = None
    ) -> Dict:
        """Create a dependency (issue_number depends on depends_on)."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{issue_number}/dependencies"
        data = {
            'dependentIssue': {
                'owner': owner,
                'repo': target_repo,
                'index': depends_on
            }
        }
        logger.info(f"Creating dependency: #{issue_number} depends on #{depends_on} in {owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def remove_issue_dependency(
        self,
        issue_number: int,
        depends_on: int,
        repo: Optional[str] = None
    ) -> bool:
        """Remove a dependency between issues."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{issue_number}/dependencies"
        data = {
            'dependentIssue': {
                'owner': owner,
                'repo': target_repo,
                'index': depends_on
            }
        }
        logger.info(f"Removing dependency: #{issue_number} no longer depends on #{depends_on}")
        response = self.session.delete(url, json=data)
        response.raise_for_status()
        return True

    def list_issue_blocks(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """List all issues that this issue blocks."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{issue_number}/blocks"
        logger.info(f"Listing issues blocked by #{issue_number} in {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    # ========================================
    # REPOSITORY VALIDATION
    # ========================================

    def get_repo_info(self, repo: Optional[str] = None) -> Dict:
        """Get repository information including owner type."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}"
        logger.info(f"Getting repo info for {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def is_org_repo(self, repo: Optional[str] = None) -> bool:
        """Check if repository belongs to an organization (not a user)."""
        info = self.get_repo_info(repo)
        owner_type = info.get('owner', {}).get('type', '')
        return owner_type.lower() == 'organization'

    def get_branch_protection(
        self,
        branch: str,
        repo: Optional[str] = None
    ) -> Optional[Dict]:
        """Get branch protection rules for a branch."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/branch_protections/{branch}"
        logger.info(f"Getting branch protection for {branch} in {owner}/{target_repo}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None  # No protection rules
            raise

    def create_label(
        self,
        name: str,
        color: str,
        description: Optional[str] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """Create a new label in the repository."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/labels"
        data = {
            'name': name,
            'color': color.lstrip('#')  # Remove # if present
        }
        if description:
            data['description'] = description
        logger.info(f"Creating label '{name}' in {owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    # ========================================
    # PULL REQUEST OPERATIONS
    # ========================================

    def list_pull_requests(
        self,
        state: str = 'open',
        sort: str = 'recentupdate',
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """
        List pull requests from Gitea repository.

        Args:
            state: PR state (open, closed, all)
            sort: Sort order (oldest, recentupdate, leastupdate, mostcomment, leastcomment, priority)
            labels: Filter by labels
            repo: Repository in 'owner/repo' format

        Returns:
            List of pull request dictionaries
        """
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/pulls"
        params = {'state': state, 'sort': sort}
        if labels:
            params['labels'] = ','.join(labels)
        logger.info(f"Listing PRs from {owner}/{target_repo} with state={state}")
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_pull_request(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> Dict:
        """Get specific pull request details."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/pulls/{pr_number}"
        logger.info(f"Getting PR #{pr_number} from {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_pr_diff(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> str:
        """Get the diff for a pull request."""
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/pulls/{pr_number}.diff"
        logger.info(f"Getting diff for PR #{pr_number} from {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

    def get_pr_comments(
        self,
        pr_number: int,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """Get comments on a pull request (uses issue comments endpoint)."""
        owner, target_repo = self._parse_repo(repo)
        # PRs share comment endpoint with issues in Gitea
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{pr_number}/comments"
        logger.info(f"Getting comments for PR #{pr_number} from {owner}/{target_repo}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_pr_review(
        self,
        pr_number: int,
        body: str,
        event: str = 'COMMENT',
        comments: Optional[List[Dict]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """
        Create a review on a pull request.

        Args:
            pr_number: Pull request number
            body: Review body/summary
            event: Review action (APPROVE, REQUEST_CHANGES, COMMENT)
            comments: Optional list of inline comments with path, position, body
            repo: Repository in 'owner/repo' format

        Returns:
            Created review dictionary
        """
        owner, target_repo = self._parse_repo(repo)
        url = f"{self.base_url}/repos/{owner}/{target_repo}/pulls/{pr_number}/reviews"
        data = {
            'body': body,
            'event': event
        }
        if comments:
            data['comments'] = comments
        logger.info(f"Creating review on PR #{pr_number} in {owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def add_pr_comment(
        self,
        pr_number: int,
        body: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Add a general comment to a pull request (uses issue comment endpoint)."""
        owner, target_repo = self._parse_repo(repo)
        # PRs share comment endpoint with issues in Gitea
        url = f"{self.base_url}/repos/{owner}/{target_repo}/issues/{pr_number}/comments"
        data = {'body': body}
        logger.info(f"Adding comment to PR #{pr_number} in {owner}/{target_repo}")
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
