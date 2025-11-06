# ProjMan Plugin Suite - Implementation Plan

**Plugins:** `projman` (single-repo) + `projman-pmo` (multi-project)
**Build Order:** projman first, then projman-pmo
**Label System:** Type/Refactor now implemented at organization level
**Configuration:** Hybrid approach (system + project level)
**Technology Stack:** Python (MCP server), Markdown (commands/agents)

> **⚠️ IMPORTANT:** For the definitive, authoritative repository structure, always refer to [CORRECT-ARCHITECTURE.md](./CORRECT-ARCHITECTURE.md). If this document conflicts with CORRECT-ARCHITECTURE.md, CORRECT-ARCHITECTURE.md is correct.

---

## Configuration Architecture

### Two MCP Server Design (Shared Codebase)

**Architecture Decision:**
Both plugins (projman and projman-pmo) **share the same MCP server codebase**. The MCP servers detect their mode (project-scoped vs company-wide) based on environment variables.

**Separation of Concerns:**
- **Gitea MCP Server**: Issues, labels, repository data
- **Wiki.js MCP Server**: Documentation, lessons learned, knowledge base

**Repository Structure:**
```
hyperhivelabs/claude-plugins/
├── mcp-servers/              # Shared by both plugins
│   ├── gitea/
│   └── wikijs/
├── projman/                  # Project plugin
└── projman-pmo/              # PMO plugin
```

**Benefits:**
✅ Single source of truth - fix bugs once, both plugins benefit  
✅ Less code duplication and maintenance  
✅ MCP servers already handle both modes  
✅ Independent service configuration (Gitea vs Wiki.js)  
✅ Can enable/disable each service independently  
✅ Wiki.js shared across entire company (not just projects)  
✅ Easier to maintain and debug  
✅ Professional architecture  

### System-Level Configuration (Shared)

**Gitea Configuration:**  
**Location:** `~/.config/claude/gitea.env`

```bash
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_gitea_token
GITEA_OWNER=hyperhivelabs
```

**Wiki.js Configuration:**  
**Location:** `~/.config/claude/wikijs.env`

```bash
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_wikijs_token
WIKIJS_BASE_PATH=/hyper-hive-labs
```

**Used by:** Both projman and pmo plugins

### Project-Level Configuration

**Location:** `project-root/.env`

**Contains:**
```bash
# Gitea repository name
GITEA_REPO=cuisineflow

# Wiki.js project path (relative to /hyper-hive-labs)
WIKIJS_PROJECT=projects/cuisineflow
```

**Used by:** projman plugin only (pmo operates across all repos/projects)

### Wiki.js Structure

```
Wiki.js
└── hyper-hive-labs/
    ├── projects/                    # Project-specific documentation
    │   ├── cuisineflow/
    │   │   ├── lessons-learned/
    │   │   │   ├── sprints/
    │   │   │   └── INDEX.md
    │   │   └── documentation/
    │   │       ├── architecture/
    │   │       └── api/
    │   ├── cuisineflow-site/
    │   │   ├── lessons-learned/
    │   │   └── documentation/
    │   ├── intuit-engine/
    │   │   ├── lessons-learned/
    │   │   └── documentation/
    │   └── hhl-site/
    │       ├── lessons-learned/
    │       └── documentation/
    ├── company/                     # Company-wide documentation
    │   ├── processes/
    │   ├── onboarding/
    │   ├── standards/
    │   └── tools/
    └── shared/                      # Cross-project resources
        ├── architecture-patterns/
        ├── best-practices/
        └── tech-stack/
```

**Path Resolution:**
- **projman**: `{WIKIJS_BASE_PATH}/{WIKIJS_PROJECT}` → `/hyper-hive-labs/projects/cuisineflow`
- **projman-pmo**: `{WIKIJS_BASE_PATH}` → `/hyper-hive-labs` (entire company namespace)

### Benefits

✅ Single token per service - update once  
✅ Project isolation - each repo declares its paths  
✅ Company-wide documentation accessible  
✅ PMO can see all projects  
✅ Shared resources available to all  
✅ Security - tokens never committed  
✅ Portability - same system config for all projects  
✅ Scalable - easy to add new projects

---

## Phase 1: Core Infrastructure (projman)

### 1.1 MCP Server Foundation (Shared Infrastructure)

**Deliverable:** Two working MCP servers (Gitea and Wiki.js) with hybrid configuration, shared by both projman and projman-pmo plugins

**Important:** These MCP servers are built ONCE and shared by both plugins. They detect their operating mode (project-scoped vs company-wide) based on environment variables.

---

#### 1.1a Gitea MCP Server

**Tasks:**

**Configuration Setup:**
- Design environment variable loading strategy:
  - System-level: `~/.config/claude/gitea.env`
  - Project-level: `project-root/.env`
  - Merge strategy: project overrides system
- Create `.env.example` template
- Document configuration precedence rules
- Add validation for required variables

**MCP Server Implementation:**
- Set up Python project structure
- Create virtual environment (.venv)
- Install dependencies:
  ```
  # requirements.txt
  anthropic-sdk>=0.18.0
  python-dotenv>=1.0.0
  requests>=2.31.0
  pydantic>=2.5.0
  pytest>=7.4.3
  ```
- Implement Gitea API authentication
- Create environment variable loader:
  ```python
  # config.py
  from pathlib import Path
  from dotenv import load_dotenv
  import os
  
  def load_config():
      """Load configuration from system and project levels"""
      # Load system config
      system_config = Path.home() / '.config' / 'claude' / 'gitea.env'
      if system_config.exists():
          load_dotenv(system_config)
      
      # Load project config (overrides system)
      project_config = Path.cwd() / '.env'
      if project_config.exists():
          load_dotenv(project_config, override=True)
      
      # Validate required variables
      required = ['GITEA_API_URL', 'GITEA_API_TOKEN', 'GITEA_OWNER']
      missing = [var for var in required if not os.getenv(var)]
      if missing:
          raise ValueError(f"Missing config: {', '.join(missing)}")
      
      return {
          'api_url': os.getenv('GITEA_API_URL'),
          'api_token': os.getenv('GITEA_API_TOKEN'),
          'owner': os.getenv('GITEA_OWNER'),
          'repo': os.getenv('GITEA_REPO')  # Optional for PMO
      }
  ```
