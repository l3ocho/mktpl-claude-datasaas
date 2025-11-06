# Gitea MCP Server Reference

## Overview

The Gitea MCP Server provides integration with Gitea for issue management, label operations, and repository tracking. It's shared by both `projman` and `projman-pmo` plugins, detecting its operating mode based on environment variables.

**Location:** `mcp-servers/gitea/` (repository root)

**Key Features:**
- Issue CRUD operations
- Label taxonomy management (43-label system)
- Mode detection (project-scoped vs company-wide)
- Hybrid configuration (system + project level)
- Python 3.11+ implementation

---

## Architecture

### Mode Detection

The MCP server operates in two modes based on environment variables:

**Project Mode (projman):**
- When `GITEA_REPO` is present
- Operates on single repository
- Used by projman plugin

**Company Mode (pmo):**
- When `GITEA_REPO` is absent
- Operates on all repositories in organization
- Used by projman-pmo plugin

```python
# mcp-servers/gitea/mcp_server/config.py
def load(self):
    # ... load configs ...

    self.repo = os.getenv('GITEA_REPO')  # Optional

    if self.repo:
        self.mode = 'project'
        logger.info(f"Running in project mode: {self.repo}")
    else:
        self.mode = 'company'
        logger.info("Running in company-wide mode (PMO)")

    return {
        'api_url': self.api_url,
        'api_token': self.api_token,
        'owner': self.owner,
        'repo': self.repo,
        'mode': self.mode
    }
```

---

## Configuration

### System-Level Configuration

**File:** `~/.config/claude/gitea.env`

```bash
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_gitea_token
GITEA_OWNER=hyperhivelabs
```

**Setup:**
```bash
# Create config directory
mkdir -p ~/.config/claude

# Create gitea.env
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_token
GITEA_OWNER=hyperhivelabs
EOF

# Secure the file
chmod 600 ~/.config/claude/gitea.env
```

### Project-Level Configuration

**File:** `project-root/.env`

```bash
# Repository name (project mode only)
GITEA_REPO=cuisineflow
```

**Setup:**
```bash
# In each project root
echo "GITEA_REPO=cuisineflow" > .env

# Add to .gitignore
echo ".env" >> .gitignore
```

### Configuration Loading Strategy

```python
# mcp-servers/gitea/mcp_server/config.py
from pathlib import Path
from dotenv import load_dotenv
import os
from typing import Dict, Optional

class GiteaConfig:
    """Hybrid configuration loader"""

    def __init__(self):
        self.api_url: Optional[str] = None
        self.api_token: Optional[str] = None
        self.owner: Optional[str] = None
        self.repo: Optional[str] = None
        self.mode: str = 'project'

    def load(self) -> Dict[str, str]:
        """
        Load configuration from system and project levels.
        Project-level configuration overrides system-level.
        """
        # Load system config
        system_config = Path.home() / '.config' / 'claude' / 'gitea.env'
        if system_config.exists():
            load_dotenv(system_config)
        else:
            raise FileNotFoundError(
                f"System config not found: {system_config}\n"
                "Create it with: mkdir -p ~/.config/claude && "
                "cat > ~/.config/claude/gitea.env"
            )

        # Load project config (overrides system)
        project_config = Path.cwd() / '.env'
        if project_config.exists():
            load_dotenv(project_config, override=True)

        # Extract values
        self.api_url = os.getenv('GITEA_API_URL')
        self.api_token = os.getenv('GITEA_API_TOKEN')
        self.owner = os.getenv('GITEA_OWNER')
        self.repo = os.getenv('GITEA_REPO')  # Optional for PMO

        # Detect mode
        self.mode = 'project' if self.repo else 'company'

        # Validate required variables
        self._validate()

        return {
            'api_url': self.api_url,
            'api_token': self.api_token,
            'owner': self.owner,
            'repo': self.repo,
            'mode': self.mode
        }

    def _validate(self) -> None:
        """Validate that required configuration is present"""
        required = {
            'GITEA_API_URL': self.api_url,
            'GITEA_API_TOKEN': self.api_token,
            'GITEA_OWNER': self.owner
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Check your ~/.config/claude/gitea.env file"
            )
```

---

## Directory Structure

