# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.
## ⛔ MANDATORY BEHAVIOR RULES - READ FIRST

**These rules are NON-NEGOTIABLE. Violating them wastes the user's time and money.**

### 1. WHEN USER ASKS YOU TO CHECK SOMETHING - CHECK EVERYTHING
- Search ALL locations, not just where you think it is
- Check cache directories: `~/.claude/plugins/cache/`
- Check installed: `~/.claude/plugins/marketplaces/`
- Check source: `~/claude-plugins-work/`
- **NEVER say "no" or "that's not the issue" without exhaustive verification**

### 2. WHEN USER SAYS SOMETHING IS WRONG - BELIEVE THEM
- The user knows their system better than you
- Investigate thoroughly before disagreeing
- If user suspects cache, CHECK THE CACHE
- If user suspects a file, READ THE FILE
- **Your confidence is often wrong. User's instincts are often right.**

### 3. NEVER SAY "DONE" WITHOUT VERIFICATION
- Run the actual command/script to verify
- Show the output to the user
- Check ALL affected locations
- **"Done" means VERIFIED WORKING, not "I made changes"**

### 4. SHOW EXACTLY WHAT USER ASKS FOR
- If user asks for messages, show the MESSAGES
- If user asks for code, show the CODE
- If user asks for output, show the OUTPUT
- **Don't interpret or summarize unless asked**

### 5. AFTER PLUGIN UPDATES - VERIFY AND RESTART

**⚠️ DO NOT clear cache mid-session** - this breaks MCP tools that are already loaded.

1. Run `./scripts/verify-hooks.sh` to check hook types
2. If changes affect MCP servers or hooks, inform the user:
   > "Plugin changes require a session restart to take effect. Please restart Claude Code."
3. Cache clearing is ONLY safe **before** starting a new session (not during)

See `docs/DEBUGGING-CHECKLIST.md` for details on cache timing.

**FAILURE TO FOLLOW THESE RULES = WASTED USER TIME = UNACCEPTABLE**

---


## Project Overview

**Repository:** leo-claude-mktplace
**Version:** 5.0.0
**Status:** Production Ready

A plugin marketplace for Claude Code containing:

| Plugin | Description | Version |
|--------|-------------|---------|
| `projman` | Sprint planning and project management with Gitea integration | 3.2.0 |
| `git-flow` | Git workflow automation with smart commits and branch management | 1.0.0 |
| `pr-review` | Multi-agent PR review with confidence scoring | 1.0.0 |
| `clarity-assist` | Prompt optimization with ND-friendly accommodations | 1.0.0 |
| `doc-guardian` | Automatic documentation drift detection and synchronization | 1.0.0 |
| `code-sentinel` | Security scanning and code refactoring tools | 1.0.0 |
| `claude-config-maintainer` | CLAUDE.md optimization and maintenance | 1.0.0 |
| `cmdb-assistant` | NetBox CMDB integration for infrastructure management | 1.0.0 |
| `data-platform` | pandas, PostgreSQL, and dbt integration for data engineering | 1.0.0 |
| `viz-platform` | DMC validation, Plotly charts, and theming for dashboards | 1.0.0 |
| `contract-validator` | Cross-plugin compatibility validation and agent verification | 1.0.0 |
| `project-hygiene` | Post-task cleanup automation via hooks | 0.1.0 |

## Quick Start

```bash
# Validate marketplace compliance
./scripts/validate-marketplace.sh

# After updates
./scripts/post-update.sh   # Rebuild venvs, verify symlinks
```

### Plugin Commands by Category

| Category | Commands |
|----------|----------|
| **Setup** | `/initial-setup`, `/project-init`, `/project-sync` |
| **Sprint** | `/sprint-plan`, `/sprint-start`, `/sprint-status`, `/sprint-close` |
| **Quality** | `/review`, `/test-check`, `/test-gen` |
| **Versioning** | `/suggest-version` |
| **PR Review** | `/pr-review:initial-setup`, `/pr-review:project-init` |
| **Docs** | `/doc-audit`, `/doc-sync` |
| **Security** | `/security-scan`, `/refactor`, `/refactor-dry` |
| **Config** | `/config-analyze`, `/config-optimize` |
| **Data** | `/ingest`, `/profile`, `/schema`, `/explain`, `/lineage`, `/run` |
| **Visualization** | `/component`, `/chart`, `/dashboard`, `/theme`, `/theme-new`, `/theme-css` |
| **Validation** | `/validate-contracts`, `/check-agent`, `/list-interfaces` |
| **Debug** | `/debug-report`, `/debug-review` |

## Repository Structure