- Validate all required variables present
- Create 7 core tools:
  - `list_issues` - Query issues with filters
  - `get_issue` - Fetch single issue details
  - `create_issue` - Create new issue with labels
  - `update_issue` - Modify existing issue
  - `add_comment` - Add comments to issues
  - `get_labels` - Fetch org + repo label taxonomy
  - `suggest_labels` - Analyze context and suggest appropriate labels

**Testing:**
- Write integration tests against actual Gitea instance
- Test configuration loading from both levels
- Test missing configuration error handling
- Test API authentication with loaded credentials

**Success Criteria:**
- Configuration loads from both system and project levels
- Missing variables produce clear error messages
- All tools pass integration tests
- Label suggestion correctly identifies Type/Refactor
- Error handling for network failures and API rate limits

---

#### 1.1b Wiki.js MCP Server

**Tasks:**

**Configuration Setup:**
- Design environment variable loading strategy:
  - System-level: `~/.config/claude/wikijs.env`
  - Project-level: `project-root/.env`
  - Path composition: `{BASE_PATH}/{PROJECT_PATH}`
- Create `.env.example` template
- Document path resolution rules
- Add validation for required variables

**MCP Server Implementation:**
- Set up Python project structure (separate from Gitea MCP)
- Create virtual environment (.venv)
- Install dependencies:
  ```
  # requirements.txt
  anthropic-sdk>=0.18.0
  python-dotenv>=1.0.0
  gql>=3.4.0              # GraphQL client for Wiki.js
  aiohttp>=3.9.0          # Async HTTP
  pydantic>=2.5.0
  pytest>=7.4.3
  pytest-asyncio>=0.23.0
  ```
- Implement Wiki.js GraphQL authentication
- Create environment variable loader:
  ```python
  # config.py
  from pathlib import Path
  from dotenv import load_dotenv
  import os
  
  def load_config():
      """Load Wiki.js configuration from system and project levels"""
      # Load system config
      system_config = Path.home() / '.config' / 'claude' / 'wikijs.env'
      if system_config.exists():
          load_dotenv(system_config)
      
      # Load project config (overrides system)
      project_config = Path.cwd() / '.env'
      if project_config.exists():
          load_dotenv(project_config, override=True)
      
      # Validate required variables
      required = ['WIKIJS_API_URL', 'WIKIJS_API_TOKEN', 'WIKIJS_BASE_PATH']
      missing = [var for var in required if not os.getenv(var)]
      if missing:
          raise ValueError(f"Missing config: {', '.join(missing)}")
      
      # Compose full path
      base_path = os.getenv('WIKIJS_BASE_PATH')  # /hyper-hive-labs
      project_path = os.getenv('WIKIJS_PROJECT')  # projects/cuisineflow
      
      full_path = f"{base_path}/{project_path}" if project_path else base_path
      
      return {
          'api_url': os.getenv('WIKIJS_API_URL'),
          'api_token': os.getenv('WIKIJS_API_TOKEN'),
          'base_path': base_path,
          'project_path': project_path,
          'full_path': full_path
      }
  ```
- Validate all required variables present
- Create 8 core tools:
  - `search_pages` - Search Wiki.js pages by keywords/tags
  - `get_page` - Fetch specific page content
  - `create_page` - Create new Wiki page
  - `update_page` - Modify existing page
  - `list_pages` - List pages in a path
  - `create_lesson` - Create lessons learned document
  - `search_lessons` - Search past lessons by tags
  - `tag_lesson` - Add tags to lessons learned

**GraphQL Client Example:**
```python
# wikijs_client.py
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class WikiJSClient:
    def __init__(self, api_url: str, api_token: str):
        transport = AIOHTTPTransport(
            url=api_url,
            headers={'Authorization': f'Bearer {api_token}'}
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
    
    async def search_pages(self, query: str, path: str = None):
        """Search pages in Wiki.js"""
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
                        }
                    }
                }
            }
        """)
        
        result = await self.client.execute(
            gql_query,
            variable_values={'query': query, 'path': path}
        )
        return result['pages']['search']['results']
    
    async def create_page(self, path: str, title: str, content: str, tags: list):
        """Create a new page in Wiki.js"""
        gql_mutation = gql("""
            mutation CreatePage($path: String!, $title: String!, $content: String!, $tags: [String]!) {
                pages {
                    create(
                        path: $path
                        title: $title
                        content: $content
                        tags: $tags
                    ) {
                        responseResult {
                            succeeded
                            errorCode
                            message
                        }
                        page {
                            id
                            path
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
                'tags': tags
            }
        )
        return result['pages']['create']
```

**Testing:**
- Write integration tests against actual Wiki.js instance
- Test configuration loading from both levels
- Test path composition and resolution
- Test GraphQL queries and mutations
- Test authentication with Wiki.js

**Success Criteria:**
- Configuration loads from both system and project levels
- Path composition works correctly
- Missing variables produce clear error messages
- All tools pass integration tests
- GraphQL queries execute successfully
- Error handling for network failures and API rate limits
- Lessons learned can be created and searched

### 1.2 Label Taxonomy System

**Deliverable:** Label reference with sync capability

**Tasks:**
- Create `skills/label-taxonomy/` directory structure
- Port `gitea-labels-reference.md` to plugin
- Document exclusive vs non-exclusive label rules
- Build label suggestion logic:
  - Type detection (Bug, Feature, Refactor, etc.)
  - Component identification from context
  - Priority inference from keywords
  - Source detection based on branch
- Create `/labels-sync` command
- Implement diff viewer for label changes
- Build interactive review workflow

**Label Sync Workflow:**
```
User: /labels-sync
Agent: Fetching labels from Gitea...
       Found 1 new label: Type/Documentation
       Found 2 modified descriptions
       
       New: Type/Documentation
       - For documentation-only changes
       - Should update suggestion logic to detect "docs", "readme"
       
       Modified: Priority/High
       - Description clarified: "Blocks sprint completion"
       
       Shall I update the local reference and suggestion rules?
User: Yes
Agent: Updated ✅
       - labels-reference.md updated
       - Suggestion logic updated
       - 43 labels now in taxonomy
```

**Success Criteria:**
- Complete 43-label taxonomy documented
- Sync command fetches live data from Gitea
- Diff detection works correctly
- Agent provides meaningful impact analysis
- Local reference stays synchronized

