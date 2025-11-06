# Two MCP Server Architecture - Implementation Guide

## Overview

The projman plugin now uses **two separate MCP servers**:
1. **Gitea MCP Server** - Issues, labels, repository management
2. **Wiki.js MCP Server** - Documentation, lessons learned, knowledge base

This separation provides better maintainability, independent configuration, and leverages Wiki.js's superior documentation features.

> **⚠️ IMPORTANT:** For the definitive repository structure and configuration paths, refer to [CORRECT-ARCHITECTURE.md](./CORRECT-ARCHITECTURE.md). This guide provides detailed implementation examples and architectural deep-dive.

---

## Wiki.js Structure at Hyper Hive Labs

### Company-Wide Organization

```
Wiki.js Instance: https://wiki.hyperhivelabs.com
└── /hyper-hive-labs/                  # Base path for all HHL content
    ├── projects/                       # Project-specific documentation
    │   ├── cuisineflow/
    │   │   ├── lessons-learned/
    │   │   │   ├── sprints/
    │   │   │   │   ├── sprint-01-auth.md
    │   │   │   │   ├── sprint-02-api.md
    │   │   │   │   └── ...
    │   │   │   ├── patterns/
    │   │   │   │   ├── service-extraction.md
    │   │   │   │   └── database-migration.md
    │   │   │   └── INDEX.md
    │   │   └── documentation/
    │   │       ├── architecture/
    │   │       ├── api/
    │   │       └── deployment/
    │   ├── cuisineflow-site/
    │   │   ├── lessons-learned/
    │   │   └── documentation/
    │   ├── intuit-engine/
    │   │   ├── lessons-learned/
    │   │   └── documentation/
    │   └── hhl-site/
    │       ├── lessons-learned/
    │       └── documentation/
    ├── company/                        # Company-wide documentation
    │   ├── processes/
    │   │   ├── onboarding.md
    │   │   ├── deployment.md
    │   │   └── code-review.md
    │   ├── standards/
    │   │   ├── python-style-guide.md
    │   │   ├── api-design.md
    │   │   └── security.md
    │   └── tools/
    │       ├── gitea-guide.md
    │       ├── wikijs-guide.md
    │       └── claude-plugins.md
    └── shared/                         # Cross-project resources
        ├── architecture-patterns/
        │   ├── microservices.md
        │   ├── api-gateway.md
        │   └── database-per-service.md
        ├── best-practices/
        │   ├── error-handling.md
        │   ├── logging.md
        │   └── testing.md
        └── tech-stack/
            ├── python-ecosystem.md
            ├── docker.md
            └── ci-cd.md
```

---

## Configuration Architecture

### System-Level Configuration

**File: `~/.config/claude/gitea.env`**
```bash
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_gitea_token_here
GITEA_OWNER=hyperhivelabs
```

**File: `~/.config/claude/wikijs.env`**
```bash
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_wikijs_token_here
WIKIJS_BASE_PATH=/hyper-hive-labs
```

**Why separate files?**
- Different services, different authentication
- Can update one without affecting the other
- Clear separation of concerns
- Easier to revoke/rotate tokens per service

### Project-Level Configuration

**File: `project-root/.env`**
```bash
# Gitea repository name
GITEA_REPO=cuisineflow

# Wiki.js project path (relative to /hyper-hive-labs)
WIKIJS_PROJECT=projects/cuisineflow
```

**Path Resolution:**
- Full Wiki.js path = `{WIKIJS_BASE_PATH}/{WIKIJS_PROJECT}`
- For cuisineflow: `/hyper-hive-labs/projects/cuisineflow`
- For intuit-engine: `/hyper-hive-labs/projects/intuit-engine`

### PMO Configuration (No Project Scope)

**PMO operates at company level:**
- **Gitea**: No `GITEA_REPO` → accesses all repos
- **Wiki.js**: No `WIKIJS_PROJECT` → accesses entire `/hyper-hive-labs` namespace

---

## Plugin Structure

### Repository Structure (CORRECT)