```
leo-claude-mktplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── mcp-servers/                  # SHARED MCP servers (v3.0.0+)
│   ├── gitea/                    # Gitea MCP (issues, PRs, wiki)
│   ├── netbox/                   # NetBox MCP (CMDB)
│   ├── data-platform/            # pandas, PostgreSQL, dbt
│   └── viz-platform/             # DMC validation, charts, themes
├── plugins/
│   ├── projman/                  # Sprint management
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── mcp-servers/gitea -> ../../../mcp-servers/gitea  # SYMLINK
│   │   ├── commands/             # 14 commands (incl. setup, debug, suggest-version)
│   │   ├── hooks/                # SessionStart: mismatch detection + sprint suggestions
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
│   ├── clarity-assist/           # Prompt optimization
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 2 commands
│   │   └── agents/
│   ├── data-platform/            # Data engineering (NEW v4.0.0)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── mcp-servers/          # pandas, postgresql, dbt MCPs
│   │   ├── commands/             # 7 commands
│   │   ├── hooks/                # SessionStart PostgreSQL check
│   │   └── agents/               # 2 agents
│   ├── viz-platform/             # Visualization (NEW v4.0.0)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── mcp-servers/          # viz-platform MCP
│   │   ├── commands/             # 7 commands
│   │   ├── hooks/                # SessionStart DMC check
│   │   └── agents/               # 3 agents
│   ├── doc-guardian/             # Documentation drift detection
│   ├── code-sentinel/            # Security scanning & refactoring
│   ├── claude-config-maintainer/
│   ├── cmdb-assistant/
│   └── project-hygiene/
├── scripts/
│   ├── setup.sh, post-update.sh
│   ├── validate-marketplace.sh   # Marketplace compliance validation
│   ├── verify-hooks.sh           # Verify all hooks are command type
│   └── check-venv.sh             # Check MCP server venvs exist
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

#### ⚠️ plugin.json Format Rules (CRITICAL)
- **Hooks in separate file** - Use `hooks/hooks.json` (auto-discovered), NOT inline in plugin.json
- **NEVER reference hooks** - Don't add `"hooks": "..."` field to plugin.json at all
- **Agents auto-discover** - NEVER add `"agents": ["./agents/"]` - .md files found automatically
- **Always validate** - Run `./scripts/validate-marketplace.sh` before committing
- **Working examples:** projman, pr-review, claude-config-maintainer all use `hooks/hooks.json`
- See lesson: `lessons/patterns/plugin-manifest-validation---hooks-and-agents-format-requirements`

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
| Issues | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `add_comment`, `aggregate_issues` |
| Labels | `get_labels`, `suggest_labels`, `create_label`, `create_label_smart` |
| Milestones | `list_milestones`, `get_milestone`, `create_milestone`, `update_milestone`, `delete_milestone` |
| Dependencies | `list_issue_dependencies`, `create_issue_dependency`, `remove_issue_dependency`, `get_execution_order` |
| Wiki | `list_wiki_pages`, `get_wiki_page`, `create_wiki_page`, `update_wiki_page`, `create_lesson`, `search_lessons` |
| **Pull Requests** | `list_pull_requests`, `get_pull_request`, `get_pr_diff`, `get_pr_comments`, `create_pr_review`, `add_pr_comment` |
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
| `docs/COMMANDS-CHEATSHEET.md` | All commands quick reference |
| `docs/CONFIGURATION.md` | Centralized setup guide |
| `docs/DEBUGGING-CHECKLIST.md` | Systematic troubleshooting guide |
| `docs/UPDATING.md` | Update guide for the marketplace |
| `plugins/projman/CONFIGURATION.md` | Projman quick reference (links to central) |
| `plugins/projman/README.md` | Projman full documentation |

## Installation Paths

Understanding where files live is critical for debugging:

| Context | Path | Purpose |
|---------|------|---------|
| **Source** | `~/claude-plugins-work/` | Development - edit here |
| **Installed** | `~/.claude/plugins/marketplaces/leo-claude-mktplace/` | Runtime - Claude uses this |
| **Cache** | `~/.claude/` | Plugin metadata and settings |

**Key insight:** Edits to source require reinstall/update to take effect at runtime.

## Debugging & Troubleshooting

See `docs/DEBUGGING-CHECKLIST.md` for systematic troubleshooting.

**Common Issues:**
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "X MCP servers failed" | Missing venv in installed path | `cd ~/.claude/plugins/marketplaces/leo-claude-mktplace && ./scripts/setup.sh` |
| MCP tools not available | Symlink broken or venv missing | Run `/debug-report` to diagnose |
| Changes not taking effect | Editing source, not installed | Reinstall plugin or edit installed path |

**Debug Commands:**
- `/debug-report` - Run full diagnostics, create issue if needed
- `/debug-review` - Investigate and propose fixes

## Versioning Workflow

This project follows [SemVer](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com).

### Version Locations (must stay in sync)

| Location | Format | Example |
|----------|--------|---------|
| Git tags | `vX.Y.Z` | `v3.2.0` |
| README.md title | `# Leo Claude Marketplace - vX.Y.Z` | `v3.2.0` |
| marketplace.json | `"version": "X.Y.Z"` | `3.2.0` |
| CHANGELOG.md | `## [X.Y.Z] - YYYY-MM-DD` | `[3.2.0] - 2026-01-24` |

### During Development

**All changes go under `[Unreleased]` in CHANGELOG.md.** Never create a versioned section until release time.

```markdown
## [Unreleased]

### Added
- New feature description

### Fixed
- Bug fix description
```

### Creating a Release

Use the release script to ensure consistency:

```bash
./scripts/release.sh 3.2.0
```

The script will:
1. Validate `[Unreleased]` section has content
2. Replace `[Unreleased]` with `[3.2.0] - YYYY-MM-DD`
3. Update README.md title
4. Update marketplace.json version
5. Commit and create git tag

### SemVer Guidelines

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fixes only | PATCH (x.y.**Z**) | 3.1.1 → 3.1.2 |
| New features (backwards compatible) | MINOR (x.**Y**.0) | 3.1.2 → 3.2.0 |
| Breaking changes | MAJOR (**X**.0.0) | 3.2.0 → 4.0.0 |

---

**Last Updated:** 2026-01-24