### 1.3 Plugin Manifest & Structure

**Deliverable:** Complete projman plugin structure

**Tasks:**
- Create `.claude-plugin/plugin.json`
- Set up repository structure:
  ```
  hyperhivelabs/claude-plugins/
  ├── mcp-servers/           # Shared by both plugins
  │   ├── gitea/
  │   │   ├── .venv/
  │   │   ├── requirements.txt
  │   │   ├── .env.example
  │   │   ├── mcp_server/
  │   │   │   ├── __init__.py
  │   │   │   ├── server.py
  │   │   │   ├── config.py      # Detects project/company mode
  │   │   │   └── gitea_client.py
  │   │   └── tests/
  │   └── wikijs/
  │       ├── .venv/
  │       ├── requirements.txt
  │       ├── .env.example
  │       ├── mcp_server/
  │       │   ├── __init__.py
  │       │   ├── server.py
  │       │   ├── config.py      # Detects project/company mode
  │       │   └── wikijs_client.py
  │       └── tests/
  ├── projman/               # Project plugin
  │   ├── .claude-plugin/
  │   │   └── plugin.json
  │   ├── .mcp.json          # References ../mcp-servers/
  │   ├── commands/
  │   │   └── (will add in Phase 2)
  │   ├── agents/
  │   │   └── (will add in Phase 3)
  │   ├── skills/
  │   │   └── label-taxonomy/
  │   │       └── labels-reference.md
  │   ├── README.md
  │   └── CONFIGURATION.md
  └── projman-pmo/           # PMO plugin
      ├── .claude-plugin/
      │   └── plugin.json
      ├── .mcp.json          # References ../mcp-servers/
      ├── commands/
      │   └── (will add in Phase 10)
      ├── agents/
      │   └── (will add in Phase 9)
      └── README.md
  ```
- Write README with installation instructions
- Create CONFIGURATION.md with hybrid config setup for both services
- Document setup steps:
  1. Create system configs (Gitea + Wiki.js)
  2. Create project .env
  3. Create virtual environments for both MCP servers (once, in mcp-servers/)
  4. Install dependencies with pip
  5. Test connections

**Mode Detection in MCP Servers:**
```python
# mcp-servers/gitea/mcp_server/config.py
class GiteaConfig:
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

**Configuration Files:**

**projman/.mcp.json:**
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

**projman-pmo/.mcp.json:**
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

**Note:** Both plugins reference `../mcp-servers/` (shared location). The MCP servers detect their mode based on which environment variables are present.

**Configuration Documentation:**

**CONFIGURATION.md structure:**
```markdown
# Configuration Setup

## System-Level (Required for all projects)

### Gitea Configuration

1. Create config directory:
   mkdir -p ~/.config/claude

2. Create gitea.env:
   cat > ~/.config/claude/gitea.env << EOF
   GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
   GITEA_API_TOKEN=your_gitea_token
   GITEA_OWNER=hyperhivelabs
   EOF

3. Secure the file:
   chmod 600 ~/.config/claude/gitea.env

### Wiki.js Configuration

1. Create wikijs.env:
   cat > ~/.config/claude/wikijs.env << EOF
   WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
   WIKIJS_API_TOKEN=your_wikijs_token
   WIKIJS_BASE_PATH=/hyper-hive-labs
   EOF

2. Secure the file:
   chmod 600 ~/.config/claude/wikijs.env

## Project-Level (Per repository)

1. Create .env in project root:
   cat > .env << EOF
   GITEA_REPO=cuisineflow
   WIKIJS_PROJECT=projects/cuisineflow
   EOF

2. Add to .gitignore:
   echo ".env" >> .gitignore

## MCP Server Setup (One-Time, Shared by Both Plugins)

### Gitea MCP Server

1. Navigate to shared MCP directory:
   cd /path/to/claude-plugins/mcp-servers/gitea

2. Create virtual environment:
   python -m venv .venv

3. Activate virtual environment:
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows

4. Install dependencies:
   pip install -r requirements.txt

### Wiki.js MCP Server

1. Navigate to Wiki.js MCP directory:
   cd /path/to/claude-plugins/mcp-servers/wikijs

2. Create virtual environment:
   python -m venv .venv

3. Activate virtual environment:
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows

4. Install dependencies:
   pip install -r requirements.txt

## Wiki.js Structure

Your Wiki.js should have this structure:

/hyper-hive-labs/
├── projects/
│   ├── cuisineflow/
│   │   ├── lessons-learned/
│   │   │   ├── sprints/
│   │   │   └── INDEX.md
│   │   └── documentation/
│   ├── intuit-engine/
│   └── hhl-site/
├── company/
│   ├── processes/
│   └── standards/
└── shared/
    └── architecture-patterns/

Create the base structure in Wiki.js before using the plugin.

## Architecture Note

Both plugins (projman and projman-pmo) share the same MCP servers.
The MCP servers detect their operating mode based on environment variables:
- Project mode: When GITEA_REPO and WIKIJS_PROJECT are present
- Company mode: When these variables are absent (PMO plugin)

## Validation

Test Gitea MCP:
python -m mcp_gitea.server --test

Test Wiki.js MCP:
python -m mcp_wikijs.server --test

Test projman plugin:
claude plugin test projman

Test projman-pmo plugin:
claude plugin test projman-pmo
```

**Success Criteria:**
- Plugin loads successfully
- MCP server starts without errors
- Documentation is clear and complete
- Configuration templates provided
- Setup can be completed in < 5 minutes

---

## Phase 2: Sprint Planning Commands (projman)

### 2.1 Sprint Plan Command

**Deliverable:** `/sprint-plan` command with planner agent integration

**Tasks:**
- Create `commands/sprint-plan.md`
- Design command parameters:
  - Sprint name/number
  - Feature description
  - Architecture considerations
- Invoke planner agent
- Handle branch detection (only create issues in development)
- Generate sprint planning document

**Command Flow:**
```
User: /sprint-plan
Agent: Let me help you plan this sprint.
       
       What are you building?
User: Extract Intuit engine into separate service
Agent: I detected architectural changes - this is Type/Refactor.
       
       Which components are affected?
       - Component/Backend
       - Component/API
       - Component/Database
       
       Should we create a Gitea issue for tracking?
