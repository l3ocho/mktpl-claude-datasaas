# CLAUDE.md

## ⛔ MANDATORY BEHAVIOR RULES - READ FIRST

**These rules are NON-NEGOTIABLE. Violating them wastes the user's time and money.**

### 1. WHEN USER ASKS YOU TO CHECK SOMETHING - CHECK EVERYTHING
- Search ALL locations, not just where you think it is
- Check cache directories: `~/.claude/plugins/cache/`
- Check installed: `~/.claude/plugins/marketplaces/`
- Check source directories
- **NEVER say "no" or "that's not the issue" without exhaustive verification**

### 2. WHEN USER SAYS SOMETHING IS WRONG - BELIEVE THEM
- The user knows their system better than you
- Investigate thoroughly before disagreeing
- **Your confidence is often wrong. User's instincts are often right.**

### 3. NEVER SAY "DONE" WITHOUT VERIFICATION
- Run the actual command/script to verify
- Show the output to the user
- **"Done" means VERIFIED WORKING, not "I made changes"**

### 4. SHOW EXACTLY WHAT USER ASKS FOR
- If user asks for messages, show the MESSAGES
- If user asks for code, show the CODE
- **Do not interpret or summarize unless asked**

**FAILURE TO FOLLOW THESE RULES = WASTED USER TIME = UNACCEPTABLE**

---



This file provides guidance to Claude Code when working with code in this repository.

## ⛔ RULES - READ FIRST

### Behavioral Rules

| Rule | Summary |
|------|---------|
| **Check everything** | Search cache (`~/.claude/plugins/cache/`), installed (`~/.claude/plugins/marketplaces/`), and source (`~/claude-plugins-work/`) |
| **Believe the user** | User knows their system. Investigate before disagreeing. |
| **Verify before "done"** | Run commands, show output, check all locations. "Done" = verified working. |
| **Show what's asked** | Don't interpret or summarize unless asked. |

### After Plugin Updates

Run `./scripts/verify-hooks.sh`. If changes affect MCP servers or hooks, inform user to restart session.
**DO NOT clear cache mid-session** - breaks loaded MCP tools.

### NEVER USE CLI TOOLS FOR EXTERNAL SERVICES
- **FORBIDDEN:** `gh`, `tea`, `curl` to APIs, any CLI that talks to Gitea/GitHub/external services
- **REQUIRED:** Use MCP tools exclusively (`mcp__plugin_projman_gitea__*`, `mcp__plugin_pr-review_gitea__*`)
- **NO EXCEPTIONS.** Don't try CLI first. Don't fall back to CLI. MCP ONLY.

### NEVER PUSH DIRECTLY TO PROTECTED BRANCHES
- **FORBIDDEN:** `git push origin development`, `git push origin main`, `git push origin master`
- **REQUIRED:** Create feature branch → push feature branch → create PR via MCP
- If you accidentally commit to a protected branch locally: `git checkout -b fix/branch-name` then reset the protected branch

### Repository Rules

| Rule | Details |
|------|---------|
| **File creation** | Only in allowed paths. Use `.scratch/` for temp work. Verify against `docs/CANONICAL-PATHS.md` |
| **plugin.json location** | Must be in `.claude-plugin/` directory |
| **Hooks** | Use `hooks/hooks.json` (auto-discovered). Never inline in plugin.json |
| **MCP servers** | Defined in root `.mcp.json`. Use MCP tools, never CLI (`tea`, `gh`) |
| **Allowed root files** | `CLAUDE.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.env.example` |

**Valid hook events:** `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Notification`, `Stop`, `SubagentStop`, `PreCompact`

### ⛔ MANDATORY: Before Any Code Change

**Claude MUST show this checklist BEFORE editing any file:**

#### 1. Impact Search Results
Run and show output of:
```bash
grep -rn "PATTERN" --include="*.sh" --include="*.md" --include="*.json" --include="*.py" | grep -v ".git"
```

#### 2. Files That Will Be Affected
Numbered list of every file to be modified, with the specific change for each.

#### 3. Files Searched But Not Changed (and why)
Proof that related files were checked and determined unchanged.

#### 4. Documentation That References This
List of docs that mention this feature/script/function.

**User verifies this list before Claude proceeds. If Claude skips this, STOP IMMEDIATELY.**

#### After Changes
Run the same grep and show results proving no references remain unaddressed.

---

## ⚠️ Development Context: We Build AND Use These Plugins

**This is a self-referential project.** We are:
1. **BUILDING** a plugin marketplace (source code in `plugins/`)
2. **USING** the installed marketplace to build it (dogfooding)

### Plugins ACTIVELY USED in This Project

These plugins are installed and should be used during development:

| Plugin | Used For |
|--------|----------|
| **projman** | Sprint planning, issue management, lessons learned |
| **git-flow** | Commits, branch management |
| **pr-review** | Pull request reviews |
| **doc-guardian** | Documentation drift detection |
| **code-sentinel** | Security scanning, refactoring |
| **clarity-assist** | Prompt clarification |
| **claude-config-maintainer** | CLAUDE.md optimization |
| **contract-validator** | Cross-plugin compatibility |

