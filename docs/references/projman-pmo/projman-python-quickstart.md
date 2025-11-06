# ProjMan Plugins - Python Quick Start

This guide provides Python-specific setup and development information for the projman and projman-pmo plugins.

> **⚠️ IMPORTANT:** For the definitive repository structure, refer to [CORRECT-ARCHITECTURE.md](./CORRECT-ARCHITECTURE.md). This guide shows Python-specific patterns and setup.

---

## Technology Stack

- **MCP Server:** Python 3.11+
- **Commands:** Markdown files
- **Agents:** Markdown files
- **Dependencies:** pip with requirements.txt
- **Virtual Environment:** .venv (per plugin)

---

## Initial Setup

### 1. System Requirements

```bash
# Python 3.11 or higher
python --version

# pip (latest)
pip --version

# git
git --version
```

### 2. System-Level Configuration

```bash
# Create config directory
mkdir -p ~/.config/claude

# Create gitea.env with your credentials
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_token_here
GITEA_OWNER=hyperhivelabs
EOF

# Secure the file
chmod 600 ~/.config/claude/gitea.env
```

### 3. Project-Level Configuration

```bash
# In each repository root
echo "GITEA_REPO=cuisineflow" > .env

# Add to .gitignore
echo ".env" >> .gitignore
```

---

## MCP Server Structure

```
hyperhivelabs/claude-plugins/
├── mcp-servers/               # SHARED by both plugins
│   ├── gitea/
│   │   ├── .venv/
│   │   ├── requirements.txt
│   │   ├── mcp_server/
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   ├── config.py
│   │   │   ├── gitea_client.py
│   │   │   └── tools/
│   │   └── tests/
│   └── wikijs/
│       ├── .venv/
│       ├── requirements.txt
│       ├── mcp_server/
│       │   ├── __init__.py
│       │   ├── server.py
│       │   ├── config.py
│       │   └── wikijs_client.py
│       └── tests/
├── projman/
│   ├── .mcp.json              # Points to ../mcp-servers/
│   ├── commands/
│   └── agents/
└── projman-pmo/
    ├── .mcp.json              # Points to ../mcp-servers/
    └── commands/
```

---

## Dependencies (requirements.txt)

```txt
# anthropic-sdk==0.18.0  # MCP SDK
anthropic-sdk>=0.18.0
# python-dotenv==1.0.0   # Environment variable loading
python-dotenv>=1.0.0
# requests==2.31.0       # HTTP client for Gitea API
requests>=2.31.0
# pydantic==2.5.0        # Data validation
pydantic>=2.5.0
# pytest==7.4.3          # Testing framework
pytest>=7.4.3
# pytest-asyncio==0.23.0 # Async testing support
pytest-asyncio>=0.23.0
```

**Note:** Following your coding preferences, library versions are specified with comments showing the exact version being used.

---

## Development Workflow

### Initial MCP Server Setup

```bash
# Navigate to MCP servers directory
cd /path/to/claude-plugins/mcp-servers/gitea

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import anthropic; print('SDK installed')"
```

### Configuration Loader (config.py)

```python
# mcp-servers/gitea/mcp_server/config.py
from pathlib import Path
from dotenv import load_dotenv
import os
from typing import Dict, Optional

class Config:
    """Hybrid configuration loader for projman plugins"""
    
    def __init__(self):
        self.api_url: Optional[str] = None
        self.api_token: Optional[str] = None
        self.owner: Optional[str] = None
        self.repo: Optional[str] = None
    
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
        
        # Validate required variables
        self._validate()
        
        return {
            'api_url': self.api_url,
            'api_token': self.api_token,
            'owner': self.owner,
            'repo': self.repo
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

# Usage
config = Config()
config_dict = config.load()
```

### Gitea API Client (gitea_client.py)

```python
# mcp-servers/gitea/mcp_server/gitea_client.py
import requests
from typing import List, Dict, Optional
from .config import Config

class GiteaClient:
    """Client for interacting with Gitea API"""
    
    def __init__(self):
        config = Config()
        config_dict = config.load()
        
        self.base_url = config_dict['api_url']
        self.token = config_dict['api_token']
        self.owner = config_dict['owner']
        self.repo = config_dict.get('repo')  # Optional
        
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
```