User: Yes
Agent: Created issue #47 with labels:
       - Type/Refactor
       - Component/Backend
       - Component/API
       - Priority/High
       - Source/Development
       
       Generating sprint plan...
       [Sprint document generated]
```

**Success Criteria:**
- Command invokes planner agent
- Agent asks relevant clarifying questions
- Issue created with correct labels
- Sprint document generated
- Only creates issues in development branch

### 2.2 Sprint Start Command

**Deliverable:** `/sprint-start` command

**Tasks:**
- Create `commands/sprint-start.md`
- Search lessons learned Wiki
- Surface relevant past issues
- Set up sprint tracking
- Initialize issue tracking

**Command Flow:**
```
User: /sprint-start
Agent: Starting sprint...
       
       Searching lessons learned for "service extraction"...
       📚 Found 2 relevant lessons:
       - Sprint 08: Service boundary issues with shared DB
       - Sprint 12: API versioning during extraction
       
       These might be helpful for Intuit engine extraction.
       
       Ready to begin. Sprint issue: #47
```

**Success Criteria:**
- Searches lessons learned Wiki
- Surfaces relevant past experiences
- Links to sprint issue
- Provides helpful context

### 2.3 Sprint Status Command

**Deliverable:** `/sprint-status` command

**Tasks:**
- Create `commands/sprint-status.md`
- Query current sprint issue
- Show progress indicators
- List blockers
- Surface next actions

**Success Criteria:**
- Clear status overview
- Identifies blockers
- Actionable next steps
- Links to relevant issues

### 2.4 Sprint Close Command

**Deliverable:** `/sprint-close` command with lessons learned capture

**Tasks:**
- Create `commands/sprint-close.md`
- Guide retrospective questions:
  - What went wrong?
  - What worked well?
  - Any Claude Code issues?
  - Architecture insights?
- Create lessons learned document
- Update Wiki INDEX.md
- Add searchable tags
- Close sprint issue

**Retrospective Template:**
```markdown
# Sprint [Number]: [Name] - Lessons Learned

**Date:** [Date]
**Issue:** #[number]

## What Went Wrong
- [Item 1]
- [Item 2]

## What Worked Well
- [Item 1]
- [Item 2]

## Claude Code Issues
- [Item 1]
- [Item 2]

## Architecture Insights
- [Item 1]
- [Item 2]

## Tags
#service-extraction #api #refactoring #claude-code-loops
```

**Success Criteria:**
- Interactive retrospective guide
- Document created in Wiki
- INDEX.md updated with tags
- Sprint issue closed
- Lessons searchable for future sprints

---

## Phase 3: Agent System (projman)

### 3.1 Planner Agent

**Deliverable:** Sprint planning agent

**Tasks:**
- Create `agents/planner.md`
- Define agent personality:
  - Asks clarifying questions
  - Analyzes architecture impact
  - Suggests appropriate labels
  - Generates structured plans
- Design interaction patterns
- Integrate with MCP tools
- Test with various scenarios

**Agent Personality:**
```markdown
You are the Sprint Planner for Hyper Hive Labs.

Your role:
- Guide users through sprint planning
- Ask targeted questions about scope and architecture
- Detect issue types (Bug, Feature, Refactor)
- Suggest appropriate labels based on context
- Generate comprehensive sprint documents
- Consider lessons learned from past sprints

You are:
- Thorough but not overwhelming
- Architecture-aware
- Label-conscious (use Type/Refactor for architectural changes)
- Process-oriented

You always:
- Reference relevant past lessons
- Consider technical debt
- Identify cross-project impacts
- Suggest realistic scope
```

**Success Criteria:**
- Agent provides valuable planning guidance
- Questions are relevant and targeted
- Label suggestions accurate
- Sprint documents well-structured
- Integrates lessons learned effectively

### 3.2 Orchestrator Agent

**Deliverable:** Sprint coordination agent

**Tasks:**
- Create `agents/orchestrator.md`
- Define orchestration responsibilities:
  - Track sprint progress
  - Identify blockers
  - Coordinate sub-tasks
  - Surface relevant context
- Design status monitoring
- Build blocker detection logic

**Agent Personality:**
```markdown
You are the Sprint Orchestrator for Hyper Hive Labs.

Your role:
- Monitor sprint progress
- Track issue status
- Identify and surface blockers
- Coordinate between tasks
- Keep sprint on track

You are:
- Progress-focused
- Blocker-aware
- Context-provider
- Coordination-minded

You always:
- Check issue status
- Identify dependencies
- Surface relevant documentation
- Keep things moving
```

**Success Criteria:**
- Tracks progress accurately
- Identifies blockers early
- Provides useful coordination
- Reduces manual overhead

### 3.3 Executor Agent

**Deliverable:** Implementation guidance agent

**Tasks:**
- Create `agents/executor.md`
- Define implementation support:
  - Technical guidance
  - Code review
  - Testing strategy
  - Documentation
- Integrate with label taxonomy
- Reference architecture patterns

**Agent Personality:**
```markdown
You are the Sprint Executor for Hyper Hive Labs.

Your role:
- Provide implementation guidance
- Suggest code patterns
- Review technical decisions
- Ensure quality standards
- Reference best practices

You are:
- Technically detailed
- Quality-focused
- Pattern-aware
- Standards-conscious

You always:
- Follow modular architecture principles
- Suggest discrete methods/functions
- Consider testability
- Document decisions
```

**Success Criteria:**
- Provides valuable technical guidance
- Maintains quality standards
- References appropriate patterns
- Supports implementation effectively

---

## Phase 4: Lessons Learned System (projman)

### 4.1 Wiki.js Integration

**Deliverable:** Lessons learned structure in Wiki.js

**Tasks:**
- Design Wiki.js page structure within project path:
  ```
  /hyper-hive-labs/projects/cuisineflow/
  ├── lessons-learned/
  │   ├── INDEX.md                  # Searchable index
  │   ├── sprints/
  │   │   ├── sprint-01-auth.md
  │   │   ├── sprint-02-api.md
  │   │   └── ...
  │   └── patterns/
  │       ├── service-extraction.md
  │       └── database-migration.md
  └── documentation/
      ├── architecture/
      └── api/
  ```
- Create INDEX.md template
- Define tagging system using Wiki.js tags
- Build search integration using Wiki.js MCP tools

**INDEX.md Structure:**
```markdown
# CuisineFlow - Lessons Learned Index