```
hyperhivelabs/claude-plugins/
├── mcp-servers/               # SHARED by both plugins
│   ├── gitea/
│   │   ├── .venv/
│   │   ├── requirements.txt
│   │   │   # anthropic-sdk>=0.18.0
│   │   │   # python-dotenv>=1.0.0
│   │   │   # requests>=2.31.0
│   │   │   # pydantic>=2.5.0
│   │   ├── .env.example
│   │   ├── mcp_server/
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   ├── config.py
│   │   │   ├── gitea_client.py
│   │   │   └── tools/
│   │   │       ├── issues.py
│   │   │       └── labels.py
│   │   └── tests/
│   │       ├── test_config.py
│   │       ├── test_gitea_client.py
│   │       └── test_tools.py
│   └── wikijs/
│       ├── .venv/
│       ├── requirements.txt
│       │   # anthropic-sdk>=0.18.0
│       │   # python-dotenv>=1.0.0
│       │   # gql>=3.4.0
│       │   # aiohttp>=3.9.0
│       │   # pydantic>=2.5.0
│       ├── .env.example
│       ├── mcp_server/
│       │   ├── __init__.py
│       │   ├── server.py
│       │   ├── config.py
│       │   ├── wikijs_client.py
│       │   └── tools/
│       │       ├── pages.py
│       │       ├── lessons_learned.py
│       │       └── documentation.py
│       └── tests/
│           ├── test_config.py
│           ├── test_wikijs_client.py
│           └── test_tools.py
├── projman/                   # Project plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── .mcp.json              # Points to ../mcp-servers/
│   ├── commands/
│   │   ├── sprint-plan.md
│   │   ├── sprint-start.md
│   │   ├── sprint-status.md
│   │   ├── sprint-close.md
│   │   └── labels-sync.md
│   ├── agents/
│   │   ├── planner.md
│   │   ├── orchestrator.md
│   │   └── executor.md
│   ├── skills/
│   │   └── label-taxonomy/
│   │       └── labels-reference.md
│   ├── README.md
│   └── CONFIGURATION.md
└── projman-pmo/               # PMO plugin
    ├── .claude-plugin/
    │   └── plugin.json
    ├── .mcp.json              # Points to ../mcp-servers/
    ├── commands/
    │   ├── pmo-status.md
    │   ├── pmo-priorities.md
    │   ├── pmo-dependencies.md
    │   └── pmo-schedule.md
    ├── agents/
    │   └── pmo-coordinator.md
    └── README.md
```

---

## MCP Configuration Files

### projman .mcp.json (Project-Scoped)

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

### projman-pmo .mcp.json (Company-Wide)

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

**Critical Notes:**
- Both plugins reference `../mcp-servers/` (shared location at repository root)
- **projman**: Includes `GITEA_REPO` and `WIKIJS_PROJECT` for project-scoped operations
- **projman-pmo**: Omits project-specific variables for company-wide operations

---

## Wiki.js MCP Server Implementation

### Configuration Loader

```python
# mcp-wikijs/mcp_server/config.py
from pathlib import Path
from dotenv import load_dotenv
import os
from typing import Dict, Optional

class WikiJSConfig:
    """Hybrid configuration loader for Wiki.js"""
    
    def __init__(self):
        self.api_url: Optional[str] = None
        self.api_token: Optional[str] = None
        self.base_path: Optional[str] = None
        self.project_path: Optional[str] = None
        self.full_path: Optional[str] = None
    
    def load(self) -> Dict[str, str]:
        """
        Load Wiki.js configuration from system and project levels.
        Composes full path from base_path + project_path.
        """
        # Load system config
        system_config = Path.home() / '.config' / 'claude' / 'wikijs.env'
        if system_config.exists():
            load_dotenv(system_config)
        else:
            raise FileNotFoundError(
                f"System config not found: {system_config}\n"
                "Create it with: cat > ~/.config/claude/wikijs.env"
            )
        
        # Load project config (if exists, optional for PMO)
        project_config = Path.cwd() / '.env'
        if project_config.exists():
            load_dotenv(project_config, override=True)
        
        # Extract values
        self.api_url = os.getenv('WIKIJS_API_URL')
        self.api_token = os.getenv('WIKIJS_API_TOKEN')
        self.base_path = os.getenv('WIKIJS_BASE_PATH')  # /hyper-hive-labs
        self.project_path = os.getenv('WIKIJS_PROJECT')  # projects/cuisineflow (optional)
        
        # Compose full path
        if self.project_path:
            self.full_path = f"{self.base_path}/{self.project_path}"
        else:
            # PMO mode - entire company namespace
            self.full_path = self.base_path
        
        # Validate required variables
        self._validate()
        
        return {
            'api_url': self.api_url,
            'api_token': self.api_token,
            'base_path': self.base_path,
            'project_path': self.project_path,
            'full_path': self.full_path
        }
    
    def _validate(self) -> None:
        """Validate that required configuration is present"""
        required = {
            'WIKIJS_API_URL': self.api_url,
            'WIKIJS_API_TOKEN': self.api_token,
            'WIKIJS_BASE_PATH': self.base_path
        }
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Check your ~/.config/claude/wikijs.env file"
            )
```

