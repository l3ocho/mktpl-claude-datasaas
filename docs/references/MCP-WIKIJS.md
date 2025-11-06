# Wiki.js MCP Server Reference

## Overview

The Wiki.js MCP Server provides integration with Wiki.js for documentation management, lessons learned capture, and knowledge base operations. It's shared by both `projman` and `projman-pmo` plugins, detecting its operating mode based on environment variables.

**Location:** `mcp-servers/wikijs/` (repository root)

**Key Features:**
- Documentation page management (CRUD)
- Lessons learned capture and search
- Tag-based organization
- GraphQL API integration
- Mode detection (project-scoped vs company-wide)
- Hybrid configuration (system + project level)
- Python 3.11+ with async/await

---

## Architecture

### Mode Detection

The MCP server operates in two modes based on environment variables:

**Project Mode (projman):**
- When `WIKIJS_PROJECT` is present
- Operates within project path: `/hyper-hive-labs/projects/cuisineflow`
- Used by projman plugin

**Company Mode (pmo):**
- When `WIKIJS_PROJECT` is absent
- Operates on entire namespace: `/hyper-hive-labs`
- Used by projman-pmo plugin

```python
# mcp-servers/wikijs/mcp_server/config.py
def load(self):
    # ... load configs ...

    self.base_path = os.getenv('WIKIJS_BASE_PATH')  # /hyper-hive-labs
    self.project_path = os.getenv('WIKIJS_PROJECT')  # projects/cuisineflow (optional)

    # Compose full path
    if self.project_path:
        self.full_path = f"{self.base_path}/{self.project_path}"
        self.mode = 'project'
    else:
        self.full_path = self.base_path
        self.mode = 'company'

    return {
        'api_url': self.api_url,
        'api_token': self.api_token,
        'base_path': self.base_path,
        'project_path': self.project_path,
        'full_path': self.full_path,
        'mode': self.mode
    }
```

---

## Wiki.js Structure

### Company-Wide Organization

```
Wiki.js: https://wiki.hyperhivelabs.com
└── /hyper-hive-labs/                  # Base path
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

### Path Resolution

**Project Mode (projman):**
- Full path = `{WIKIJS_BASE_PATH}/{WIKIJS_PROJECT}`
- Example: `/hyper-hive-labs/projects/cuisineflow`

**Company Mode (pmo):**
- Full path = `{WIKIJS_BASE_PATH}`
- Example: `/hyper-hive-labs`

---

## Configuration

### System-Level Configuration

**File:** `~/.config/claude/wikijs.env`

```bash
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_wikijs_token
WIKIJS_BASE_PATH=/hyper-hive-labs
```

**Setup:**
```bash
# Create config directory
mkdir -p ~/.config/claude

# Create wikijs.env
cat > ~/.config/claude/wikijs.env << EOF
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_token
WIKIJS_BASE_PATH=/hyper-hive-labs
EOF

# Secure the file
chmod 600 ~/.config/claude/wikijs.env
```

### Project-Level Configuration

**File:** `project-root/.env`

```bash
# Wiki.js project path (relative to base path)
WIKIJS_PROJECT=projects/cuisineflow
```

**Setup:**
```bash
# In each project root
echo "WIKIJS_PROJECT=projects/cuisineflow" >> .env