## By Sprint
- [Sprint 01: Auth System](sprints/sprint-01-auth) #authentication #oauth #security
- [Sprint 02: API Gateway](sprints/sprint-02-api) #api #gateway #routing

## By Pattern
- [Service Extraction](patterns/service-extraction) #microservices #refactoring

## By Technology
- Authentication: Sprint 01, Sprint 08
- API Design: Sprint 02, Sprint 12
- Database: Sprint 03, Sprint 15

## By Problem
- Claude Code Loops: Sprint 04, Sprint 12, Sprint 14
- Deployment Issues: Sprint 08, Sprint 13

## Tags
#authentication #api #database #deployment #refactoring #claude-code-loops
```

**Wiki.js Advantages:**
- Rich markdown editor
- Built-in search
- Tag system
- Version history
- Access control
- Web UI for review

**Success Criteria:**
- Clear Wiki.js page structure
- Searchable index page
- Tagging system works with Wiki.js tags
- Easy to navigate via web interface
- Integrates with Git (Wiki.js can sync to Git)

### 4.2 Search Integration

**Deliverable:** Lessons learned search using Wiki.js MCP

**Tasks:**
- Use Wiki.js MCP server tools for search:
  - `search_pages` - Search by keywords/tags in project path
  - `get_page` - Fetch specific lesson document
  - `create_page` - Create new lesson
  - `update_page` - Update INDEX.md
  - `list_pages` - List all lessons in path
- Implement tag-based search using Wiki.js tags
- Build keyword matching using Wiki.js search API
- Integrate with agents

**Search Example:**
```python
# Using Wiki.js MCP tools
from mcp_wikijs import WikiJSClient

client = WikiJSClient()

# Search for service extraction lessons
results = await client.search_pages(
    query="service extraction",
    path="/hyper-hive-labs/projects/cuisineflow/lessons-learned"
)

# Filter by tags
lessons_with_tag = await client.search_pages(
    query="#refactoring",
    path="/hyper-hive-labs/projects/cuisineflow/lessons-learned"
)
```

**Success Criteria:**
- Fast search using Wiki.js search API
- Tag-based filtering works
- Relevant results surfaced
- Integrates with planning process
- Can search across all projects (for PMO)

### 4.3 Capture Workflow

**Deliverable:** Lessons learned capture during sprint close

**Tasks:**
- Integrate into `/sprint-close` command
- Guide retrospective discussion
- Generate structured markdown document
- Auto-tag based on content using Wiki.js tags
- Create page in Wiki.js via MCP
- Update INDEX.md automatically
- Use Wiki.js version control for history

**Capture Flow:**
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

**Wiki.js Page Creation:**
```python
# Using Wiki.js MCP create_page tool
await wikijs_client.create_page(
    path="/hyper-hive-labs/projects/cuisineflow/lessons-learned/sprints/sprint-16-intuit-engine",
    title="Sprint 16: Intuit Engine Extraction",
    content=lesson_markdown,
    tags=["service-extraction", "api", "refactoring", "claude-code-loops"]
)
```

**Success Criteria:**
- Guided retrospective questions
- Document created in Wiki.js
- Tags added via Wiki.js tag system
- INDEX.md updated automatically
- Viewable in Wiki.js web interface
- Version history tracked
- Searchable immediately

---

## Phase 5: Testing & Validation (projman)

### 5.1 Integration Testing

**Deliverable:** Comprehensive test suite

**Tasks:**
- Test MCP server tools:
  - Issue CRUD operations
  - Label operations
  - Wiki operations
  - Configuration loading
- Test command workflows:
  - Complete sprint lifecycle
  - Label sync
  - Lessons learned capture
- Test agent interactions:
  - Planner workflow
  - Orchestrator monitoring
  - Executor guidance
- Test configuration:
  - System-level loading
  - Project-level loading
  - Hybrid merge behavior
  - Missing config handling

**Test Matrix:**
```
| Component        | Test Coverage | Status |
|------------------|---------------|--------|
| MCP Tools        | All 10 tools  | ✅     |
| Commands         | All 5 cmds    | ✅     |
| Agents           | All 3 agents  | ✅     |
| Configuration    | All scenarios | ✅     |
| Wiki Integration | Full flow     | ✅     |
| Label System     | All labels    | ✅     |
```

**Success Criteria:**
- All tests pass
- Edge cases handled
- Error messages clear
- Configuration validation works
- Performance acceptable

### 5.2 Real Sprint Testing

**Deliverable:** Plugin validated with actual sprint

**Tasks:**
- Use plugin for Intuit engine extraction sprint
- Monitor for issues
- Collect user feedback
- Identify pain points
- Document improvements needed

**Test Sprint Checklist:**
- [ ] Sprint planning with planner agent
- [ ] Issue created with correct labels
- [ ] Lessons learned searched at start
- [ ] Status monitoring during sprint
- [ ] Blocker identification
- [ ] Sprint close with retrospective
- [ ] Wiki updated with lessons

**Success Criteria:**
- Plugin handles real sprint
- No critical bugs
- Workflow feels natural
- Saves time vs manual process
- Lessons learned captured

### 5.3 Configuration Testing

**Deliverable:** Validated hybrid configuration

**Tasks:**
- Test system config creation
- Test project config creation
- Test configuration loading order
- Test missing config scenarios:
  - No system config
  - No project config
  - Invalid credentials
  - Network issues
- Test multi-project scenarios:
  - Different repos with same system config
  - Switching between projects
  - Config changes propagation

**Test Scenarios:**
```
Scenario 1: Fresh install
- No configs exist
- Plugin guides user through setup
- All configs created correctly

Scenario 2: System config exists
- User adds new project
- Only needs project .env
- System config reused

Scenario 3: Invalid credentials
- Clear error message
- Suggests checking config
- Points to CONFIGURATION.md