### GraphQL Client

```python
# mcp-wikijs/mcp_server/wikijs_client.py
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from typing import List, Dict, Optional
from .config import WikiJSConfig

class WikiJSClient:
    """Client for interacting with Wiki.js GraphQL API"""
    
    def __init__(self):
        config = WikiJSConfig()
        config_dict = config.load()
        
        self.api_url = config_dict['api_url']
        self.api_token = config_dict['api_token']
        self.base_path = config_dict['base_path']
        self.project_path = config_dict.get('project_path')
        self.full_path = config_dict['full_path']
        
        # Set up GraphQL client
        transport = AIOHTTPTransport(
            url=self.api_url,
            headers={'Authorization': f'Bearer {self.api_token}'}
        )
        self.client = Client(
            transport=transport,
            fetch_schema_from_transport=True
        )
    
    async def search_pages(
        self,
        query: str,
        path: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search pages in Wiki.js within a specific path.
        
        Args:
            query: Search query string
            path: Optional path to search within (defaults to full_path)
            tags: Optional list of tags to filter by
        """
        search_path = path or self.full_path
        
        gql_query = gql("""
            query SearchPages($query: String!, $path: String) {
                pages {
                    search(query: $query, path: $path) {
                        results {
                            id
                            path
                            title
                            description
                            tags
                            updatedAt
                        }
                    }
                }
            }
        """)
        
        result = await self.client.execute(
            gql_query,
            variable_values={'query': query, 'path': search_path}
        )
        
        pages = result['pages']['search']['results']
        
        # Filter by tags if specified
        if tags:
            pages = [
                p for p in pages
                if any(tag in p['tags'] for tag in tags)
            ]
        
        return pages
    
    async def get_page(self, path: str) -> Dict:
        """Fetch a specific page by path"""
        gql_query = gql("""
            query GetPage($path: String!) {
                pages {
                    single(path: $path) {
                        id
                        path
                        title
                        description
                        content
                        tags
                        createdAt
                        updatedAt
                    }
                }
            }
        """)
        
        result = await self.client.execute(
            gql_query,
            variable_values={'path': path}
        )
        return result['pages']['single']
    
    async def create_page(
        self,
        path: str,
        title: str,
        content: str,
        tags: List[str],
        description: str = ""
    ) -> Dict:
        """
        Create a new page in Wiki.js.
        
        Args:
            path: Full path for the page (e.g., /hyper-hive-labs/projects/cuisineflow/lessons-learned/sprints/sprint-01)
            title: Page title
            content: Page content (markdown)
            tags: List of tags
            description: Optional description
        """
        gql_mutation = gql("""
            mutation CreatePage(
                $path: String!,
                $title: String!,
                $content: String!,
                $tags: [String]!,
                $description: String
            ) {
                pages {
                    create(
                        path: $path,
                        title: $title,
                        content: $content,
                        tags: $tags,
                        description: $description,
                        isPublished: true,
                        editor: "markdown"
                    ) {
                        responseResult {
                            succeeded
                            errorCode
                            message
                        }
                        page {
                            id
                            path
                            title
                        }
                    }
                }
            }
        """)
        
        result = await self.client.execute(
            gql_mutation,
            variable_values={
                'path': path,
                'title': title,
                'content': content,
                'tags': tags,
                'description': description
            }
        )
        return result['pages']['create']
    
    async def update_page(
        self,
        page_id: int,
        content: str,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """Update existing page"""
        variables = {
            'id': page_id,
            'content': content
        }
        
        if tags is not None:
            variables['tags'] = tags
        
        gql_mutation = gql("""
            mutation UpdatePage(
                $id: Int!,
                $content: String!,
                $tags: [String]
            ) {
                pages {
                    update(
                        id: $id,
                        content: $content,
                        tags: $tags
                    ) {
                        responseResult {
                            succeeded
                            errorCode
                            message
                        }
                    }
                }
            }
        """)
        
        result = await self.client.execute(gql_mutation, variable_values=variables)
        return result['pages']['update']
    
    async def list_pages(self, path: str) -> List[Dict]:
        """List all pages within a path"""
        gql_query = gql("""
            query ListPages($path: String!) {
                pages {
                    list(path: $path, orderBy: TITLE) {
                        id
                        path
                        title
                        description
                        tags
                        updatedAt
                    }
                }
            }
        """)
        
        result = await self.client.execute(
            gql_query,
            variable_values={'path': path}
        )
        return result['pages']['list']
    
    # Lessons Learned Specific Methods
    
    async def create_lesson(
        self,
        sprint_name: str,
        lesson_content: str,
        tags: List[str]
    ) -> Dict:
        """
        Create a lessons learned document for a sprint.
        
        Args:
            sprint_name: Sprint identifier (e.g., "sprint-16-intuit-engine")
            lesson_content: Full lesson markdown content
            tags: Tags for categorization
        """
        # Compose path within project's lessons-learned/sprints/
        lesson_path = f"{self.full_path}/lessons-learned/sprints/{sprint_name}"
        title = f"Sprint {sprint_name.split('-')[1]}: {' '.join(sprint_name.split('-')[2:]).title()}"
        
        return await self.create_page(
            path=lesson_path,
            title=title,
            content=lesson_content,
            tags=tags,
            description=f"Lessons learned from {sprint_name}"
        )
    
    async def search_lessons(
        self,
        query: str,
        tags: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search lessons learned within the current project.
        
        Args:
            query: Search keywords
            tags: Optional tags to filter by
        """
        lessons_path = f"{self.full_path}/lessons-learned"
        return await self.search_pages(
            query=query,
            path=lessons_path,
            tags=tags
        )
    
    # PMO Multi-Project Methods
    
    async def search_all_projects(
        self,
        query: str,
        tags: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Search lessons across all projects (PMO mode).
        Returns results grouped by project.
        """
        all_projects_path = f"{self.base_path}/projects"
        results = await self.search_pages(
            query=query,
            path=all_projects_path,
            tags=tags
        )
        
        # Group by project
        by_project = {}
        for result in results:
            # Extract project name from path
            # e.g., "/hyper-hive-labs/projects/cuisineflow/..." -> "cuisineflow"
            path_parts = result['path'].split('/')
            if len(path_parts) >= 4:
                project = path_parts[3]
                if project not in by_project:
                    by_project[project] = []
                by_project[project].append(result)
        
        return by_project
    
    async def get_shared_docs(self, category: str) -> List[Dict]:
        """
        Access company-wide shared documentation.
        
        Args:
            category: Category within shared/ (e.g., "architecture-patterns", "best-practices")
        """
        shared_path = f"{self.base_path}/shared/{category}"
        return await self.list_pages(path=shared_path)
```

