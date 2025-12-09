# Projman - Project Management for Claude Code

Sprint planning and project management plugin with Gitea and Wiki.js integration.

## Overview

Projman transforms a proven 15-sprint workflow into a distributable Claude Code plugin. It provides AI-guided sprint planning, intelligent issue creation with label taxonomy, and systematic lessons learned capture to prevent repeated mistakes.

**Key Features:**
- 🎯 **Sprint Planning** - AI-guided architecture analysis and issue creation
- 🏷️ **Smart Label Suggestions** - Intelligent label recommendations from 44-label taxonomy
- 📚 **Lessons Learned** - Systematic capture and search of sprint insights
- 🔒 **Branch-Aware Security** - Prevents accidental changes on production branches
- ⚙️ **Hybrid Configuration** - Simple setup with system + project-level config
- 🤖 **Three-Agent Model** - Planner, Orchestrator, and Executor agents

## Quick Start

### 1. Prerequisites

- Claude Code installed
- Access to Gitea instance with API token
- Access to Wiki.js instance with API token
- Python 3.10+ installed
- Git repository initialized

### 2. Install MCP Servers

The plugin requires two shared MCP servers:

```bash
# Navigate to MCP servers directory
cd ../mcp-servers/gitea
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

cd ../wikijs
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

See [CONFIGURATION.md](./CONFIGURATION.md) for detailed setup instructions.

### 3. Configure System-Level Settings

Create system-wide configuration with your Gitea and Wiki.js credentials:

```bash
mkdir -p ~/.config/claude

# Gitea configuration
cat > ~/.config/claude/gitea.env << EOF
GITEA_API_URL=https://gitea.example.com/api/v1
GITEA_API_TOKEN=your_gitea_token_here
GITEA_OWNER=bandit
EOF

# Wiki.js configuration
cat > ~/.config/claude/wikijs.env << EOF
WIKIJS_API_URL=https://wiki.hyperhivelabs.com/graphql
WIKIJS_API_TOKEN=your_wikijs_token_here
WIKIJS_BASE_PATH=/hyper-hive-labs
EOF

