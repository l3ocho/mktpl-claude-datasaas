# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**Repository:** support-claude-mktplace
**Version:** 2.3.0
**Status:** Production Ready

A Claude Code plugin marketplace containing:

| Plugin | Description | Version |
|--------|-------------|---------|
| `projman` | Sprint planning and project management with Gitea integration | 2.3.0 |
| `doc-guardian` | Automatic documentation drift detection and synchronization | 1.0.0 |
| `code-sentinel` | Security scanning and code refactoring tools | 1.0.0 |
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
│   ├── projman/                  # Sprint management
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── mcp-servers/gitea/    # Bundled MCP server
│   │   ├── commands/             # 9 commands
│   │   │   ├── sprint-plan.md, sprint-start.md, sprint-status.md
│   │   │   ├── sprint-close.md, labels-sync.md, initial-setup.md
│   │   │   └── review.md, test-check.md, test-gen.md
│   │   ├── agents/               # 4 agents
│   │   │   ├── planner.md, orchestrator.md, executor.md
│   │   │   └── code-reviewer.md
│   │   └── skills/label-taxonomy/
│   ├── doc-guardian/             # Documentation drift detection
│   │   ├── .claude-plugin/plugin.json
│   │   ├── hooks/hooks.json      # PostToolUse, Stop hooks
│   │   ├── commands/             # doc-audit.md, doc-sync.md
│   │   ├── agents/               # doc-analyzer.md
│   │   └── skills/doc-patterns/
│   ├── code-sentinel/            # Security scanning & refactoring
│   │   ├── .claude-plugin/plugin.json
│   │   ├── hooks/hooks.json      # PreToolUse hook
│   │   ├── commands/             # security-scan.md, refactor.md, refactor-dry.md
│   │   ├── agents/               # security-reviewer.md, refactor-advisor.md
│   │   └── skills/security-patterns/
│   ├── claude-config-maintainer/
│   ├── cmdb-assistant/
│   └── project-hygiene/
├── scripts/
│   ├── setup.sh, post-update.sh
│   └── validate-marketplace.sh   # Marketplace compliance validation
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

### Four-Agent Model

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
| `docs/UPDATING.md` | Update guide for the marketplace |
| `plugins/projman/CONFIGURATION.md` | Projman setup guide |
| `plugins/projman/README.md` | Projman full documentation |

## Versioning and Changelog Rules

### Version Display
**The marketplace version is displayed ONLY in the main `README.md` title.**

- Format: `# Claude Code Marketplace - vX.Y.Z`
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