```
mcp-servers/gitea/
├── .venv/                      # Python virtual environment
├── requirements.txt            # Python dependencies
├── .env.example               # Configuration template
├── mcp_server/
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   ├── config.py              # Configuration loader
│   ├── gitea_client.py        # Gitea API client
│   └── tools/
│       ├── __init__.py
│       ├── issues.py          # Issue CRUD tools
│       └── labels.py          # Label management tools
└── tests/
    ├── test_config.py
    ├── test_gitea_client.py
    └── test_tools.py
```

---

## Dependencies

**File:** `mcp-servers/gitea/requirements.txt`

```txt
anthropic-sdk>=0.18.0    # MCP SDK
python-dotenv>=1.0.0     # Environment variable loading
requests>=2.31.0         # HTTP client for Gitea API
pydantic>=2.5.0          # Data validation
pytest>=7.4.3            # Testing framework
pytest-asyncio>=0.23.0   # Async testing support
```

**Installation:**
```bash
cd mcp-servers/gitea
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## Gitea API Client

```python
# mcp-servers/gitea/mcp_server/gitea_client.py
import requests
from typing import List, Dict, Optional
from .config import GiteaConfig

class GiteaClient:
    """Client for interacting with Gitea API"""

    def __init__(self):
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
        """
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues"
        params = {'state': state}

        if labels:
            params['labels'] = ','.join(labels)

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_issue(
        self,
        issue_number: int,
        repo: Optional[str] = None
    ) -> Dict:
        """Get specific issue details"""
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues/{issue_number}"
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
        """Create a new issue in Gitea"""
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues"
        data = {
            'title': title,
            'body': body
        }

        if labels:
            data['labels'] = labels

        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def update_issue(
        self,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        repo: Optional[str] = None
    ) -> Dict:
        """Update existing issue"""
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

        response = self.session.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def add_comment(
        self,
        issue_number: int,
        comment: str,
        repo: Optional[str] = None
    ) -> Dict:
        """Add comment to issue"""
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/issues/{issue_number}/comments"
        data = {'body': comment}

        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_labels(
        self,
        repo: Optional[str] = None
    ) -> List[Dict]:
        """Get all labels from repository"""
        target_repo = repo or self.repo
        if not target_repo:
            raise ValueError("Repository not specified")

        url = f"{self.base_url}/repos/{self.owner}/{target_repo}/labels"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_org_labels(self) -> List[Dict]:
        """Get organization-level labels"""
        url = f"{self.base_url}/orgs/{self.owner}/labels"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    # PMO-specific methods

    def list_repos(self) -> List[Dict]:
        """List all repositories in organization (PMO mode)"""
        url = f"{self.base_url}/orgs/{self.owner}/repos"
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
        """
        repos = self.list_repos()
        aggregated = {}

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
            except Exception as e:
                # Log error but continue with other repos
                print(f"Error fetching issues from {repo_name}: {e}")

        return aggregated
```

---

## Label Taxonomy System

### 43-Label System

**Organization Labels (27):**
- Agent/2
- Complexity/3
- Efforts/5
- Priority/4
- Risk/3
- Source/4
- Type/6 (includes Type/Refactor)

**Repository Labels (16):**
- Component/9
- Tech/7

### Label Suggestion Logic

```python
# mcp-servers/gitea/mcp_server/tools/labels.py
from typing import List, Dict
import re