# Secure the files
chmod 600 ~/.config/claude/*.env
```

### 4. Configure Project-Level Settings

In your project root directory, create a `.env` file:

```bash
# In your project directory
cat > .env << EOF
GITEA_REPO=your-repo-name
WIKIJS_PROJECT=projects/your-project-name
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

### 5. Sync Label Taxonomy

Fetch the label taxonomy from Gitea:

```bash
/labels-sync
```

### 6. Start Planning!

```bash
/sprint-plan
```

## Commands

### `/sprint-plan`
Start sprint planning with the AI planner agent.

**What it does:**
- Asks clarifying questions about sprint goals
- Searches relevant lessons learned from previous sprints
- Performs architecture analysis
- Creates Gitea issues with intelligent label suggestions
- Generates planning document

**When to use:** Beginning of a new sprint or when planning a major feature

**Example:**
```
/sprint-plan

> "I want to plan a sprint for user authentication"
```

### `/sprint-start`
Begin sprint execution with the orchestrator agent.

**What it does:**
- Reviews open sprint issues
- Searches relevant lessons learned by tags
- Identifies next task based on priority and dependencies
- Generates lean execution prompts
- Tracks progress

**When to use:** After planning, when ready to start implementation

**Example:**
```
/sprint-start
```

### `/sprint-status`
Check current sprint progress.

**What it does:**
- Lists all sprint issues by status (open, in progress, blocked, completed)
- Identifies blockers and priorities
- Shows completion percentage
- Highlights critical items needing attention

**When to use:** Daily standup, progress check, deciding what to work on next

**Example:**
```
/sprint-status
```

### `/sprint-close`
Complete sprint and capture lessons learned.

**What it does:**
- Reviews sprint completion
- Captures lessons learned (what went wrong, what went right)
- Tags lessons for discoverability
- Saves lessons to Wiki.js
- Handles git operations (merge, tag, cleanup)

**When to use:** End of sprint, before starting the next one

**Example:**
```
/sprint-close
```

**CRITICAL:** Don't skip this! After 15 sprints without lesson capture, teams repeat the same mistakes.

### `/labels-sync`
Synchronize label taxonomy from Gitea.

**What it does:**
- Fetches current labels from Gitea (org + repo)
- Compares with local reference
- Detects changes (new, modified, removed labels)
- Updates local taxonomy reference
- Updates suggestion logic

**When to use:**
- First-time setup
- Monthly maintenance
- When new labels are added to Gitea
- When label suggestions seem incorrect

**Example:**
```
/labels-sync
```

## Agents

### Planner Agent
**Personality:** Thoughtful, methodical, asks clarifying questions

**Responsibilities:**
- Sprint planning and architecture analysis
- Asking clarifying questions before making assumptions
- Searching relevant lessons learned
- Creating well-structured Gitea issues
- Suggesting appropriate labels based on context

**Invoked by:** `/sprint-plan`

### Orchestrator Agent
**Personality:** Concise, action-oriented, detail-focused

**Responsibilities:**
- Coordinating sprint execution
- Generating lean execution prompts (not full documents)
- Tracking progress meticulously
- Managing Git operations
- Handling task dependencies
- Capturing lessons learned at sprint close

**Invoked by:** `/sprint-start`, `/sprint-close`

### Executor Agent
**Personality:** Implementation-focused, follows specs precisely

**Responsibilities:**
- Providing implementation guidance
- Writing clean, tested code
- Following architectural decisions from planning
- Generating completion reports
- Code review and quality standards

**Usage:** Can be invoked by the orchestrator when implementation guidance is needed.

## Label Taxonomy

The plugin uses a dynamic 44-label taxonomy (28 organization + 16 repository):

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
- ✅ Full planning and execution capabilities
- ✅ Can create and modify issues
- ✅ Can capture lessons learned

**Staging Branches** (`staging`, `stage/*`):
- ✅ Can create issues to document bugs
- ❌ Cannot modify code
- ⚠️ Warns when attempting changes

**Production Branches** (`main`, `master`, `prod/*`):
- ✅ Read-only access
- ❌ Cannot create issues
- ❌ Cannot modify code
- 🛑 Blocks all planning and execution

## Lessons Learned System

**Why it matters:** After 15 sprints without lesson capture, repeated mistakes occurred:
- Claude Code infinite loops on similar issues (2-3 times)
- Same architectural mistakes (multiple occurrences)
- Forgotten optimizations (re-discovered each time)

**Solution:** Mandatory lessons learned capture at sprint close, searchable at sprint start.

**Workflow:**
1. **Sprint Close:** Orchestrator captures lessons (what went wrong, what went right, preventable mistakes)
2. **Wiki.js Storage:** Lessons saved to `/projects/{project}/lessons-learned/sprints/`
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

## Configuration

See [CONFIGURATION.md](./CONFIGURATION.md) for detailed configuration instructions.

**Quick summary:**
- **System-level:** `~/.config/claude/gitea.env` and `wikijs.env` (credentials)
- **Project-level:** `.env` in project root (repository and project paths)
- **MCP Servers:** Located at `../mcp-servers/` (shared by multiple plugins)

## Troubleshooting

### Plugin not loading
- Check that MCP servers are installed: `ls ../mcp-servers/gitea/.venv`
- Verify plugin manifest: `cat .claude-plugin/plugin.json | jq`
- Check Claude Code logs for errors

### Cannot connect to Gitea
- Verify `~/.config/claude/gitea.env` exists and has correct URL and token
- Test token: `curl -H "Authorization: token YOUR_TOKEN" https://gitea.example.com/api/v1/user`
- Check network connectivity

### Cannot connect to Wiki.js
- Verify `~/.config/claude/wikijs.env` exists and has correct URL and token
- Check Wiki.js GraphQL endpoint: `https://wiki.hyperhivelabs.com/graphql`
- Verify API token has pages read/write permissions

### Labels not syncing
- Run `/labels-sync` manually
- Check Gitea API token has `read:org` and `repo` permissions
- Verify repository name in `.env` matches Gitea

### Branch detection not working
- Ensure you're in a git repository: `git status`
- Check current branch: `git branch --show-current`
- If on wrong branch, switch: `git checkout development`

## Architecture

```
projman/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── .mcp.json                # MCP server configuration
├── commands/                # Slash commands
│   ├── sprint-plan.md
│   ├── sprint-start.md
│   ├── sprint-status.md
│   ├── sprint-close.md
│   └── labels-sync.md
├── agents/                  # Agent prompts (Phase 3)
│   ├── planner.md
│   ├── orchestrator.md
│   └── executor.md
├── skills/                  # Supporting knowledge
│   └── label-taxonomy/
│       └── labels-reference.md
├── README.md                # This file
└── CONFIGURATION.md         # Setup guide
```

**MCP Servers (shared):**
```
../mcp-servers/
├── gitea/                   # Gitea MCP server
│   ├── .venv/
│   ├── mcp_server/
│   └── tests/
└── wikijs/                  # Wiki.js MCP server
    ├── .venv/
    ├── mcp_server/
    └── tests/
```

## Workflow Example

**Complete Sprint Lifecycle:**

```bash
# 1. Plan the sprint
/sprint-plan
> "Extract Intuit Engine service from monolith"
[Planner asks questions, searches lessons, creates issues]

# 2. Start execution
/sprint-start
[Orchestrator reviews issues, finds relevant lessons, identifies next task]

# 3. Check progress daily
/sprint-status
[See completion percentage, blockers, priorities]

# 4. Close sprint and capture lessons
/sprint-close
[Orchestrator captures lessons learned, saves to Wiki.js]

# Next sprint uses those lessons automatically!
```

## Support

**Documentation:**
- [CONFIGURATION.md](./CONFIGURATION.md) - Setup and configuration
- [Gitea MCP Server](../mcp-servers/gitea/README.md) - Gitea integration details
- [Wiki.js MCP Server](../mcp-servers/wikijs/README.md) - Wiki.js integration details

**Issues:**
- Report bugs: Contact repository maintainer
- Feature requests: Contact repository maintainer
- Documentation improvements: Submit PR

## License

MIT License - See repository root for details

## Related Plugins

- **projman-pmo** - Multi-project PMO coordination (build after projman is validated)

## Version

**Current:** 0.1.0 (Phase 2 - Commands implemented)

**Roadmap:**
- Phase 3: Agent system implementation
- Phase 4: Lessons learned integration
- Phase 5: Testing and validation
- Phase 6-8: Documentation, marketplace, production

---

**Built for:** Bandit Labs
**Status:** Phase 2 Complete - Commands ready for testing
**Next:** Implement agent system (Phase 3)