### Plugins NOT Used Here (Development Only)

These plugins exist in source but are **NOT relevant** to this project's workflow:

| Plugin | Why Not Used |
|--------|--------------|
| **data-platform** | For data engineering projects (pandas, PostgreSQL, dbt) |
| **viz-platform** | For dashboard projects (Dash, Plotly) |
| **cmdb-assistant** | For infrastructure projects (NetBox) |

**Do NOT suggest** `/ingest`, `/profile`, `/chart`, `/cmdb-*` commands - they don't apply here.

### Key Distinction

| Context | Path | What To Do |
|---------|------|------------|
| **Editing plugin source** | `~/claude-plugins-work/plugins/` | Modify code, add features |
| **Using installed plugins** | `~/.claude/plugins/marketplaces/` | Run commands like `/sprint-plan` |

When user says "run /sprint-plan", use the INSTALLED plugin.
When user says "fix the sprint-plan command", edit the SOURCE code.

---

## Project Overview

**Repository:** leo-claude-mktplace
**Version:** 5.9.0
**Status:** Production Ready

A plugin marketplace for Claude Code containing:

| Plugin | Description | Version |
|--------|-------------|---------|
| `projman` | Sprint planning and project management with Gitea integration | 3.3.0 |
| `git-flow` | Git workflow automation with smart commits and branch management | 1.0.0 |
| `pr-review` | Multi-agent PR review with confidence scoring | 1.1.0 |
| `clarity-assist` | Prompt optimization with ND-friendly accommodations | 1.0.0 |
| `doc-guardian` | Automatic documentation drift detection and synchronization | 1.0.0 |
| `code-sentinel` | Security scanning and code refactoring tools | 1.0.1 |
| `claude-config-maintainer` | CLAUDE.md optimization and maintenance | 1.0.0 |
| `cmdb-assistant` | NetBox CMDB integration for infrastructure management | 1.2.0 |
| `data-platform` | pandas, PostgreSQL, and dbt integration for data engineering | 1.3.0 |
| `viz-platform` | DMC validation, Plotly charts, and theming for dashboards | 1.1.0 |
| `contract-validator` | Cross-plugin compatibility validation and agent verification | 1.1.0 |
| `project-hygiene` | Post-task cleanup automation via hooks | 0.1.0 |

## Quick Start

```bash
# Validate marketplace compliance
./scripts/validate-marketplace.sh

# After updates
./scripts/post-update.sh   # Rebuild venvs
```

### Plugin Commands - USE THESE in This Project

| Category | Commands |
|----------|----------|
| **Setup** | `/setup` (modes: `--full`, `--quick`, `--sync`) |
| **Sprint** | `/sprint-plan`, `/sprint-start`, `/sprint-status` (with `--diagram`), `/sprint-close` |
| **Quality** | `/review`, `/test` (modes: `run`, `gen`) |
| **Versioning** | `/suggest-version` |
| **PR Review** | `/pr-review`, `/pr-summary`, `/pr-findings`, `/pr-diff` |
| **Docs** | `/doc-audit`, `/doc-sync`, `/changelog-gen`, `/doc-coverage`, `/stale-docs` |
| **Security** | `/security-scan`, `/refactor`, `/refactor-dry` |
| **Config** | `/config-analyze`, `/config-optimize`, `/config-diff`, `/config-lint` |
| **Validation** | `/validate-contracts`, `/check-agent`, `/list-interfaces`, `/dependency-graph` |
| **Debug** | `/debug` (modes: `report`, `review`) |

### Plugin Commands - NOT RELEVANT to This Project

These commands are being developed but don't apply to this project's workflow:

| Category | Commands | For Projects Using |
|----------|----------|-------------------|
| **Data** | `/ingest`, `/profile`, `/schema`, `/lineage`, `/dbt-test` | pandas, PostgreSQL, dbt |
| **Visualization** | `/component`, `/chart`, `/dashboard`, `/theme` | Dash, Plotly dashboards |
| **CMDB** | `/cmdb-search`, `/cmdb-device`, `/cmdb-sync` | NetBox infrastructure |

## Repository Structure

