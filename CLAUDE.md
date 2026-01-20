# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**Repository:** support-claude-mktplace
**Version:** 2.2.0
**Status:** Production Ready

A Claude Code plugin marketplace containing:

| Plugin | Description | Version |
|--------|-------------|---------|
| `projman` | Sprint planning and project management with Gitea integration | 2.2.0 |
| `claude-config-maintainer` | CLAUDE.md optimization and maintenance | 1.0.0 |
| `cmdb-assistant` | NetBox CMDB integration for infrastructure management | 1.0.0 |
| `project-hygiene` | Post-task cleanup automation via hooks | 0.1.0 |

## Quick Start

```bash
# Validate marketplace compliance
./scripts/validate-marketplace.sh

# Run projman commands (in a target project with plugin installed)
/sprint-plan      # Start sprint planning
/sprint-status    # Check progress
/review           # Pre-close code quality review
/test-check       # Verify tests before close
/sprint-close     # Complete sprint
```

## Repository Structure

```
support-claude-mktplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── plugins/
│   ├── projman/                  # Sprint management (v2.2.0)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── mcp-servers/gitea/    # Bundled MCP server
│   │   ├── commands/             # 8 commands
│   │   │   ├── sprint-plan.md, sprint-start.md, sprint-status.md
│   │   │   ├── sprint-close.md, labels-sync.md, initial-setup.md
│   │   │   ├── review.md, test-check.md    # NEW in v2.2.0
│   │   ├── agents/               # 4 agents
│   │   │   ├── planner.md, orchestrator.md, executor.md
│   │   │   └── code-reviewer.md            # NEW in v2.2.0
│   │   └── skills/label-taxonomy/
│   ├── claude-config-maintainer/
│   ├── cmdb-assistant/
│   └── project-hygiene/
├── scripts/
│   ├── setup.sh, post-update.sh
│   └── validate-marketplace.sh   # NEW in v2.2.0
└── docs/
    ├── CANONICAL-PATHS.md        # Single source of truth for paths
    └── references/
```

## CRITICAL: Rules You MUST Follow

### File Operations
- **NEVER** create files in repository root unless listed in "Allowed Root Files"
- **NEVER** modify `.gitignore` without explicit permission
- **ALWAYS** use `.scratch/` for temporary/exploratory work
- **ALWAYS** verify paths against `docs/CANONICAL-PATHS.md` before creating files

### Plugin Development
- **plugin.json MUST be in `.claude-plugin/` directory** (not plugin root)
- **Every plugin MUST be listed in marketplace.json**
- **MCP servers MUST use venv python path**: `${CLAUDE_PLUGIN_ROOT}/mcp-servers/{name}/.venv/bin/python`
- **CLI tools forbidden** - Use MCP tools exclusively (never `tea`, `gh`, etc.)

### Hooks (Valid Events Only)
`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Notification`, `Stop`, `SubagentStop`, `PreCompact`

**INVALID:** `task-completed`, `file-changed`, `git-commit-msg-needed`

### Allowed Root Files
`CLAUDE.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.env.example`

### Allowed Root Directories
`.claude/`, `.claude-plugin/`, `.claude-plugins/`, `.scratch/`, `docs/`, `hooks/`, `plugins/`, `scripts/`

## Architecture

### Four-Agent Model (projman v2.2.0)

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **Planner** | Thoughtful, methodical | Sprint planning, architecture analysis, issue creation, lesson search |
| **Orchestrator** | Concise, action-oriented | Sprint execution, parallel batching, Git operations, lesson capture |
| **Executor** | Implementation-focused | Code implementation, branch management, MR creation |
| **Code Reviewer** | Thorough, practical | Pre-close quality review, security scan, test verification |

### MCP Server Tools (Gitea)

| Category | Tools |
|----------|-------|
| Issues | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `add_comment` |
| Labels | `get_labels`, `suggest_labels`, `create_label` |
| Milestones | `list_milestones`, `get_milestone`, `create_milestone`, `update_milestone` |
| Dependencies | `list_issue_dependencies`, `create_issue_dependency`, `get_execution_order` |
| Wiki | `list_wiki_pages`, `get_wiki_page`, `create_wiki_page`, `create_lesson`, `search_lessons` |
| Validation | `validate_repo_org`, `get_branch_protection` |

### Hybrid Configuration

| Level | Location | Purpose |
|-------|----------|---------|
| System | `~/.config/claude/gitea.env` | Credentials (GITEA_URL, GITEA_TOKEN, GITEA_ORG) |
| Project | `.env` in project root | Repository specification (GITEA_REPO) |

### Branch-Aware Security

| Branch Pattern | Mode | Capabilities |
|----------------|------|--------------|
| `development`, `feat/*` | Development | Full access |
| `staging` | Staging | Read-only code, can create issues |
| `main`, `master` | Production | Read-only, emergency only |

## Label Taxonomy

43 labels total: 27 organization + 16 repository

**Organization:** Agent/2, Complexity/3, Efforts/5, Priority/4, Risk/3, Source/4, Type/6
**Repository:** Component/9, Tech/7

Sync with `/labels-sync` command.

## Lessons Learned System

Stored in Gitea Wiki under `lessons-learned/sprints/`.

**Workflow:**
1. Orchestrator captures at sprint close via MCP tools
2. Planner searches at sprint start using `search_lessons`
3. Tags enable cross-project discovery

## Common Operations

### Adding a New Plugin

1. Create `plugins/{name}/.claude-plugin/plugin.json`
2. Add entry to `.claude-plugin/marketplace.json`
3. Create `README.md` and `claude-md-integration.md`
4. Run `./scripts/validate-marketplace.sh`
5. Update `CHANGELOG.md`

### Adding a Command to projman

1. Create `plugins/projman/commands/{name}.md`
2. Update `plugins/projman/README.md`
3. Update marketplace description if significant

### Validation

```bash
./scripts/validate-marketplace.sh  # Validates all manifests
```

## Path Verification Protocol

**Before creating any file:**

1. Read `docs/CANONICAL-PATHS.md`
2. List all paths to be created/modified
3. Verify each against canonical paths
4. If not in canonical paths, STOP and ask

## Documentation Index

| Document | Purpose |
|----------|---------|
| `docs/CANONICAL-PATHS.md` | **Single source of truth** for paths |
| `docs/references/` | Reference specs and summaries |
| `plugins/projman/CONFIGURATION.md` | Projman setup guide |
| `plugins/projman/README.md` | Projman full documentation |

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 2.2.0 | 2026-01-20 | `/review`, `/test-check` commands, code-reviewer agent, validation script, marketplace compliance |
| 2.1.0 | Previous | Canonical paths, initial-setup command, documentation improvements |
| 2.0.0 | Previous | Full Gitea integration, wiki, milestones, dependencies, parallel execution |
| 0.1.0 | Initial | Basic plugin structure |

---

**Last Updated:** 2026-01-20 | **Current Version:** 2.2.0