### MCP Server Entry Point (server.py)

```python
# mcp-servers/gitea/mcp_server/server.py
from anthropic import Anthropic
from .gitea_client import GiteaClient
from .tools import IssueTools, LabelTools, WikiTools

class ProjManMCPServer:
    """Main MCP server for projman plugin"""
    
    def __init__(self):
        self.gitea = GiteaClient()
        self.issue_tools = IssueTools(self.gitea)
        self.label_tools = LabelTools(self.gitea)
        self.wiki_tools = WikiTools(self.gitea)
    
    def register_tools(self):
        """Register all available MCP tools"""
        return [
            # Issue tools
            self.issue_tools.list_issues,
            self.issue_tools.get_issue,
            self.issue_tools.create_issue,
            self.issue_tools.update_issue,
            self.issue_tools.add_comment,
            
            # Label tools
            self.label_tools.get_labels,
            self.label_tools.suggest_labels,
            
            # Wiki tools
            self.wiki_tools.search_wiki,
            self.wiki_tools.get_wiki_page,
            self.wiki_tools.create_wiki_page
        ]

if __name__ == '__main__':
    server = ProjManMCPServer()
    # MCP server startup logic here
```

---

## Testing

### Unit Tests

```python
# tests/test_config.py
import pytest
from pathlib import Path
from mcp_server.config import Config

def test_load_system_config(tmp_path):
    """Test loading system-level configuration"""
    # Create mock system config
    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)
    
    config_file = config_dir / 'gitea.env'
    config_file.write_text(
        "GITEA_API_URL=https://test.com/api/v1\n"
        "GITEA_API_TOKEN=test_token\n"
        "GITEA_OWNER=test_owner\n"
    )
    
    # Test config loading
    config = Config()
    # ... test assertions

def test_project_config_override(tmp_path):
    """Test that project config overrides system config"""
    # ... test implementation

def test_missing_required_config():
    """Test error handling for missing configuration"""
    with pytest.raises(ValueError):
        config = Config()
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
        labels=["Type/Bug"]
    )
    assert issue['title'] == "Test Issue"
    assert "Type/Bug" in [label['name'] for label in issue['labels']]
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

## .mcp.json Configuration

### projman (Repository-Specific)

```json
{
  "mcpServers": {
    "gitea-projman": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
        "GITEA_API_URL": "${GITEA_API_URL}",
        "GITEA_API_TOKEN": "${GITEA_API_TOKEN}",
        "GITEA_OWNER": "${GITEA_OWNER}",
        "GITEA_REPO": "${GITEA_REPO}"
      }
    },
    "wikijs-projman": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
        "WIKIJS_API_URL": "${WIKIJS_API_URL}",
        "WIKIJS_API_TOKEN": "${WIKIJS_API_TOKEN}",
        "WIKIJS_BASE_PATH": "${WIKIJS_BASE_PATH}",
        "WIKIJS_PROJECT": "${WIKIJS_PROJECT}"
      }
    }
  }
}
```

### projman-pmo (Multi-Project)

```json
{
  "mcpServers": {
    "gitea-pmo": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/gitea",
        "GITEA_API_URL": "${GITEA_API_URL}",
        "GITEA_API_TOKEN": "${GITEA_API_TOKEN}",
        "GITEA_OWNER": "${GITEA_OWNER}"
      }
    },
    "wikijs-pmo": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/../mcp-servers/wikijs",
        "WIKIJS_API_URL": "${WIKIJS_API_URL}",
        "WIKIJS_API_TOKEN": "${WIKIJS_API_TOKEN}",
        "WIKIJS_BASE_PATH": "${WIKIJS_BASE_PATH}"
      }
    }
  }
}
```

**Note:** Both plugins reference `../mcp-servers/` (shared location). PMO doesn't use `GITEA_REPO` since it operates across all repositories.

---

## Modular Code Structure (Following Your Preferences)

### Single Responsibility Functions

```python
def validate_configuration(config: Dict[str, str]) -> None:
    """
    Validate that all required configuration values are present.
    Raises ValueError if any required values are missing.
    """
    required_keys = ['api_url', 'api_token', 'owner']
    missing = [key for key in required_keys if not config.get(key)]
    
    if missing:
        raise ValueError(f"Missing configuration: {', '.join(missing)}")