# Add to .gitignore (if not already)
echo ".env" >> .gitignore
```

### Configuration Loading Strategy

```python
# mcp-servers/wikijs/mcp_server/config.py
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
        self.mode: str = 'project'

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
            self.mode = 'project'
        else:
            # PMO mode - entire company namespace
            self.full_path = self.base_path
            self.mode = 'company'

        # Validate required variables
        self._validate()

        return {
            'api_url': self.api_url,
            'api_token': self.api_token,
            'base_path': self.base_path,
            'project_path': self.project_path,
            'full_path': self.full_path,
            'mode': self.mode
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

---

## Directory Structure

```
mcp-servers/wikijs/
├── .venv/                      # Python virtual environment
├── requirements.txt            # Python dependencies
├── .env.example               # Configuration template
├── mcp_server/
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   ├── config.py              # Configuration loader
│   ├── wikijs_client.py       # GraphQL client
│   └── tools/
│       ├── __init__.py
│       ├── pages.py           # Page CRUD tools
│       ├── lessons_learned.py # Lessons learned tools
│       └── documentation.py   # Documentation tools
└── tests/
    ├── test_config.py
    ├── test_wikijs_client.py
    └── test_tools.py
```

---

## Dependencies

**File:** `mcp-servers/wikijs/requirements.txt`

```txt
anthropic-sdk>=0.18.0    # MCP SDK
python-dotenv>=1.0.0     # Environment variable loading
gql>=3.4.0               # GraphQL client for Wiki.js
aiohttp>=3.9.0           # Async HTTP
pydantic>=2.5.0          # Data validation
pytest>=7.4.3            # Testing framework
pytest-asyncio>=0.23.0   # Async testing support
```

**Installation:**
```bash
cd mcp-servers/wikijs
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## Wiki.js GraphQL Client

```python
# mcp-servers/wikijs/mcp_server/wikijs_client.py
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
        self.mode = config_dict['mode']

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
            path: Full path for the page
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

    async def update_index(
        self,
        sprint_name: str,
        tags: List[str]
    ) -> Dict:
        """
        Update lessons learned INDEX.md with new sprint entry.

        Args:
            sprint_name: Sprint identifier
            tags: Tags for categorization
        """
        index_path = f"{self.full_path}/lessons-learned/INDEX.md"

        # Get current index
        try:
            index_page = await self.get_page(index_path)
            current_content = index_page['content']
            page_id = index_page['id']
        except:
            # Index doesn't exist, create it
            current_content = "# Lessons Learned Index\n\n## By Sprint\n\n## By Tags\n"
            create_result = await self.create_page(
                path=index_path,
                title="Lessons Learned Index",
                content=current_content,
                tags=["index", "lessons-learned"],
                description="Index of all lessons learned"
            )
            page_id = create_result['page']['id']

        # Add new entry
        sprint_link = f"- [Sprint {sprint_name}](sprints/{sprint_name}) {' '.join(['#' + tag for tag in tags])}\n"

        # Insert after "## By Sprint" header
        lines = current_content.split('\n')
        insert_index = None
        for i, line in enumerate(lines):
            if line.startswith('## By Sprint'):
                insert_index = i + 1
                break

        if insert_index:
            lines.insert(insert_index, sprint_link)
            new_content = '\n'.join(lines)
        else:
            new_content = current_content + "\n" + sprint_link

        # Update index
        return await self.update_page(page_id, new_content)

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
            category: Category within shared/ (e.g., "architecture-patterns")
        """
        shared_path = f"{self.base_path}/shared/{category}"
        return await self.list_pages(path=shared_path)

    async def create_pattern_doc(
        self,
        pattern_name: str,
        content: str,
        tags: List[str]
    ) -> Dict:
        """
        Create a pattern document in shared/architecture-patterns.

        Args:
            pattern_name: Pattern identifier (e.g., "service-extraction")
            content: Pattern documentation (markdown)
            tags: Tags for categorization
        """
        pattern_path = f"{self.base_path}/shared/architecture-patterns/{pattern_name}"
        title = pattern_name.replace('-', ' ').title()

        return await self.create_page(
            path=pattern_path,
            title=title,
            content=content,
            tags=tags,
            description=f"Architecture pattern: {title}"
        )
```

---

## MCP Tools

### Page Management Tools

```python
# mcp-servers/wikijs/mcp_server/tools/pages.py
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

    async def update_page(self, page_id, content, tags=None):
        """Update existing page"""
        return await self.wikijs.update_page(page_id, content, tags)

    async def list_pages(self, path):
        """List all pages within a path"""
        return await self.wikijs.list_pages(path)
```

### Lessons Learned Tools

```python
# mcp-servers/wikijs/mcp_server/tools/lessons_learned.py
class LessonsLearnedTools:
    def __init__(self, wikijs_client):
        self.wikijs = wikijs_client

    async def create_lesson(self, sprint_name, content, tags):
        """
        Create lessons learned document.

        Args:
            sprint_name: Sprint identifier
            content: Lesson content (markdown)
            tags: Categorization tags
        """
        result = await self.wikijs.create_lesson(sprint_name, content, tags)

        # Update index
        await self.wikijs.update_index(sprint_name, tags)

        return result

    async def search_lessons(self, query, tags=None):
        """
        Search past lessons within current project.

        Args:
            query: Search keywords
            tags: Optional tag filters
        """
        return await self.wikijs.search_lessons(query, tags)

    async def search_all_projects(self, query, tags=None):
        """
        Search lessons across all projects (PMO mode).

        Args:
            query: Search keywords
            tags: Optional tag filters

        Returns:
            Dict keyed by project name
        """
        if self.wikijs.mode != 'company':
            raise ValueError("search_all_projects only available in company mode")

        return await self.wikijs.search_all_projects(query, tags)

    async def get_lessons_by_tag(self, tag):
        """Retrieve all lessons with a specific tag"""
        return await self.wikijs.search_lessons(
            query="*",
            tags=[tag]
        )
```

### Documentation Tools

```python
# mcp-servers/wikijs/mcp_server/tools/documentation.py
class DocumentationTools:
    def __init__(self, wikijs_client):
        self.wikijs = wikijs_client

    async def create_architecture_doc(self, name, content, tags):
        """Create architecture documentation"""
        doc_path = f"{self.wikijs.full_path}/documentation/architecture/{name}"
        return await self.wikijs.create_page(
            path=doc_path,
            title=name.replace('-', ' ').title(),
            content=content,
            tags=tags
        )

    async def create_api_doc(self, name, content, tags):
        """Create API documentation"""
        doc_path = f"{self.wikijs.full_path}/documentation/api/{name}"
        return await self.wikijs.create_page(
            path=doc_path,
            title=name.replace('-', ' ').title(),
            content=content,
            tags=tags
        )

    async def get_shared_patterns(self):
        """Get company-wide architecture patterns"""
        return await self.wikijs.get_shared_docs("architecture-patterns")

    async def get_shared_best_practices(self):
        """Get company-wide best practices"""
        return await self.wikijs.get_shared_docs("best-practices")

    async def create_pattern(self, pattern_name, content, tags):
        """
        Create shared architecture pattern (PMO mode).

        Args:
            pattern_name: Pattern identifier
            content: Pattern documentation
            tags: Categorization tags
        """
        if self.wikijs.mode != 'company':
            raise ValueError("create_pattern only available in company mode")

        return await self.wikijs.create_pattern_doc(pattern_name, content, tags)
```

---

## Lessons Learned Workflow

### Lesson Template

```markdown
# Sprint [Number]: [Name] - Lessons Learned

**Date:** [Date]
**Issue:** #[number]
**Sprint Duration:** [X weeks]

## Summary

Brief overview of what was accomplished and major outcomes.

## What Went Wrong

- **Issue 1:** Description and impact
  - **Root Cause:** Why it happened
  - **Prevention:** How to avoid in future

- **Issue 2:** ...

## What Worked Well

- **Success 1:** What worked and why
  - **Replication:** How to repeat this success

- **Success 2:** ...

## Claude Code Issues

- **Loop 1:** Description of infinite loop or blocking issue
  - **Trigger:** What caused it
  - **Resolution:** How it was fixed
  - **Prevention:** How to avoid

## Architecture Insights

- **Decision 1:** Architectural decision made
  - **Rationale:** Why this approach
  - **Trade-offs:** What was compromised

- **Insight 1:** Technical learning
  - **Application:** Where else this applies

## Action Items

- [ ] Task 1
- [ ] Task 2

## Tags

#service-extraction #api #refactoring #claude-code-loops
```

### Capture Flow

```
User: /sprint-close

Agent: Let's capture lessons learned...

       What went wrong that we should avoid next time?
User: [Response]

Agent: What decisions worked really well?
User: [Response]

Agent: Were there any Claude Code issues that caused loops/blocks?
User: [Response]

Agent: Any architectural insights for similar future work?
User: [Response]

Agent: I'll create a lesson in Wiki.js:
       Path: /hyper-hive-labs/projects/cuisineflow/lessons-learned/sprints/sprint-16-intuit-engine

       Tags detected:
       #service-extraction #api #refactoring #claude-code-loops

       Creating page in Wiki.js... ✅
       Updating INDEX.md... ✅

       View at: https://wiki.hyperhivelabs.com/hyper-hive-labs/projects/cuisineflow/lessons-learned/sprints/sprint-16-intuit-engine
```

---

## Testing

### Unit Tests

```python
# tests/test_config.py
import pytest
from pathlib import Path
from mcp_server.config import WikiJSConfig

def test_load_system_config(tmp_path, monkeypatch):
    """Test loading system-level configuration"""
    config_dir = tmp_path / '.config' / 'claude'
    config_dir.mkdir(parents=True)

    config_file = config_dir / 'wikijs.env'
    config_file.write_text(
        "WIKIJS_API_URL=https://wiki.test.com/graphql\n"
        "WIKIJS_API_TOKEN=test_token\n"
        "WIKIJS_BASE_PATH=/test-base\n"
    )

    monkeypatch.setenv('HOME', str(tmp_path))

    config = WikiJSConfig()
    result = config.load()

    assert result['api_url'] == 'https://wiki.test.com/graphql'
    assert result['api_token'] == 'test_token'
    assert result['base_path'] == '/test-base'
    assert result['mode'] == 'company'  # No project specified

def test_project_config_path_composition(tmp_path, monkeypatch):
    """Test path composition with project config"""
    system_config_dir = tmp_path / '.config' / 'claude'
    system_config_dir.mkdir(parents=True)

    system_config = system_config_dir / 'wikijs.env'
    system_config.write_text(
        "WIKIJS_API_URL=https://wiki.test.com/graphql\n"
        "WIKIJS_API_TOKEN=test_token\n"
        "WIKIJS_BASE_PATH=/hyper-hive-labs\n"
    )

    project_dir = tmp_path / 'project'
    project_dir.mkdir()

    project_config = project_dir / '.env'
    project_config.write_text("WIKIJS_PROJECT=projects/cuisineflow\n")

    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(project_dir)

    config = WikiJSConfig()
    result = config.load()

    assert result['project_path'] == 'projects/cuisineflow'
    assert result['full_path'] == '/hyper-hive-labs/projects/cuisineflow'
    assert result['mode'] == 'project'
```

### Integration Tests

```python
# tests/test_wikijs_client.py
import pytest
import asyncio
from mcp_server.wikijs_client import WikiJSClient

@pytest.fixture
def wikijs_client():
    """Fixture providing configured Wiki.js client"""
    return WikiJSClient()

@pytest.mark.asyncio
async def test_search_pages(wikijs_client):
    """Test searching pages in Wiki.js"""
    results = await wikijs_client.search_pages(query="test")
    assert isinstance(results, list)

@pytest.mark.asyncio
async def test_create_lesson(wikijs_client):
    """Test creating a lessons learned document"""
    lesson = await wikijs_client.create_lesson(
        sprint_name="sprint-99-test",
        lesson_content="# Test Lesson\n\nTest content",
        tags=["test", "sprint-99"]
    )

    assert lesson['responseResult']['succeeded']
    assert lesson['page']['title'].startswith("Sprint 99")

@pytest.mark.asyncio
async def test_search_lessons(wikijs_client):
    """Test searching lessons learned"""
    results = await wikijs_client.search_lessons(
        query="service extraction",
        tags=["refactoring"]
    )

    assert isinstance(results, list)
    for result in results:
        assert "refactoring" in result['tags']

@pytest.mark.asyncio
async def test_pmo_search_all_projects():
    """Test PMO mode cross-project search"""
    client = WikiJSClient()  # Should detect company mode

    if client.mode == 'company':
        results = await client.search_all_projects(
            query="authentication",
            tags=["security"]
        )

        assert isinstance(results, dict)
        # Results should be grouped by project
        for project_name, lessons in results.items():
            assert isinstance(lessons, list)
```

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run async tests
pytest -v tests/test_wikijs_client.py

# Run with coverage
pytest --cov=mcp_server --cov-report=html

# Run specific test
pytest tests/test_config.py::test_project_config_path_composition
```

---

## Wiki.js Setup

### Initial Structure Creation

```python
# setup_wiki_structure.py
import asyncio
from mcp_server.wikijs_client import WikiJSClient

async def initialize_wiki_structure():
    """One-time setup script to create base Wiki.js structure"""
    client = WikiJSClient()

    # Base structure
    base_pages = [
        {
            'path': '/hyper-hive-labs',
            'title': 'Hyper Hive Labs',
            'content': '# Hyper Hive Labs Documentation\n\nCompany-wide knowledge base.',
            'tags': ['company']
        },
        {
            'path': '/hyper-hive-labs/projects',
            'title': 'Projects',
            'content': '# Project Documentation\n\nProject-specific documentation and lessons learned.',
            'tags': ['projects']
        },
        {
            'path': '/hyper-hive-labs/company',
            'title': 'Company',
            'content': '# Company Documentation\n\nProcesses, standards, and tools.',
            'tags': ['company', 'processes']
        },
        {
            'path': '/hyper-hive-labs/shared',
            'title': 'Shared Resources',
            'content': '# Shared Resources\n\nArchitecture patterns, best practices, tech stack.',
            'tags': ['shared', 'resources']
        }
    ]

    for page_data in base_pages:
        try:
            result = await client.create_page(**page_data)
            print(f"Created: {page_data['path']}")
        except Exception as e:
            print(f"Error creating {page_data['path']}: {e}")

if __name__ == '__main__':
    asyncio.run(initialize_wiki_structure())
```

---

## Migration from Git-based Wiki

```python
# migrate_to_wikijs.py
import asyncio
from pathlib import Path
from mcp_server.wikijs_client import WikiJSClient
import re

async def migrate_lessons_to_wikijs():
    """Migrate existing lessons learned from Git to Wiki.js"""
    client = WikiJSClient()

    # Read existing markdown files
    lessons_dir = Path("wiki/lessons-learned/sprints")

    for lesson_file in lessons_dir.glob("*.md"):
        content = lesson_file.read_text()
        sprint_name = lesson_file.stem

        # Extract tags from content (hashtags at end)
        tags = extract_tags_from_content(content)

        # Create in Wiki.js
        try:
            await client.create_lesson(
                sprint_name=sprint_name,
                lesson_content=content,
                tags=tags
            )
            print(f"Migrated: {sprint_name}")
        except Exception as e:
            print(f"Error migrating {sprint_name}: {e}")

def extract_tags_from_content(content: str) -> List[str]:
    """Extract hashtags from markdown content"""
    # Find all hashtags
    hashtag_pattern = r'#([\w-]+)'
    matches = re.findall(hashtag_pattern, content)

    # Remove duplicates and return
    return list(set(matches))

if __name__ == '__main__':
    asyncio.run(migrate_lessons_to_wikijs())
```

---

## Benefits of Wiki.js Integration

### 1. Superior Documentation Features

- Rich markdown editor
- Built-in search and indexing
- Tag system
- Version history
- Access control
- Web-based review and editing
- GraphQL API

### 2. Company-Wide Knowledge Base

- Shared documentation accessible to all projects
- Cross-project lesson learning
- Best practices repository
- Onboarding materials
- Technical standards

### 3. Better Collaboration

- Web interface for team review
- Comments and discussions
- Version control with history
- Role-based access
- Easy sharing with stakeholders

### 4. Scalability

- Add new projects easily
- Grow company documentation organically
- PMO has visibility across everything
- Individual projects stay focused
- Search across all content

---

## Troubleshooting

### Common Issues

**Issue:** GraphQL authentication failing
```bash
# Solution: Test token manually
curl -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ pages { list { id title } } }"}' \
  https://wiki.hyperhivelabs.com/graphql
```

**Issue:** Path not found
```bash
# Solution: Verify base structure exists
# Check in Wiki.js web interface that /hyper-hive-labs path exists
```

**Issue:** Tags not working
```bash
# Solution: Ensure tags are provided as list of strings
tags = ["tag1", "tag2"]  # Correct
tags = "tag1,tag2"        # Wrong
```

**Issue:** PMO mode search returns nothing
```bash
# Solution: Ensure WIKIJS_PROJECT is NOT set
# Check environment variables
env | grep WIKIJS
```

---

## Security

### Best Practices

1. **Token Storage:**
   - Store tokens in `~/.config/claude/wikijs.env`
   - Set file permissions to 600
   - Never commit tokens to git

2. **Content Validation:**
   - Sanitize user input before creating pages
   - Validate markdown content
   - Prevent XSS in page content

3. **Access Control:**
   - Use Wiki.js role-based permissions
   - Limit API token permissions
   - Audit access logs

---

## Next Steps

1. **Set up Wiki.js instance** (if not already done)
2. **Create base structure** using setup script
3. **Configure system and project configs**
4. **Test GraphQL connectivity**
5. **Migrate existing lessons** (if applicable)
6. **Integrate with projman plugin**