Scenario 4: Multi-project
- cuisineflow project
- Switch to intuit-engine project
- Each uses correct GITEA_REPO
- Same system credentials
```

**Success Criteria:**
- Configuration works in all scenarios
- Error messages are helpful
- Setup is intuitive
- Multi-project switching seamless
- Documentation matches reality

---

## Phase 6: Documentation & Refinement (projman)

### 6.1 User Documentation

**Deliverable:** Complete user guide

**Tasks:**
- Write README.md:
  - Installation instructions
  - Configuration setup (hybrid approach)
  - Command reference
  - Agent descriptions
  - Troubleshooting
- Write CONFIGURATION.md:
  - System-level setup
  - Project-level setup
  - Validation steps
  - Common issues
- Create ARCHITECTURE.md:
  - Plugin structure
  - MCP server design
  - Configuration flow
  - Agent system
- Write CONTRIBUTING.md:
  - Development setup
  - Testing guidelines
  - Label taxonomy updates
  - Wiki maintenance

**Success Criteria:**
- Complete documentation
- Clear setup instructions
- Configuration well-explained
- Examples provided
- Troubleshooting guide

### 6.2 Iteration Based on Feedback

**Deliverable:** Refined plugin based on real use

**Tasks:**
- Address issues from test sprint
- Improve agent prompts
- Refine command flows
- Enhance error messages
- Optimize performance
- Update configuration docs if needed

**Feedback Categories:**
- Usability issues
- Missing features
- Confusing workflows
- Error handling gaps
- Documentation unclear
- Configuration complexity

**Success Criteria:**
- Major issues resolved
- Workflows improved
- Documentation updated
- Performance acceptable
- Ready for team use

---

## Phase 7: Marketplace Preparation (projman)

### 7.1 Gitea Marketplace Setup

**Deliverable:** projman available in Gitea marketplace

**Tasks:**
- Create marketplace repository in Gitea:
  - `hyperhivelabs/claude-plugins`
- Add projman plugin to repository
- Create `.claude-plugin/marketplace.json`:
  ```json
  {
    "plugins": [
      {
        "name": "projman",
        "displayName": "Project Manager",
        "description": "Single-repo project management with Gitea",
        "version": "1.0.0",
        "author": "Hyper Hive Labs",
        "repository": "hyperhivelabs/claude-plugins",
        "path": "projman"
      }
    ]
  }
  ```
- Test marketplace loading
- Document installation for team

**Installation Command:**
```bash
# Add marketplace
/plugin marketplace add https://your-gitea.com/hyperhivelabs/claude-plugins

# Install plugin
/plugin install projman
```

**Success Criteria:**
- Marketplace repository created
- Plugin available for installation
- Installation works smoothly
- Team can access plugin
- Documentation clear

### 7.2 Team Onboarding

**Deliverable:** Team trained on projman usage

**Tasks:**
- Create onboarding guide
- Walk through configuration setup:
  - System config creation
  - Project config per repo
- Demonstrate sprint workflow
- Show lessons learned capture
- Explain label system
- Share best practices

**Onboarding Checklist:**
- [ ] Configuration setup completed
- [ ] Test sprint planned
- [ ] Issue created successfully
- [ ] Labels used correctly
- [ ] Lessons learned captured
- [ ] Wiki searched successfully

**Success Criteria:**
- Team understands configuration
- Can run full sprint workflow
- Uses labels correctly
- Captures lessons learned
- Comfortable with plugin

---

## Phase 8: Production Hardening (projman)

### 8.1 Error Handling & Resilience

**Deliverable:** Production-ready error handling

**Tasks:**
- Implement comprehensive error handling:
  - Network failures
  - API rate limits
  - Authentication errors
  - Invalid configurations
  - Missing Wiki
  - Git conflicts
- Add retry logic for transient failures
- Improve error messages
- Add logging for debugging
- Create health check command

**Success Criteria:**
- Graceful failure handling
- Clear error messages
- Automatic retries where appropriate
- Logging helps debugging
- Users not blocked by errors

### 8.2 Performance Optimization

**Deliverable:** Optimized plugin performance

**Tasks:**
- Profile MCP server operations using cProfile
- Optimize API calls:
  - Batch requests where possible
  - Cache label data using lru_cache
  - Minimize Wiki searches
- Reduce startup time
- Optimize configuration loading
- Test with large repositories
- Use async/await for concurrent operations where beneficial

**Success Criteria:**
- Fast command execution
- Low latency for API calls
- Efficient caching
- Handles large repos
- Startup time < 2 seconds

### 8.3 Security Audit

**Deliverable:** Security-hardened plugin

**Tasks:**
- Review credential handling:
  - System config permissions
  - Token storage security
  - Environment variable safety
- Validate input sanitization
- Check for injection vulnerabilities
- Review error message information leakage
- Audit logging for sensitive data
- Test access controls

**Security Checklist:**
- [ ] Credentials never logged
- [ ] Config files have correct permissions
- [ ] Input validation on all user input
- [ ] No SQL/command injection vectors
- [ ] Error messages don't leak tokens
- [ ] API calls use TLS
- [ ] Token rotation supported

**Success Criteria:**
- No security vulnerabilities
- Credentials protected
- Safe input handling
- Audit clean
- Best practices followed

---

## Phase 9: PMO Plugin Foundation (projman-pmo)

### 9.1 Requirements Analysis

**Deliverable:** PMO plugin requirements document

**Tasks:**
- Analyze multi-project workflows:
  - CuisineFlow → CuisineFlow-Site sync
  - Intuit Engine → CuisineFlow integration
  - HHL-Site updates
  - Customer VPS deployments
- Identify cross-project dependencies
- Define coordination pain points
- Design PMO plugin scope
- Determine what belongs in PMO vs projman

**Key Questions:**
- What triggers demo site updates?
- What triggers Intuit engine updates?
- How do you coordinate customer VPS deployments?
- Where do multi-project conflicts happen?
- What decisions require cross-project visibility?

**Success Criteria:**
- Clear understanding of multi-project workflows
- Pain points documented
- PMO plugin scope defined
- Not duplicating single-repo functionality

### 9.2 MCP Server Extension

**Deliverable:** Multi-repo query capabilities

**Tasks:**
- Extend Gitea MCP server for multi-repo operations
- Add tools:
  - `list_repos` - Get all organization repos
  - `aggregate_issues` - Fetch issues across repos
  - `check_dependencies` - Analyze cross-repo dependencies
  - `get_deployment_status` - Check deployment states
- Build dependency graph visualization data
- Implement cross-repo search

**Configuration for PMO:**

**pmo/.mcp.json:**
```json
{
  "mcpServers": {
    "gitea-pmo": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}/mcp-server",
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/mcp-server",
        "GITEA_API_URL": "${GITEA_API_URL}",
        "GITEA_API_TOKEN": "${GITEA_API_TOKEN}",
        "GITEA_OWNER": "${GITEA_OWNER}"
      }
    }
  }
}
```

**Note:** PMO only uses system-level config (no GITEA_REPO).

**Success Criteria:**
- Can query multiple repos efficiently
- Dependency analysis works
- Aggregated views make sense
- Performance acceptable for 3-5 repos
- System-level config sufficient

### 9.3 PMO Agent Design

**Deliverable:** Multi-project coordinator agent

**Tasks:**
- Define PMO agent personality
- Design cross-project prioritization logic
- Create resource allocation algorithms
- Build conflict detection rules
- Design dependency tracking system

**PMO Agent Personality:**
```markdown
You are the PMO Coordinator for Hyper Hive Labs.

