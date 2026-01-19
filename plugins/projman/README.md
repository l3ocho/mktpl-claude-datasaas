# Projman v2.0.0 - Project Management for Claude Code

Sprint planning and project management plugin with full Gitea integration.

## Overview

Projman transforms a proven 15-sprint workflow into a distributable Claude Code plugin. It provides AI-guided sprint planning, intelligent issue creation with label taxonomy, native issue dependencies, parallel task execution, and systematic lessons learned capture via Gitea Wiki.

**Key Features:**
- **Sprint Planning** - AI-guided architecture analysis and issue creation
- **Smart Label Suggestions** - Intelligent label recommendations from 43-label taxonomy
- **Issue Dependencies** - Native Gitea dependencies with parallel execution batching
- **Milestones** - Sprint milestone management and tracking
- **Lessons Learned** - Systematic capture and search via Gitea Wiki
- **Branch-Aware Security** - Prevents accidental changes on production branches
- **Three-Agent Model** - Planner, Orchestrator, and Executor agents
- **CLI Tools Blocked** - All operations via MCP tools only (no `tea` or `gh`)

## Quick Start

### 1. Prerequisites

- Claude Code installed
- Access to Gitea instance with API token
- Python 3.10+ installed
- Git repository initialized

### 2. Install MCP Server

The plugin bundles the Gitea MCP server:

```bash
cd plugins/projman/mcp-servers/gitea
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

See [CONFIGURATION.md](./CONFIGURATION.md) for detailed setup instructions.

### 3. Configure System-Level Settings

Create system-wide configuration with your Gitea credentials:

```bash
mkdir -p ~/.config/claude

# Gitea configuration
cat > ~/.config/claude/gitea.env << 'EOF'
GITEA_URL=https://gitea.example.com
GITEA_TOKEN=your_gitea_token_here
GITEA_ORG=your_organization
EOF

# Secure the file
chmod 600 ~/.config/claude/gitea.env
```

### 4. Configure Project-Level Settings

In your project root directory, create a `.env` file:

```bash
# In your project directory
cat > .env << 'EOF'
GITEA_REPO=your-repo-name
EOF
```

### 5. Run Initial Setup

```bash
/initial-setup
```

### 6. Start Planning!

```bash
/sprint-plan
```

## Commands

### `/sprint-plan`
Start sprint planning with the AI planner agent.

**What it does:**
- Validates repository organization and label taxonomy
- Asks clarifying questions about sprint goals
- Searches relevant lessons learned from previous sprints
- Performs architecture analysis
- Creates Gitea issues with intelligent label suggestions
- Sets up issue dependencies for parallel execution
- Creates sprint milestone

**Pre-Planning Validations:**
1. Repository belongs to configured organization
2. Required label categories exist
3. `docs/changes/` folder exists in repository

**Task Naming:** `[Sprint XX] <type>: <description>`

**When to use:** Beginning of a new sprint or when planning a major feature

### `/sprint-start`
Begin sprint execution with the orchestrator agent.

**What it does:**
- Reviews open sprint issues and dependencies
- Batches tasks by dependency graph for parallel execution
- Generates lean execution prompts
- Tracks progress

**Parallel Execution:**
```
Batch 1 (parallel): Task A, Task B, Task C
Batch 2 (parallel): Task D, Task E  (depend on Batch 1)
Batch 3 (sequential): Task F        (depends on Batch 2)
```

**Branch Naming:** `feat/123-task-title`, `fix/456-bug-fix`, `debug/789-investigation`

**When to use:** After planning, when ready to start implementation

### `/sprint-status`
Check current sprint progress.

**What it does:**
- Lists all sprint issues by status (open, in progress, blocked, completed)
- Shows dependency analysis and blocked tasks
- Displays completion percentage
- Shows milestone progress

**When to use:** Daily standup, progress check, deciding what to work on next

### `/sprint-close`
Complete sprint and capture lessons learned.

**What it does:**
- Reviews sprint completion
- Captures lessons learned (what went wrong, what went right)
- Tags lessons for discoverability
- Saves lessons to Gitea Wiki
- Closes sprint milestone
- Handles git operations (merge, tag, cleanup)

**When to use:** End of sprint, before starting the next one

**CRITICAL:** Don't skip this! After 15 sprints without lesson capture, teams repeat the same mistakes.

### `/labels-sync`
Synchronize label taxonomy from Gitea.

**What it does:**
- Validates repository belongs to organization
- Fetches current labels from Gitea (org + repo)
- Validates required label categories
- Compares with local reference
- Updates local taxonomy reference

**When to use:**
- First-time setup
- Monthly maintenance
- When new labels are added to Gitea

### `/initial-setup`
Run initial setup for a new project.

**What it does:**
- Validates Gitea MCP server connection
- Tests credential configuration
- Syncs label taxonomy
- Creates required directory structure

**When to use:** First time setting up projman for a project

## Agents

### Planner Agent
**Personality:** Thoughtful, methodical, asks clarifying questions

**Responsibilities:**
- Pre-planning validations (org, labels, folder structure)
- Sprint planning and architecture analysis
- Asking clarifying questions before making assumptions
- Searching relevant lessons learned via Gitea Wiki
- Creating well-structured Gitea issues
- Setting up issue dependencies
- Suggesting appropriate labels based on context

**Invoked by:** `/sprint-plan`

### Orchestrator Agent
**Personality:** Concise, action-oriented, detail-focused

**Responsibilities:**
- Coordinating sprint execution with parallel batching
- Generating lean execution prompts (not full documents)
- Tracking progress meticulously
- Managing Git operations
- Handling task dependencies via `get_execution_order`
- Capturing lessons learned at sprint close

**Invoked by:** `/sprint-start`, `/sprint-close`

### Executor Agent
**Personality:** Implementation-focused, follows specs precisely

**Responsibilities:**
- Providing implementation guidance
- Writing clean, tested code
- Following architectural decisions from planning
- Creating branches with proper naming (`feat/`, `fix/`, `debug/`)
- Generating MR body template
- Code review and quality standards

**MR Body Template:**
```markdown
## Summary
<1-3 bullet points>