---

## MCP Tools Structure

### Gitea MCP Tools

```python
# mcp-gitea/mcp_server/tools/issues.py
class IssueTools:
    def __init__(self, gitea_client):
        self.gitea = gitea_client
    
    async def list_issues(self, state='open', labels=None):
        """List issues in current repository"""
        return await self.gitea.list_issues(state=state, labels=labels)
    
    async def get_issue(self, issue_number):
        """Get specific issue details"""
        return await self.gitea.get_issue(issue_number)
    
    async def create_issue(self, title, body, labels=None):
        """Create new issue"""
        return await self.gitea.create_issue(title, body, labels)
    
    # ... other issue tools

# mcp-gitea/mcp_server/tools/labels.py
class LabelTools:
    def __init__(self, gitea_client):
        self.gitea = gitea_client
    
    async def get_labels(self):
        """Get all labels from repository"""
        return await self.gitea.get_labels()
    
    async def suggest_labels(self, context):
        """Suggest appropriate labels based on context"""
        # Label suggestion logic using taxonomy
        pass
```

### Wiki.js MCP Tools

```python
# mcp-wikijs/mcp_server/tools/pages.py
class PageTools:
    def __init__(self, wikijs_client):
        self.wikijs = wikijs_client
    
    async def search_pages(self, query, path=None, tags=None):
        """Search Wiki.js pages"""
        return await self.wikijs.search_pages(query, path, tags)
    
    async def get_page(self, path):
        """Get specific page"""
        return await self.wikijs.get_page(path)
    
    async def create_page(self, path, title, content, tags):
        """Create new page"""
        return await self.wikijs.create_page(path, title, content, tags)
    
    # ... other page tools

# mcp-wikijs/mcp_server/tools/lessons_learned.py
class LessonsLearnedTools:
    def __init__(self, wikijs_client):
        self.wikijs = wikijs_client
    
    async def create_lesson(self, sprint_name, content, tags):
        """Create lessons learned document"""
        return await self.wikijs.create_lesson(sprint_name, content, tags)
    
    async def search_lessons(self, query, tags=None):
        """Search past lessons"""
        return await self.wikijs.search_lessons(query, tags)
    
    async def search_all_projects(self, query, tags=None):
        """Search lessons across all projects (PMO)"""
        return await self.wikijs.search_all_projects(query, tags)
```