Your role:
- Maintain strategic view across all projects
- Identify cross-project dependencies
- Detect resource conflicts
- Balance competing priorities
- Coordinate release timing
- Track customer deployment schedules

You are:
- Strategic thinker
- Dependency-aware
- Conflict detector
- Priority balancer
- Team coordinator

You delegate to project-level agents:
- Don't micromanage single projects
- Focus on cross-project issues
- Surface conflicts early
- Facilitate coordination
```

**Success Criteria:**
- Clear separation from projman agents
- Valuable for multi-project scenarios
- Doesn't micromanage single projects
- Integrates with projman seamlessly

---

## Phase 10: PMO Plugin Development (projman-pmo)

### 10.1 Cross-Project Commands

**Deliverable:** PMO-specific commands

**Tasks:**
- `/pmo-status` - View all projects status
- `/pmo-priorities` - Review and adjust priorities across projects
- `/pmo-dependencies` - Visualize project dependencies
- `/pmo-conflicts` - Identify resource conflicts
- `/pmo-schedule` - View deployment schedule

**Command Examples:**

**`/pmo-status`:**
```
Projects Overview:

CuisineFlow (main)
├── Sprint: Intuit Engine Extraction
├── Status: In Progress (60%)
├── Blockers: None
└── Next: API testing

CuisineFlow-Site (demo)
├── Sprint: Dashboard Updates
├── Status: Waiting on CuisineFlow API
├── Blockers: Depends on #cuisineflow-47
└── Next: Deploy when API ready

Intuit-Engine (service)
├── Sprint: Initial Setup
├── Status: Planning
├── Blockers: Architecture decisions needed
└── Next: Service boundary definition

HHL-Site (marketing)
├── Sprint: Content Updates
├── Status: Complete
├── Blockers: None
└── Next: Deploy to production
```

**`/pmo-dependencies`:**
```
Project Dependencies:

CuisineFlow → Intuit-Engine
  ├── Must complete before v2.0 launch
  └── API contracts defined

CuisineFlow → CuisineFlow-Site
  ├── Demo must sync with main features
  └── Deploy together for consistency

Deployment Order:
1. Intuit-Engine (backend service)
2. CuisineFlow (main app)
3. CuisineFlow-Site (demo sync)
4. Customer VPS deployments
```

**Success Criteria:**
- Commands provide valuable cross-project insights
- Dependencies clearly visualized
- Conflicts easily identified
- Priorities make sense
- Schedule coordination works

### 10.2 Coordination Workflows

**Deliverable:** Multi-project coordination automation

**Tasks:**
- Implement dependency tracking
- Build conflict detection:
  - Resource conflicts
  - Timeline conflicts
  - Priority conflicts
- Create notification system for cross-project impacts
- Design release coordination workflow

**Conflict Detection Examples:**

**Resource Conflict:**
```
⚠️ Resource Conflict Detected

Leo is assigned to:
- CuisineFlow: Intuit Engine extraction (Priority: Critical)
- CuisineFlow-Site: Dashboard redesign (Priority: High)
- HHL-Site: Content update (Priority: Medium)

Recommendation: 
- Focus on Intuit Engine (blocks launch)
- Defer dashboard redesign to next sprint
- Delegate content update to marketing
```

**Timeline Conflict:**
```
⚠️ Timeline Conflict Detected

CuisineFlow v2.0 launch: Nov 15
├── Depends on: Intuit Engine completion
└── Current status: Behind schedule

Impact:
- Demo site deployment delayed
- Customer VPS updates postponed
- Marketing announcements on hold

Action needed: Re-evaluate scope or push date
```

**Success Criteria:**
- Conflicts detected automatically
- Clear recommendations provided
- Dependencies tracked accurately
- Timeline visibility maintained

### 10.3 Dashboard & Reporting

**Deliverable:** Multi-project dashboard

**Tasks:**
- Create consolidated view:
  - All active sprints
  - Cross-project dependencies
  - Resource allocation
  - Timeline status
  - Blockers across projects
- Build reporting commands:
  - `/pmo-report daily` - Daily standup report
  - `/pmo-report weekly` - Weekly progress
  - `/pmo-report release` - Release readiness
- Generate stakeholder updates

**Success Criteria:**
- Dashboard provides clear overview
- Reports are actionable
- Stakeholder communication improved
- Decision-making supported

---

## Phase 11: PMO Testing & Integration (projman-pmo)

### 11.1 Multi-Project Testing

**Deliverable:** Validated PMO plugin

**Tasks:**
- Test with CuisineFlow + CuisineFlow-Site + Intuit Engine
- Simulate deployment coordination scenarios
- Test priority conflict resolution
- Validate dependency tracking
- Test customer deployment scheduling

**Test Scenarios:**

**Scenario 1: Dependent Deploy**
```
Given: CuisineFlow has API changes
And: CuisineFlow-Site depends on those changes
When: CuisineFlow sprint completes
Then: PMO should alert about Site sync needed
And: Suggest coordinated deployment
```

**Scenario 2: Resource Conflict**
```
Given: Multiple critical priorities
And: Single developer (Leo)
When: PMO analyzes priorities
Then: Should detect conflict
And: Recommend prioritization
```

**Scenario 3: Release Coordination**
```
Given: Intuit Engine must deploy first
And: CuisineFlow depends on it
And: Demo site must sync
When: Release planned
Then: PMO generates deployment order
And: Validates dependencies satisfied
```

**Success Criteria:**
- All scenarios handled correctly
- Dependencies respected
- Conflicts detected and surfaced
- Coordination reduces manual overhead

### 11.2 Integration with projman

**Deliverable:** Seamless plugin interoperability

**Tasks:**
- Ensure PMO agent delegates to projman agents
- Test command interoperability
- Validate shared MCP server usage (if applicable)
- Check lessons learned sharing across projects
- Test configuration isolation (PMO system-only vs projman hybrid)

**Integration Points:**
```
PMO Plugin            projman Plugin
    ├─────────────────────┤
    │   Delegates         │
    │   single-project    │
    │   details           │
    │                     │
    ├─ Aggregates ────────┤
    │  cross-project      │
    │  status             │
    │                     │
    └─ Coordinates ───────┘
       dependencies