class LabelTools:
    def __init__(self, gitea_client):
        self.gitea = gitea_client

    async def get_labels(self, repo: str = None) -> List[Dict]:
        """Get all labels (org + repo)"""
        org_labels = self.gitea.get_org_labels()

        if repo or self.gitea.repo:
            target_repo = repo or self.gitea.repo
            repo_labels = self.gitea.get_labels(target_repo)
            return org_labels + repo_labels

        return org_labels

    async def suggest_labels(self, context: str) -> List[str]:
        """
        Analyze context and suggest appropriate labels.

        Args:
            context: Issue title + description or sprint context
        """
        suggested = []
        context_lower = context.lower()

        # Type detection (exclusive - only one)
        if any(word in context_lower for word in ['bug', 'error', 'fix', 'broken']):
            suggested.append('Type/Bug')
        elif any(word in context_lower for word in ['refactor', 'extract', 'restructure', 'architecture', 'service extraction']):
            suggested.append('Type/Refactor')
        elif any(word in context_lower for word in ['feature', 'add', 'implement', 'new']):
            suggested.append('Type/Feature')
        elif any(word in context_lower for word in ['docs', 'documentation', 'readme']):
            suggested.append('Type/Documentation')
        elif any(word in context_lower for word in ['test', 'testing', 'spec']):
            suggested.append('Type/Test')
        elif any(word in context_lower for word in ['chore', 'maintenance', 'update']):
            suggested.append('Type/Chore')

        # Priority detection
        if any(word in context_lower for word in ['critical', 'urgent', 'blocker', 'blocking']):
            suggested.append('Priority/Critical')
        elif any(word in context_lower for word in ['high', 'important', 'asap']):
            suggested.append('Priority/High')
        elif any(word in context_lower for word in ['low', 'nice-to-have', 'optional']):
            suggested.append('Priority/Low')
        else:
            suggested.append('Priority/Medium')

        # Component detection (based on keywords)
        component_keywords = {
            'Component/Backend': ['backend', 'server', 'api', 'database', 'service'],
            'Component/Frontend': ['frontend', 'ui', 'interface', 'react', 'vue'],
            'Component/API': ['api', 'endpoint', 'rest', 'graphql'],
            'Component/Database': ['database', 'db', 'sql', 'migration', 'schema'],
            'Component/Auth': ['auth', 'authentication', 'login', 'oauth', 'token'],
            'Component/Deploy': ['deploy', 'deployment', 'docker', 'kubernetes'],
            'Component/Testing': ['test', 'testing', 'spec', 'jest', 'pytest'],
            'Component/Docs': ['docs', 'documentation', 'readme', 'guide']
        }

        for label, keywords in component_keywords.items():
            if any(keyword in context_lower for keyword in keywords):
                suggested.append(label)

        # Source detection (based on git branch or context)
        if 'development' in context_lower or 'dev/' in context_lower:
            suggested.append('Source/Development')
        elif 'staging' in context_lower:
            suggested.append('Source/Staging')
        elif 'production' in context_lower or 'prod' in context_lower:
            suggested.append('Source/Production')

        return suggested
```

---

## MCP Tools

### Issue Tools

```python
# mcp-servers/gitea/mcp_server/tools/issues.py
class IssueTools:
    def __init__(self, gitea_client):
        self.gitea = gitea_client

    async def list_issues(self, state='open', labels=None, repo=None):
        """List issues in repository"""
        return self.gitea.list_issues(state=state, labels=labels, repo=repo)

    async def get_issue(self, issue_number, repo=None):
        """Get specific issue details"""
        return self.gitea.get_issue(issue_number, repo=repo)

    async def create_issue(self, title, body, labels=None, repo=None):
        """Create new issue"""
        return self.gitea.create_issue(title, body, labels=labels, repo=repo)

    async def update_issue(self, issue_number, title=None, body=None, state=None, labels=None, repo=None):
        """Update existing issue"""
        return self.gitea.update_issue(
            issue_number,
            title=title,
            body=body,
            state=state,
            labels=labels,
            repo=repo
        )

    async def add_comment(self, issue_number, comment, repo=None):
        """Add comment to issue"""
        return self.gitea.add_comment(issue_number, comment, repo=repo)

    # PMO-specific
    async def aggregate_issues(self, state='open', labels=None):
        """Aggregate issues across all repositories (PMO mode)"""
        if self.gitea.mode != 'company':
            raise ValueError("aggregate_issues only available in company mode")
        return self.gitea.aggregate_issues(state=state, labels=labels)
```

---

## Testing

### Unit Tests

```python
# tests/test_config.py
import pytest
from pathlib import Path
from mcp_server.config import GiteaConfig

def test_load_system_config(tmp_path, monkeypatch):
    """Test loading system-level configuration"""
    # Mock home directory
    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)

    config_file = config_dir / 'gitea.env'
    config_file.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        "GITEA_API_TOKEN=test_token\n"
        "GITEA_OWNER=test_owner\n"
    )

    monkeypatch.setenv('HOME', str(tmp_path))

    config = GiteaConfig()
    result = config.load()

    assert result['api_url'] == 'https://test.com/api/v1'
    assert result['api_token'] == 'test_token'
    assert result['owner'] == 'test_owner'
    assert result['mode'] == 'company'  # No repo specified