```
leo-claude-mktplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── .mcp.json                     # MCP server configuration (all servers)
├── mcp-servers/                  # SHARED MCP servers
│   ├── gitea/                    # Gitea MCP (issues, PRs, wiki)
│   ├── netbox/                   # NetBox MCP (CMDB)
│   ├── data-platform/            # pandas, PostgreSQL, dbt
│   ├── viz-platform/             # DMC validation, charts, themes
│   └── contract-validator/       # Plugin compatibility validation
├── plugins/
│   ├── projman/                  # Sprint management
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 12 commands
│   │   ├── hooks/                # SessionStart: mismatch detection
│   │   ├── agents/               # 4 agents
│   │   └── skills/               # 17 reusable skill files
│   ├── git-flow/                 # Git workflow automation
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 8 commands
│   │   └── agents/
│   ├── pr-review/                # Multi-agent PR review
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 6 commands
│   │   ├── hooks/                # SessionStart mismatch detection
│   │   └── agents/               # 5 agents
│   ├── clarity-assist/           # Prompt optimization
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 2 commands
│   │   └── agents/
│   ├── data-platform/            # Data engineering
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 7 commands
│   │   ├── hooks/                # SessionStart PostgreSQL check
│   │   └── agents/               # 2 agents
│   ├── viz-platform/             # Visualization
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 7 commands
│   │   ├── hooks/                # SessionStart DMC check
│   │   └── agents/               # 3 agents
│   ├── doc-guardian/             # Documentation drift detection
│   ├── code-sentinel/            # Security scanning & refactoring
│   ├── claude-config-maintainer/
│   ├── cmdb-assistant/
│   ├── contract-validator/
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

## Architecture

### Four-Agent Model (projman)

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **Planner** | Thoughtful, methodical | Sprint planning, architecture analysis, issue creation, lesson search |
| **Orchestrator** | Concise, action-oriented | Sprint execution, parallel batching, Git operations, lesson capture |
| **Executor** | Implementation-focused | Code implementation, branch management, MR creation |
| **Code Reviewer** | Thorough, practical | Pre-close quality review, security scan, test verification |

### Agent Model Selection

Agents specify their model in frontmatter using Claude Code's `model` field. Supported values: `sonnet` (default), `opus`, `haiku`, `inherit`.

| Plugin | Agent | Model | Rationale |
|--------|-------|-------|-----------|
| projman | Planner | sonnet | Architectural analysis, sprint planning |
| projman | Orchestrator | sonnet | Coordination and tool dispatch |
| projman | Executor | sonnet | Code generation and implementation |
| projman | Code Reviewer | sonnet | Quality gate, pattern detection |
| pr-review | Coordinator | sonnet | Orchestrates sub-agents, aggregates findings |
| pr-review | Security Reviewer | sonnet | Security analysis |
| pr-review | Performance Analyst | sonnet | Performance pattern detection |
| pr-review | Maintainability Auditor | haiku | Pattern matching (complexity, duplication) |
| pr-review | Test Validator | haiku | Coverage gap detection |
| data-platform | Data Advisor | sonnet | Schema validation, dbt orchestration |
| data-platform | Data Analysis | sonnet | Data exploration and profiling |
| data-platform | Data Ingestion | haiku | Data loading operations |
| viz-platform | Design Reviewer | sonnet | DMC validation + accessibility |
| viz-platform | Layout Builder | sonnet | Dashboard design guidance |
| viz-platform | Component Check | haiku | Quick component validation |
| viz-platform | Theme Setup | haiku | Theme configuration |
| contract-validator | Agent Check | haiku | Reference checking |
| contract-validator | Full Validation | sonnet | Marketplace sweep |
| code-sentinel | Security Reviewer | sonnet | Security analysis |
| code-sentinel | Refactor Advisor | sonnet | Code refactoring advice |
| doc-guardian | Doc Analyzer | sonnet | Documentation drift detection |
| clarity-assist | Clarity Coach | sonnet | Conversational coaching |
| git-flow | Git Assistant | haiku | Git operations |
| claude-config-maintainer | Maintainer | sonnet | CLAUDE.md optimization |
| cmdb-assistant | CMDB Assistant | sonnet | NetBox operations |

Override by editing the `model:` field in `plugins/{plugin}/agents/{agent}.md`.

### MCP Server Tools (Gitea)

| Category | Tools |
|----------|-------|
| Issues | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `add_comment`, `aggregate_issues` |
| Labels | `get_labels`, `suggest_labels`, `create_label`, `create_label_smart` |
| Milestones | `list_milestones`, `get_milestone`, `create_milestone`, `update_milestone`, `delete_milestone` |
| Dependencies | `list_issue_dependencies`, `create_issue_dependency`, `remove_issue_dependency`, `get_execution_order` |
| Wiki | `list_wiki_pages`, `get_wiki_page`, `create_wiki_page`, `update_wiki_page`, `create_lesson`, `search_lessons`, `allocate_rfc_number` |
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

### RFC System

Wiki-based Request for Comments system for tracking feature ideas from proposal through implementation.

**RFC Wiki Naming:**
- RFC pages: `RFC-NNNN: Short Title` (4-digit zero-padded)
- Index page: `RFC-Index` (auto-maintained)

**Lifecycle:** Draft → Review → Approved → Implementing → Implemented

**Integration with Sprint Planning:**
- `/sprint-plan` detects approved RFCs and offers selection
- `/sprint-close` updates RFC status on completion

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
3. Create `claude-md-integration.md`
4. If using new MCP server, add to root `mcp-servers/` and update `.mcp.json`
5. Run `./scripts/validate-marketplace.sh`
6. Update `CHANGELOG.md`

### Adding a Command to projman

1. Create `plugins/projman/commands/{name}.md`
2. Update marketplace description if significant

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
| MCP tools not available | Venv missing or .mcp.json misconfigured | Run `/debug report` to diagnose |
| Changes not taking effect | Editing source, not installed | Reinstall plugin or edit installed path |

**Debug Commands:**
- `/debug report` - Run full diagnostics, create issue if needed
- `/debug review` - Investigate and propose fixes

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

**Last Updated:** 2026-02-02