```

**Success Criteria:**
- PMO doesn't interfere with single-project work
- Delegation works smoothly
- Shared infrastructure stable (if any)
- Cross-project lessons accessible
- Configuration doesn't conflict

---

## Phase 12: Production Deployment

### 12.1 Multi-Environment Rollout

**Deliverable:** Plugins deployed across all environments

**Tasks:**
- Deploy to laptop (development)
- Deploy to staging VPS
- Deploy to production VPS
- Configure branch-aware permissions per environment
- Test network connectivity and API access
- Validate configuration in each environment

**Environment Configuration:**

**Laptop (Development):**
```bash
# System config (~/.config/claude/gitea.env)
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=dev_token
GITEA_OWNER=hyperhivelabs

# Project configs (per repo .env)
# cuisineflow/.env
GITEA_REPO=cuisineflow

# intuit-engine/.env
GITEA_REPO=intuit-engine
```

**VPS Environments:**
- Same system config copied to VPS
- Each project repo has its own .env
- MCP server runs in production mode
- Network access validated

**Success Criteria:**
- Plugins work in all environments
- Configuration portable across systems
- Network connectivity stable
- Production ready

### 12.2 Backup & Recovery

**Deliverable:** Backup and recovery procedures

**Tasks:**
- Document configuration backup:
  - System config backup
  - Project configs tracked in git
- Create Wiki backup strategy
- Document recovery procedures
- Test configuration restoration
- Automate backups where possible

**Backup Strategy:**
```bash
# System config backup
cp ~/.config/claude/gitea.env ~/.config/claude/gitea.env.backup

# Wiki is already in git
cd wiki
git push origin main

# Project configs are in .gitignore (not backed up, easily recreated)
```

**Success Criteria:**
- Configuration backup documented
- Wiki backed up regularly
- Recovery procedures tested
- Data loss risk minimized

### 12.3 Monitoring & Maintenance

**Deliverable:** Ongoing monitoring and maintenance plan

**Tasks:**
- Set up error monitoring
- Create maintenance schedule:
  - Label taxonomy updates
  - Wiki cleanup
  - Configuration audits
  - Security updates
- Document troubleshooting procedures
- Establish update process for MCP server

**Maintenance Checklist:**
- [ ] Weekly: Review error logs
- [ ] Monthly: Update Python dependencies (pip list --outdated)
- [ ] Quarterly: Security audit (pip-audit)
- [ ] As-needed: Label taxonomy sync
- [ ] As-needed: Wiki organization
- [ ] As-needed: Recreate virtual environment for major updates

**Success Criteria:**
- Monitoring in place
- Maintenance plan documented
- Update process defined
- Team knows how to maintain

---

## Rollback Plan

If plugins cause more problems than they solve:

**Immediate Fallback:**
- Keep existing skills and scripts functional
- Plugins are opt-in, not replacement
- Document issues and iterate
- Can disable plugins without losing work

**Criteria for Rollback:**
- Plugin slower than current workflow
- Frequent errors or data loss
- User frustration increases
- Blocks urgent work (like sprint deadlines)

**Progressive Enhancement:**
- Build plugins alongside current system
- Migrate piece by piece
- Keep escape hatches
- Only deprecate scripts when plugin proven

---

## Configuration Quick Reference

### System-Level Setup (Once per machine)

```bash
# Create config directory
mkdir -p ~/.config/claude

# Create gitea.env
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.hyperhivelabs.com/api/v1
GITEA_API_TOKEN=your_token_here
GITEA_OWNER=hyperhivelabs
EOF

# Set permissions
chmod 600 ~/.config/claude/gitea.env
```

### Project-Level Setup (Per repository)

```bash
# In project root
echo "GITEA_REPO=cuisineflow" > .env

# Add to .gitignore
echo ".env" >> .gitignore
```

### Validation

```bash
# Test projman configuration
cd your-project
claude plugin test projman

# Test pmo configuration (no project needed)
claude plugin test projman-pmo
```

---

## Notes on Type/Refactor Label

**Label Details:**
- **Name:** `Type/Refactor`
- **Level:** Organization (available to all repos)
- **Category:** Type/ (Exclusive - only one Type per issue)
- **Color:** #0052cc (matches other Type labels)
- **Description:** Architectural changes and code restructuring

**Usage in Plugins:**
- Planner agent suggests Type/Refactor for:
  - Service extraction (like Intuit engine)
  - Architecture modifications
  - Code restructuring without feature changes
  - Performance optimizations requiring significant changes
- Label suggestion engine detects refactor keywords:
  - "extract", "refactor", "restructure", "optimize architecture"
  - "service boundary", "microservice", "decouple"
  - "technical debt", "code quality"
- Shows in label sync diffs when fetching from Gitea
- Documented in label taxonomy skill

**Integration Points:**
- MCP server includes Type/Refactor in label enumeration
- Suggestion engine trained on architectural patterns
- Sprint planning templates include refactor considerations
- Lessons learned can tag architectural mistakes for future refactors

---

## End of Implementation Plan

This plan builds two plugins systematically, starting with single-repo project management (projman) and expanding to multi-project coordination (projman-pmo). Each phase builds on previous phases, with testing and validation throughout.

The hybrid configuration approach provides the right balance of simplicity (single token location) and flexibility (per-project repository specification).

The plan is execution-ready but flexible - adjust based on real-world feedback and discovered requirements.