def load_system_config() -> Dict[str, str]:
    """
    Load configuration from system-level gitea.env file.
    Returns dictionary of configuration values.
    """
    config_path = Path.home() / '.config' / 'claude' / 'gitea.env'
    
    if not config_path.exists():
        raise FileNotFoundError(f"System config not found: {config_path}")
    
    load_dotenv(config_path)
    
    return {
        'api_url': os.getenv('GITEA_API_URL'),
        'api_token': os.getenv('GITEA_API_TOKEN'),
        'owner': os.getenv('GITEA_OWNER')
    }

def load_project_config() -> Dict[str, Optional[str]]:
    """
    Load project-specific configuration from local .env file.
    Returns dictionary with 'repo' key, value may be None if not configured.
    """
    project_env = Path.cwd() / '.env'
    
    if project_env.exists():
        load_dotenv(project_env, override=True)
    
    return {
        'repo': os.getenv('GITEA_REPO')
    }

def merge_configurations(system: Dict, project: Dict) -> Dict[str, str]:
    """
    Merge system and project configurations.
    Project values override system values where present.
    """
    merged = system.copy()
    merged.update({k: v for k, v in project.items() if v is not None})
    return merged

def main():
    """Main entry point that orchestrates configuration loading"""
    system_config = load_system_config()
    project_config = load_project_config()
    final_config = merge_configurations(system_config, project_config)
    validate_configuration(final_config)
    return final_config
```

---

## Virtual Environment Management

### Creation

```bash
# In plugin mcp-server directory
python -m venv .venv
```

### Activation

```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Deactivation

```bash
deactivate
```

### Cleanup & Rebuild

```bash
# Remove old virtual environment
rm -rf .venv

# Create fresh virtual environment
python -m venv .venv

# Activate and reinstall
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Debugging

### Enable Debug Logging

```python
# Add to server.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Common Issues

**Issue:** Module not found
```bash
# Solution: Ensure PYTHONPATH is set in .mcp.json
"env": {
  "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/mcp-server"
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

---

## Performance Optimization

### Caching with functools

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_labels_cached(repo: str) -> List[Dict]:
    """Cached label retrieval to reduce API calls"""
    return self.gitea.get_labels(repo)
```

### Async Operations

```python
import asyncio
import aiohttp

async def fetch_multiple_repos(repos: List[str]) -> List[Dict]:
    """Fetch data from multiple repositories concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_repo_data(session, repo) for repo in repos]
        return await asyncio.gather(*tasks)
```

---

## Next Steps

1. **Set up system configuration** as shown above
2. **Create project configuration** in your first repository
3. **Navigate to Phase 1.1** of the implementation plan
4. **Build the MCP server** following the structure above
5. **Write tests** as you implement each component
6. **Test with real Gitea instance** early and often

---

## Key Differences from Node.js Approach

| Aspect | Node.js | Python (Your Choice) |
|--------|---------|---------------------|
| Dependencies | package.json | requirements.txt |
| Package Manager | npm/yarn | pip |
| Isolation | node_modules | .venv |
| Module System | ES6 imports | Python imports |
| Async | async/await | async/await |
| Type Checking | TypeScript | Type hints + Pydantic |
| Testing | Jest | pytest |

---

## Resources

- **Anthropic MCP SDK (Python):** https://github.com/anthropics/anthropic-sdk-python
- **Python Requests:** https://docs.python-requests.org/
- **Pydantic:** https://docs.pydantic.dev/
- **pytest:** https://docs.pytest.org/
- **Gitea API Docs:** https://docs.gitea.com/api/

---

Ready to build! 🚀