def test_project_config_override(tmp_path, monkeypatch):
    """Test that project config overrides system config"""
    # Set up system config
    system_config_dir = tmp_path / '.config' / 'claude'
    system_config_dir.mkdir(parents=True)

    system_config = system_config_dir / 'gitea.env'
    system_config.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        "GITEA_API_TOKEN=test_token\n"
        "GITEA_OWNER=test_owner\n"
    )

    # Set up project config
    project_dir = tmp_path / 'project'
    project_dir.mkdir()

    project_config = project_dir / '.env'
    project_config.write_text("GITEA_REPO=test_repo\n")

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)

    config = GiteaConfig()
    result = config.load()

    assert result['repo'] == 'test_repo'
    assert result['mode'] == 'project'

def test_missing_required_config():
    """Test error handling for missing configuration"""
    with pytest.raises(FileNotFoundError):
        config = GiteaConfig()
        config.load()
```

### Integration Tests

```python
# tests/test_gitea_client.py
import pytest
from mcp_server.gitea_client import GiteaClient

@pytest.fixture
def gitea_client():
    """Fixture providing configured Gitea client"""
    return GiteaClient()

def test_list_issues(gitea_client):
    """Test listing issues from Gitea"""
    issues = gitea_client.list_issues(state='open')
    assert isinstance(issues, list)

def test_create_issue(gitea_client):
    """Test creating an issue in Gitea"""
    issue = gitea_client.create_issue(
        title="Test Issue",
        body="Test body",
        labels=["Type/Bug", "Priority/Low"]
    )
    assert issue['title'] == "Test Issue"
    assert any(label['name'] == "Type/Bug" for label in issue['labels'])

def test_get_labels(gitea_client):
    """Test fetching labels"""
    labels = gitea_client.get_labels()
    assert isinstance(labels, list)
    assert len(labels) > 0

def test_pmo_mode_aggregate_issues():
    """Test PMO mode aggregation (no repo specified)"""
    # Set up client without repo
    client = GiteaClient()  # Should detect company mode

    if client.mode == 'company':
        aggregated = client.aggregate_issues(state='open')
        assert isinstance(aggregated, dict)
        # Each key should be a repo name
        for repo_name, issues in aggregated.items():
            assert isinstance(issues, list)
```

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_server --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v
```

---

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_labels_cached(self, repo: str) -> List[Dict]:
    """Cached label retrieval to reduce API calls"""
    return self.get_labels(repo)
```

### Retry Logic

```python
import time
from typing import Callable

def retry_on_failure(max_retries=3, delay=1):
    """Decorator for retrying failed API calls"""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

@retry_on_failure(max_retries=3)
def list_issues(self, state='open', labels=None, repo=None):
    """List issues with automatic retry"""
    # Implementation
```

---

## Troubleshooting

### Common Issues

**Issue:** Module not found
```bash
# Solution: Ensure PYTHONPATH is set in .mcp.json
"env": {
  "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea"
}
```

**Issue:** Configuration not loading
```bash
# Solution: Check file permissions
chmod 600 ~/.config/claude/gitea.env

# Verify file exists
cat ~/.config/claude/gitea.env
```

**Issue:** API authentication failing
```bash
# Solution: Test token manually
curl -H "Authorization: token YOUR_TOKEN" \
  https://your-gitea.com/api/v1/user
```

**Issue:** PMO mode not working
```bash
# Solution: Ensure GITEA_REPO is NOT set
# Check environment variables
env | grep GITEA
```

---

## Security

### Best Practices

1. **Token Storage:**
   - Store tokens in `~/.config/claude/gitea.env`
   - Set file permissions to 600
   - Never commit tokens to git

2. **Input Validation:**
   - Validate all user input before API calls
   - Sanitize issue titles and descriptions
   - Prevent injection attacks

3. **Error Handling:**
   - Don't leak tokens in error messages
   - Log errors without sensitive data
   - Provide user-friendly error messages

4. **API Rate Limiting:**
   - Implement exponential backoff
   - Cache frequently accessed data
   - Batch requests where possible

---

## Next Steps

1. **Set up system configuration**
2. **Create virtual environment**
3. **Install dependencies**
4. **Run tests against actual Gitea instance**
5. **Integrate with projman plugin**
