# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**Repository:** leo-claude-mktplace
**Version:** 3.0.1
**Status:** Production Ready

A plugin marketplace for Claude Code containing:

| Plugin | Description | Version |
|--------|-------------|---------|
| `projman` | Sprint planning and project management with Gitea integration | 3.0.0 |
| `git-flow` | Git workflow automation with smart commits and branch management | 1.0.0 |
| `pr-review` | Multi-agent PR review with confidence scoring | 1.0.0 |
| `clarity-assist` | Prompt optimization with ND-friendly accommodations | 1.0.0 |
| `doc-guardian` | Automatic documentation drift detection and synchronization | 1.0.0 |
| `code-sentinel` | Security scanning and code refactoring tools | 1.0.0 |
| `claude-config-maintainer` | CLAUDE.md optimization and maintenance | 1.0.0 |
| `cmdb-assistant` | NetBox CMDB integration for infrastructure management | 1.0.0 |
| `project-hygiene` | Post-task cleanup automation via hooks | 0.1.0 |

## Quick Start

```bash
# Validate marketplace compliance
./scripts/validate-marketplace.sh

# Setup commands (in a target project with plugin installed)
/initial-setup    # First time: full setup wizard
/project-init     # New project: quick config
/project-sync     # After repo move: sync config

# Run projman commands
/sprint-plan      # Start sprint planning
/sprint-status    # Check progress
/review           # Pre-close code quality review
/test-check       # Verify tests before close
/sprint-close     # Complete sprint
```

## Repository Structure

```
leo-claude-mktplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── mcp-servers/                  # SHARED MCP servers (v3.0.0+)
│   ├── gitea/                    # Gitea MCP (issues, PRs, wiki)
│   └── netbox/                   # NetBox MCP (CMDB)
├── plugins/
│   ├── projman/                  # Sprint management
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── mcp-servers/gitea -> ../../../mcp-servers/gitea  # SYMLINK
│   │   ├── commands/             # 12 commands (incl. setup)
│   │   ├── hooks/                # SessionStart mismatch detection
│   │   ├── agents/               # 4 agents
│   │   └── skills/label-taxonomy/
│   ├── git-flow/                 # Git workflow automation
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 8 commands
│   │   └── agents/
│   ├── pr-review/                # Multi-agent PR review
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── mcp-servers/gitea -> ../../../mcp-servers/gitea  # SYMLINK
│   │   ├── commands/             # 6 commands (incl. setup)
│   │   ├── hooks/                # SessionStart mismatch detection
│   │   └── agents/               # 5 agents
│   ├── clarity-assist/           # Prompt optimization (NEW v3.0.0)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 2 commands
│   │   └── agents/
│   ├── doc-guardian/             # Documentation drift detection
│   ├── code-sentinel/            # Security scanning & refactoring
│   ├── claude-config-maintainer/
│   ├── cmdb-assistant/
│   └── project-hygiene/
├── scripts/
│   ├── setup.sh, post-update.sh
│   └── validate-marketplace.sh   # Marketplace compliance validation
└── docs/
    ├── CANONICAL-PATHS.md        # Single source of truth for paths
    └── CONFIGURATION.md          # Centralized configuration guide
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
- **MCP servers are SHARED at root** with symlinks from plugins
- **MCP server venv path**: `${CLAUDE_PLUGIN_ROOT}/mcp-servers/{name}/.venv/bin/python`
- **CLI tools forbidden** - Use MCP tools exclusively (never `tea`, `gh`, etc.)

### Hooks (Valid Events Only)
`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Notification`, `Stop`, `SubagentStop`, `PreCompact`

**INVALID:** `task-completed`, `file-changed`, `git-commit-msg-needed`

### Allowed Root Files
`CLAUDE.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.env.example`

### Allowed Root Directories
`.claude/`, `.claude-plugin/`, `.claude-plugins/`, `.scratch/`, `docs/`, `hooks/`, `mcp-servers/`, `plugins/`, `scripts/`

## Architecture

### Four-Agent Model (projman)

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
| **Pull Requests** | `list_pull_requests`, `get_pull_request`, `get_pr_diff`, `get_pr_comments`, `create_pr_review`, `add_pr_comment` *(NEW v3.0.0)* |
| Validation | `validate_repo_org`, `get_branch_protection` |

### Hybrid Configuration

| Level | Location | Purpose |
|-------|----------|---------|
| System | `~/.config/claude/gitea.env` | Credentials (GITEA_API_URL, GITEA_API_TOKEN) |
| Project | `.env` in project root | Repository specification (GITEA_ORG, GITEA_REPO) |

**Note:** `GITEA_ORG` is at project level since different projects may belong to different organizations.

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
2. Add entry to `.claude-plugin/marketplace.json` with category, tags, license
3. Create `README.md` and `claude-md-integration.md`
4. If using MCP server, create symlink: `ln -s ../../../mcp-servers/{server} plugins/{name}/mcp-servers/{server}`
5. Run `./scripts/validate-marketplace.sh`
6. Update `CHANGELOG.md`

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
| `docs/COMMANDS-CHEATSHEET.md` | All commands quick reference with workflow examples |
| `docs/CONFIGURATION.md` | Centralized setup guide |
| `docs/UPDATING.md` | Update guide for the marketplace |
| `plugins/projman/CONFIGURATION.md` | Quick reference (links to central) |
| `plugins/projman/README.md` | Projman full documentation |

## Versioning and Changelog Rules

### Version Display
**The marketplace version is displayed ONLY in the main `README.md` title.**

- Format: `# Leo Claude Marketplace - vX.Y.Z`
- Do NOT add version numbers to individual plugin documentation titles
- Do NOT add version numbers to configuration guides
- Do NOT add version numbers to CLAUDE.md or other docs

### Changelog Maintenance (MANDATORY)
**`CHANGELOG.md` is the authoritative source for version history.**

When releasing a new version:
1. Update main `README.md` title with new version
2. Update `CHANGELOG.md` with:
   - Version number and date: `## [X.Y.Z] - YYYY-MM-DD`
   - **Added**: New features, commands, files
   - **Changed**: Modifications to existing functionality
   - **Fixed**: Bug fixes
   - **Removed**: Deleted features, files, deprecated items
3. Update `marketplace.json` metadata version
4. Update plugin `plugin.json` versions if plugin-specific changes

### Version Format
- Follow [Semantic Versioning](https://semver.org/): MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, minor improvements

---

**Last Updated:** 2026-01-20