---

## Setup Instructions

### 1. System Configuration

```bash
# Create config directory
mkdir -p ~/.config/claude

# Create Gitea config
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_gitea_token
GITEA_OWNER=hyperhivelabs
EOF

# Create Wiki.js config
cat > ~/.config/claude/wikijs.env << EOF
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_wikijs_token
WIKIJS_BASE_PATH=/hyper-hive-labs
EOF

# Secure config files
chmod 600 ~/.config/claude/*.env
```

### 2. Project Configuration

```bash
# In each project root
cat > .env << EOF
GITEA_REPO=cuisineflow
WIKIJS_PROJECT=projects/cuisineflow
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

### 3. Install MCP Servers

```bash
# Gitea MCP Server
cd /path/to/claude-plugins/mcp-servers/gitea
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Wiki.js MCP Server
cd /path/to/claude-plugins/mcp-servers/wikijs
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Initialize Wiki.js Structure

Create the base structure in Wiki.js web interface:
1. Navigate to https://wiki.hyperhivelabs.com
2. Create `/hyper-hive-labs` page
3. Create `/hyper-hive-labs/projects` page
4. Create `/hyper-hive-labs/company` page
5. Create `/hyper-hive-labs/shared` page

Or use the Wiki.js API:
```python
# One-time setup script
import asyncio
from wikijs_client import WikiJSClient

async def initialize_wiki_structure():
    client = WikiJSClient()
    
    # Create base pages
    await client.create_page(
        path="/hyper-hive-labs",
        title="Hyper Hive Labs",
        content="# Hyper Hive Labs Documentation",
        tags=["company"]
    )
    
    await client.create_page(
        path="/hyper-hive-labs/projects",
        title="Projects",
        content="# Project Documentation",
        tags=["projects"]
    )
    
    # ... create other base pages

asyncio.run(initialize_wiki_structure())
```

---

## Benefits of This Architecture

### 1. Separation of Concerns
- **Gitea MCP**: Project tracking, issues, labels
- **Wiki.js MCP**: Knowledge management, documentation

### 2. Independent Configuration
- Update Gitea credentials without affecting Wiki.js
- Different token expiration policies
- Independent service availability

### 3. Better Documentation Features
- Wiki.js rich editor
- Built-in search and indexing
- Tag system
- Version history
- Access control
- Web-based review and editing

### 4. Company-Wide Knowledge Base
- Shared documentation accessible to all projects
- Cross-project lesson learning
- Best practices repository
- Onboarding materials
- Technical standards

### 5. Scalability
- Add new projects easily
- Grow company documentation organically
- PMO has visibility across everything
- Individual projects stay focused

---

## Migration from Single MCP

If you have existing Wiki content in Git:

```python
# Migration script
import asyncio
from wikijs_client import WikiJSClient
from pathlib import Path

async def migrate_lessons_to_wikijs():
    """Migrate existing lessons learned from Git to Wiki.js"""
    client = WikiJSClient()
    
    # Read existing markdown files
    lessons_dir = Path("wiki/lessons-learned/sprints")
    
    for lesson_file in lessons_dir.glob("*.md"):
        content = lesson_file.read_text()
        sprint_name = lesson_file.stem
        
        # Extract tags from content (e.g., from frontmatter or hashtags)
        tags = extract_tags(content)
        
        # Create in Wiki.js
        await client.create_lesson(
            sprint_name=sprint_name,
            lesson_content=content,
            tags=tags
        )
        
        print(f"Migrated: {sprint_name}")

asyncio.run(migrate_lessons_to_wikijs())
```

---

## Next Steps

1. **Set up Wiki.js instance** if not already done
2. **Create base structure** in Wiki.js
3. **Implement both MCP servers** (Phase 1.1a and 1.1b)
4. **Test configuration** with both services
5. **Migrate existing lessons** (if applicable)
6. **Start using with next sprint**

The two-MCP-server architecture provides a solid foundation for both project-level and company-wide knowledge management!