## Test plan
<Testing approach>

Closes #<issue-number>
```

## MCP Tools

### Issue Tools
| Tool | Description |
|------|-------------|
| `list_issues` | Query issues with filters |
| `get_issue` | Fetch single issue details |
| `create_issue` | Create new issue with labels |
| `update_issue` | Modify existing issue |
| `add_comment` | Add comments to issues |

### Label Tools
| Tool | Description |
|------|-------------|
| `get_labels` | Fetch org + repo label taxonomy |
| `suggest_labels` | Analyze context and suggest appropriate labels |
| `create_label` | Create missing required labels |

### Milestone Tools
| Tool | Description |
|------|-------------|
| `list_milestones` | List sprint milestones |
| `get_milestone` | Get milestone details |
| `create_milestone` | Create sprint milestone |
| `update_milestone` | Update/close milestone |

### Dependency Tools
| Tool | Description |
|------|-------------|
| `list_issue_dependencies` | Get issue dependencies |
| `create_issue_dependency` | Create dependency between issues |
| `get_execution_order` | Get parallel execution batches |

### Wiki Tools (Gitea Wiki)
| Tool | Description |
|------|-------------|
| `list_wiki_pages` | List wiki pages |
| `get_wiki_page` | Fetch specific page content |
| `create_wiki_page` | Create new wiki page |
| `create_lesson` | Create lessons learned document |
| `search_lessons` | Search past lessons by tags |

### Validation Tools
| Tool | Description |
|------|-------------|
| `validate_repo_org` | Check repo belongs to organization |
| `get_branch_protection` | Check branch protection rules |

## Label Taxonomy

The plugin uses a dynamic 43-label taxonomy (27 organization + 16 repository):

**Organization Labels:**
- Agent/* (2): Human, Claude
- Complexity/* (3): Simple, Medium, Complex
- Efforts/* (5): XS, S, M, L, XL
- Priority/* (4): Low, Medium, High, Critical
- Risk/* (3): Low, Medium, High
- Source/* (4): Development, Staging, Production, Customer
- Type/* (6): Bug, Feature, Refactor, Documentation, Test, Chore

**Repository Labels:**
- Component/* (9): Backend, Frontend, API, Database, Auth, Deploy, Testing, Docs, Infra
- Tech/* (7): Python, JavaScript, Docker, PostgreSQL, Redis, Vue, FastAPI

Labels are fetched dynamically from Gitea using `/labels-sync`.

## Branch-Aware Security

The plugin implements defense-in-depth branch detection to prevent accidental changes on production:

**Development Branches** (`development`, `develop`, `feat/*`, `dev/*`):
- Full planning and execution capabilities
- Can create and modify issues
- Can capture lessons learned

**Staging Branches** (`staging`, `stage/*`):
- Can create issues to document bugs
- Cannot modify code
- Warns when attempting changes

**Production Branches** (`main`, `master`, `prod/*`):
- Read-only access
- Cannot create issues
- Blocks all planning and execution

## Lessons Learned System

**Why it matters:** After 15 sprints without lesson capture, repeated mistakes occurred:
- Claude Code infinite loops on similar issues (2-3 times)
- Same architectural mistakes (multiple occurrences)
- Forgotten optimizations (re-discovered each time)

**Solution:** Mandatory lessons learned capture at sprint close, searchable at sprint start.

**Workflow:**
1. **Sprint Close:** Orchestrator captures lessons via Gitea Wiki tools
2. **Gitea Wiki Storage:** Lessons saved to repository wiki under `lessons-learned/sprints/`
3. **Sprint Start:** Planner searches relevant lessons by tags and keywords
4. **Prevention:** Apply learned insights to avoid repeating mistakes

**Lesson Structure:**
```markdown
# Sprint X - [Lesson Title]

## Context
[What were you trying to do?]

## Problem
[What went wrong or what insight emerged?]

## Solution
[How did you solve it?]

## Prevention
[How can this be avoided in the future?]

## Tags
[technology, component, type]
```

## Architecture

```
projman/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── .mcp.json                # MCP server configuration
├── mcp-servers/             # Bundled MCP server
│   └── gitea/
│       ├── .venv/
│       ├── requirements.txt
│       ├── mcp_server/
│       │   ├── server.py
│       │   ├── gitea_client.py
│       │   └── tools/
│       │       ├── issues.py
│       │       ├── labels.py
│       │       ├── wiki.py
│       │       ├── milestones.py
│       │       └── dependencies.py
│       └── tests/
├── commands/                # Slash commands
│   ├── sprint-plan.md
│   ├── sprint-start.md
│   ├── sprint-status.md
│   ├── sprint-close.md
│   ├── labels-sync.md
│   └── initial-setup.md
├── agents/                  # Agent prompts
│   ├── planner.md
│   ├── orchestrator.md
│   └── executor.md
├── skills/                  # Supporting knowledge
│   └── label-taxonomy/
│       └── labels-reference.md
├── README.md                # This file
└── CONFIGURATION.md         # Setup guide
```

## Configuration

See [CONFIGURATION.md](./CONFIGURATION.md) for detailed configuration instructions.

**Quick summary:**
- **System-level:** `~/.config/claude/gitea.env` (credentials)
- **Project-level:** `.env` in project root (repository specification)

## Troubleshooting

### Plugin not loading
- Check that MCP server is installed: `ls mcp-servers/gitea/.venv`
- Verify plugin manifest: `cat .claude-plugin/plugin.json | jq`
- Check Claude Code logs for errors

### Cannot connect to Gitea
- Verify `~/.config/claude/gitea.env` exists and has correct URL and token
- Test token: `curl -H "Authorization: token YOUR_TOKEN" https://gitea.example.com/api/v1/user`
- Check network connectivity

### Labels not syncing
- Run `/labels-sync` manually
- Check Gitea API token has `read:org` and `repo` permissions
- Verify repository name in `.env` matches Gitea

### Branch detection not working
- Ensure you're in a git repository: `git status`
- Check current branch: `git branch --show-current`
- If on wrong branch, switch: `git checkout development`

## Support

**Documentation:**
- [CONFIGURATION.md](./CONFIGURATION.md) - Setup and configuration

**Issues:**
- Report bugs: Contact repository maintainer
- Feature requests: Contact repository maintainer

## License

MIT License - See repository root for details

## Version

**Current:** 2.0.0

**Changelog:**
- v2.0.0: Full Gitea integration with wiki, milestones, dependencies, parallel execution
- v1.0.0: Initial release with basic commands

---

**Status:** Production Ready
