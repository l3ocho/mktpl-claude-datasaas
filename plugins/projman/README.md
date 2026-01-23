# Projman - Project Management for Claude Code

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
- **Four-Agent Model** - Planner, Orchestrator, Executor, and Code Reviewer agents
- **CLI Tools Blocked** - All operations via MCP tools only (no `tea` or `gh`)

## Quick Start

### 1. Prerequisites

- Claude Code installed
- Access to Gitea instance with API token
- Python 3.10+ installed
- Git repository initialized

### 2. Run Interactive Setup

The setup wizard handles everything:

```
/initial-setup
```

This will:
- Set up the MCP server (Python venv + dependencies)
- Create system config (`~/.config/claude/gitea.env`)
- Guide you through adding your Gitea token
- Detect and validate your repository via API
- Create project config (`.env`)

**For new projects** (when system is already configured):

```
/project-init
```

**After moving a repository:**

```
/project-sync
```

See [docs/CONFIGURATION.md](../../docs/CONFIGURATION.md) for detailed instructions.

### 3. Start Planning!

```
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
Full interactive setup wizard.

**What it does:**
- Checks Python version (requires 3.10+)
- Sets up MCP server virtual environment
- Creates system-level config (`~/.config/claude/gitea.env`)
- Guides token setup (manual entry for security)
- Detects and validates repository via Gitea API
- Creates project-level config (`.env` with GITEA_ORG, GITEA_REPO)

**When to use:** First time on a new machine

### `/project-init`
Quick project setup (assumes system config exists).

**What it does:**
- Verifies system configuration exists
- Detects organization and repository from git remote
- Validates via Gitea API
- Creates project `.env` file

**When to use:** Starting work on a new project

### `/project-sync`
Sync configuration with current git remote.

**What it does:**
- Compares .env values with git remote URL
- Validates new repository via Gitea API
- Updates .env if mismatch detected

**When to use:** After moving or renaming a repository

**Note:** A SessionStart hook automatically checks for:
1. Missing MCP venvs at the installed marketplace location (warns to run setup.sh)
2. Repository config mismatches (warns to run `/project-sync`)

### `/review`
Pre-sprint-close code quality review.

**What it does:**
- Scans recent changes for debug artifacts (TODO, console.log, commented code)
- Checks for code complexity issues (long functions, deep nesting)
- Performs lightweight security scan (hardcoded secrets, SQL injection risks)
- Identifies error handling gaps (bare except, swallowed exceptions)

**Output format:**
- Critical Issues (Block Sprint Close)
- Warnings (Should Address)
- Recommendations (Nice to Have)

**When to use:** Before closing a sprint to ensure code quality

### `/test-check`
Test verification before sprint close.

**What it does:**
- Automatically detects test framework (pytest, Jest, Go test, Cargo, etc.)
- Runs the test suite
- Reports pass/fail summary with details on failures
- Includes coverage report when available
- Identifies sprint files lacking test coverage

**Flags:**
- "run tests with coverage" - Include coverage report
- "run tests verbose" - Show full output
- "just check, don't run" - Report framework detection only

**When to use:** Before closing a sprint to ensure tests pass

### `/test-gen`
Generate tests for specified code.

**What it does:**
- Analyzes target code (function, class, or module)
- Auto-detects test framework (pytest, Jest, vitest, Go test, Cargo, etc.)
- Generates comprehensive tests: happy path, edge cases, error cases
- Supports unit, integration, e2e, and snapshot test types

**Usage:**
```
/test-gen <target> [--type=<type>] [--framework=<framework>]
```

**Target:** File path, function name, class name, or module
**Type:** unit (default), integration, e2e, snapshot

**When to use:** When adding new code that needs test coverage

## Debug Workflow Commands

These commands enable a cross-repository debugging workflow between your project and the marketplace.

### `/debug-report`
Run diagnostics and create structured issue in marketplace repository.

**What it does:**
- Runs MCP tool diagnostics (validate_repo_org, get_labels, list_issues, etc.)
- Captures error messages and hypothesis
- Creates a structured issue in the marketplace repository
- Tags with `Source: Diagnostic` label

**When to use:** When MCP tools fail in your project, run this to report the issue to the marketplace for investigation.

### `/debug-review`
Investigate diagnostic issues and propose fixes with human approval.

**What it does:**
- Fetches open diagnostic issues from marketplace
- Lets you select which issue to investigate
- Maps errors to relevant source files
- Reads code and analyzes root cause
- Proposes fixes with THREE mandatory approval gates
- Creates PR with fix after approval

**Approval Gates:**
1. Analysis confirmation - Does the investigation match your understanding?
2. Fix approach - Proceed with proposed changes?
3. PR creation - Create pull request?

**When to use:** In the marketplace repo, to investigate and fix issues reported by `/debug-report`.

## Code Quality Commands

The `/review` and `/test-check` commands complement the Executor agent by catching issues before work is marked complete. Run both commands before `/sprint-close` for a complete quality check.

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

### Code Reviewer Agent
**Personality:** Thorough, practical, severity-focused

**Responsibilities:**
- Identifying code quality issues before sprint close
- Prioritizing findings (Critical > Warning > Recommendation)
- Providing actionable feedback with file:line references
- Respecting sprint scope (only reviewing changed files)

**Invoked by:** `/review`

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
├── mcp-servers/
│   └── gitea -> ../../../mcp-servers/gitea  # SYMLINK to shared MCP server
├── commands/                # Slash commands
│   ├── sprint-plan.md
│   ├── sprint-start.md
│   ├── sprint-status.md
│   ├── sprint-close.md
│   ├── labels-sync.md
│   ├── initial-setup.md
│   ├── project-init.md
│   ├── project-sync.md
│   ├── review.md
│   ├── test-check.md
│   ├── test-gen.md
│   ├── debug-report.md
│   └── debug-review.md
├── agents/                  # Agent prompts
│   ├── planner.md
│   ├── orchestrator.md
│   ├── executor.md
│   └── code-reviewer.md
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

---

**Status:** Production Ready
