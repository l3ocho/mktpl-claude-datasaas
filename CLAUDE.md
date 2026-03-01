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
| **saas-api-platform** | For REST/GraphQL API projects (FastAPI, Express) |
| **saas-db-migrate** | For database migration projects (Alembic, Prisma) |
| **saas-react-platform** | For React frontend projects (Next.js, Vite) |
| **saas-test-pilot** | For test automation projects (pytest, Jest, Playwright) |
| **data-seed** | For test data generation and seeding |
| **ops-release-manager** | For release management workflows |
| **ops-deploy-pipeline** | For deployment pipeline management |
| **debug-mcp** | For MCP server debugging and development |

**Do NOT suggest** `/data ingest`, `/data profile`, `/viz chart`, `/cmdb *`, `/api *`, `/db-migrate *`, `/react *`, `/test *`, `/seed *`, `/release *`, `/deploy *`, `/debug-mcp *` commands - they don't apply here.

### Key Distinction

| Context | Path | What To Do |
|---------|------|------------|
| **Editing plugin source** | `~/claude-plugins-work/plugins/` | Modify code, add features |
| **Using installed plugins** | `~/.claude/plugins/marketplaces/` | Run commands like `/sprint plan` |

When user says "run /sprint plan", use the INSTALLED plugin.
When user says "fix the sprint plan command", edit the SOURCE code.

---

## Project Overview

**Repository:** mktpl-claude-datasaas
**Version:** 9.1.2
**Status:** Production Ready

A plugin marketplace for Claude Code containing:

| Plugin | Description | Version |
|--------|-------------|---------|
| `projman` | Sprint planning and project management with Gitea integration | 9.0.1 |
| `git-flow` | Git workflow automation with smart commits and branch management | 9.0.1 |
| `pr-review` | Multi-agent PR review with confidence scoring | 9.0.1 |
| `clarity-assist` | Prompt optimization with ND-friendly accommodations | 9.0.1 |
| `doc-guardian` | Automatic documentation drift detection and synchronization | 9.0.1 |
| `code-sentinel` | Security scanning and code refactoring tools | 9.0.1 |
| `claude-config-maintainer` | CLAUDE.md optimization and maintenance | 9.0.1 |
| `cmdb-assistant` | NetBox CMDB integration for infrastructure management | 9.0.1 |
| `data-platform` | pandas, PostgreSQL, and dbt integration for data engineering | 9.1.0 |
| `viz-platform` | DMC validation, Plotly charts, and theming for dashboards | 9.1.0 |
| `contract-validator` | Cross-plugin compatibility validation and agent verification | 9.0.1 |
| `project-hygiene` | Manual project hygiene checks | 9.0.1 |
| `saas-api-platform` | REST/GraphQL API scaffolding for FastAPI and Express | 0.1.0 |
| `saas-db-migrate` | Database migration management for Alembic, Prisma, raw SQL | 0.1.0 |
| `saas-react-platform` | React frontend toolkit for Next.js and Vite | 0.1.0 |
| `saas-test-pilot` | Test automation for pytest, Jest, Vitest, Playwright | 0.1.0 |
| `data-seed` | Test data generation and database seeding | 0.1.0 |
| `ops-release-manager` | Release management with SemVer and changelog automation | 0.1.0 |
| `ops-deploy-pipeline` | Deployment pipeline for Docker Compose and systemd | 0.1.0 |
| `debug-mcp` | MCP server debugging and development toolkit | 0.1.0 |

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
| **Setup** | `/projman setup` (modes: `--full`, `--quick`, `--sync`) |
| **Sprint** | `/sprint plan`, `/sprint start`, `/sprint status` (with `--diagram`), `/sprint close` |
| **Quality** | `/sprint review`, `/sprint test` (modes: `run`, `gen`) |
| **Project** | `/project initiation`, `/project plan`, `/project status`, `/project close` |
| **ADR** | `/adr create`, `/adr list`, `/adr update`, `/adr supersede` |
| **RFC** | `/rfc create`, `/rfc list`, `/rfc review`, `/rfc approve`, `/rfc reject` |
| **PR Review** | `/pr review`, `/pr summary`, `/pr findings`, `/pr diff` |
| **Docs** | `/doc audit`, `/doc sync`, `/doc changelog-gen`, `/doc coverage`, `/doc stale-docs` |
| **Security** | `/sentinel scan`, `/sentinel refactor`, `/sentinel refactor-dry` |
| **Config** | `/claude-config analyze`, `/claude-config optimize`, `/claude-config diff`, `/claude-config lint` |
| **Validation** | `/cv validate`, `/cv check-agent`, `/cv list-interfaces`, `/cv dependency-graph`, `/cv status` |
| **Maintenance** | `/hygiene check` |

### Plugin Commands - NOT RELEVANT to This Project

These commands are being developed but don't apply to this project's workflow:

| Category | Commands | For Projects Using |
|----------|----------|-------------------|
| **Data** | `/data ingest`, `/data profile`, `/data schema`, `/data lineage`, `/data dbt-test` | pandas, PostgreSQL, dbt |
| **Visualization** | `/viz component`, `/viz chart`, `/viz dashboard`, `/viz theme` | Dash, Plotly dashboards |
| **CMDB** | `/cmdb search`, `/cmdb device`, `/cmdb sync` | NetBox infrastructure |
| **API** | `/api scaffold`, `/api validate`, `/api docs`, `/api middleware` | FastAPI, Express |
| **DB Migrate** | `/db-migrate generate`, `/db-migrate validate`, `/db-migrate plan` | Alembic, Prisma |
| **React** | `/react component`, `/react route`, `/react state`, `/react hook` | Next.js, Vite |
| **Testing** | `/test generate`, `/test coverage`, `/test fixtures`, `/test e2e` | pytest, Jest, Playwright |
| **Seeding** | `/seed generate`, `/seed profile`, `/seed apply` | Faker, test data |
| **Release** | `/release prepare`, `/release validate`, `/release tag` | SemVer releases |
| **Deploy** | `/deploy generate`, `/deploy validate`, `/deploy check` | Docker Compose, systemd |
| **Debug MCP** | `/debug-mcp status`, `/debug-mcp test`, `/debug-mcp logs` | MCP server development |

## Repository Structure

```
mktpl-claude-datasaas/
├── .claude-plugin/                # Marketplace manifest
│   ├── marketplace.json
│   ├── marketplace-lean.json      # Lean profile (6 core plugins)
│   └── marketplace-full.json      # Full profile (all plugins)
├── .mcp.json                     # MCP server configuration (all servers)
├── mcp-servers/                  # SHARED MCP servers
│   ├── gitea/                    # Gitea (issues, PRs, wiki)
│   ├── netbox/                   # NetBox (DCIM, IPAM)
│   ├── data-platform/            # pandas, PostgreSQL, dbt
│   ├── viz-platform/             # DMC, Plotly, theming
│   └── contract-validator/       # Plugin compatibility validation
├── plugins/                      # All plugins (20 total)
│   ├── projman/                  # [core] Sprint management
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/             # 19 commands
│   │   ├── agents/               # 4 agents
│   │   └── skills/               # 23 reusable skill files
│   ├── git-flow/                 # [core] Git workflow automation
│   ├── pr-review/                # [core] PR review
│   ├── clarity-assist/           # [core] Prompt optimization
│   ├── doc-guardian/             # [core] Documentation drift detection
│   ├── code-sentinel/            # [core] Security scanning
│   ├── claude-config-maintainer/ # [core] CLAUDE.md optimization
│   ├── contract-validator/       # [core] Cross-plugin validation
│   ├── project-hygiene/          # [core] Manual cleanup checks
│   ├── cmdb-assistant/           # [ops] NetBox CMDB integration
│   ├── data-platform/            # [data] Data engineering
│   ├── viz-platform/             # [data] Visualization
│   ├── data-seed/                # [data] Test data generation (scaffold)
│   ├── saas-api-platform/        # [saas] API scaffolding (scaffold)
│   ├── saas-db-migrate/          # [saas] DB migrations (scaffold)
│   ├── saas-react-platform/      # [saas] React toolkit (scaffold)
│   ├── saas-test-pilot/          # [saas] Test automation (scaffold)
│   ├── ops-release-manager/      # [ops] Release management (scaffold)
│   ├── ops-deploy-pipeline/      # [ops] Deployment pipeline (scaffold)
│   └── debug-mcp/                # [debug] MCP debugging (scaffold)
├── scripts/                      # Setup and maintenance
│   ├── setup.sh                  # Initial setup (create venvs, config)
│   ├── post-update.sh            # Post-update (clear cache, changelog)
│   ├── setup-venvs.sh            # MCP server venv management (cache-based)
│   ├── validate-marketplace.sh   # Marketplace compliance validation
│   ├── verify-hooks.sh           # Hook inventory verification
│   ├── release.sh                # Release automation with version bumping
│   ├── claude-launch.sh          # Profile-based launcher
│   ├── install-plugin.sh         # Install plugin to consumer project
│   ├── list-installed.sh         # Show installed plugins in a project
│   └── uninstall-plugin.sh       # Remove plugin from consumer project
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # System architecture & plugin reference
│   ├── CANONICAL-PATHS.md        # Authoritative path reference
│   ├── COMMANDS-CHEATSHEET.md    # All commands quick reference
│   ├── CONFIGURATION.md          # Centralized setup guide
│   ├── DEBUGGING-CHECKLIST.md    # Systematic troubleshooting guide
│   ├── MIGRATION-v9.md           # v8.x to v9.0.0 migration guide
│   └── UPDATING.md               # Update guide
├── CLAUDE.md                      # Project instructions for Claude Code
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

## Architecture

### Four-Agent Model (projman)

| Agent | Personality | Responsibilities |
|-------|-------------|------------------|
| **Planner** | Thoughtful, methodical | Sprint planning, architecture analysis, issue creation, lesson search |
| **Orchestrator** | Concise, action-oriented | Sprint execution, parallel batching, Git operations, lesson capture |
| **Executor** | Implementation-focused | Code implementation, branch management, MR creation |
| **Code Reviewer** | Thorough, practical | Pre-close quality review, security scan, test verification |

### Agent Frontmatter Configuration

Agents specify their configuration in frontmatter using Claude Code's supported fields. Reference: https://code.claude.com/docs/en/sub-agents

**Supported frontmatter fields:**

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | Yes | — | Unique identifier, lowercase + hyphens |
| `description` | Yes | — | When Claude should delegate to this subagent |
| `model` | No | `inherit` | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default` | Controls permission prompts: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `disallowedTools` | No | none | Comma-separated tools to remove from agent's toolset |
| `skills` | No | none | Comma-separated skills auto-injected into context at startup |
| `hooks` | No | none | Lifecycle hooks scoped to this subagent |

**Complete agent matrix:**

| Plugin | Agent | `model` | `permissionMode` | `disallowedTools` | `skills` |
|--------|-------|---------|-------------------|--------------------|----------|
| projman | planner | opus | default | — | frontmatter (2) + body text (12) |
| projman | orchestrator | sonnet | acceptEdits | — | frontmatter (2) + body text (10) |
| projman | executor | sonnet | bypassPermissions | — | frontmatter (7) |
| projman | code-reviewer | opus | default | Write, Edit, MultiEdit | frontmatter (4) |
| pr-review | coordinator | sonnet | plan | Write, Edit, MultiEdit | — |
| pr-review | security-reviewer | sonnet | plan | Write, Edit, MultiEdit | — |
| pr-review | performance-analyst | sonnet | plan | Write, Edit, MultiEdit | — |
| pr-review | maintainability-auditor | haiku | plan | Write, Edit, MultiEdit | — |
| pr-review | test-validator | haiku | plan | Write, Edit, MultiEdit | — |
| data-platform | data-advisor | sonnet | default | — | — |
| data-platform | data-analysis | sonnet | plan | Write, Edit, MultiEdit | — |
| data-platform | data-ingestion | haiku | acceptEdits | — | — |
| viz-platform | design-reviewer | sonnet | plan | Write, Edit, MultiEdit | — |
| viz-platform | layout-builder | sonnet | default | — | — |
| viz-platform | component-check | haiku | plan | Write, Edit, MultiEdit | — |
| viz-platform | theme-setup | haiku | acceptEdits | — | — |
| contract-validator | full-validation | sonnet | default | — | — |
| contract-validator | agent-check | haiku | plan | Write, Edit, MultiEdit | — |
| code-sentinel | security-reviewer | sonnet | plan | Write, Edit, MultiEdit | — |
| code-sentinel | refactor-advisor | sonnet | acceptEdits | — | — |
| doc-guardian | doc-analyzer | sonnet | acceptEdits | — | — |
| clarity-assist | clarity-coach | sonnet | default | Write, Edit, MultiEdit | — |
| git-flow | git-assistant | haiku | acceptEdits | — | — |
| claude-config-maintainer | maintainer | sonnet | acceptEdits | — | frontmatter (2) |
| cmdb-assistant | cmdb-assistant | sonnet | default | — | — |

**Design principles:**
- `bypassPermissions` is granted to exactly ONE agent (Executor) which has code-sentinel PreToolUse hook + Code Reviewer downstream as safety nets.
- `plan` mode is assigned to all pure analysis agents (pr-review, read-only validators).
- `disallowedTools: Write, Edit, MultiEdit` provides defense-in-depth on agents that should never write files.
- `skills` frontmatter is used for agents with ≤7 skills where guaranteed loading is safety-critical. Agents with 8+ skills use body text `## Skills to Load` for selective loading.
- `hooks` (agent-scoped) is reserved for future use (v6.0+).

Override any field by editing the agent's `.md` file in `plugins/{plugin}/agents/`.

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
- `/sprint plan` detects approved RFCs and offers selection
- `/sprint close` updates RFC status on completion

## Label Taxonomy

58 labels total: 31 organization + 27 repository

**Organization:** Agent/2, Complexity/3, Efforts/5, Priority/4, Risk/3, Source/4, Status/4, Type/6
**Repository:** Component/9, Tech/7, Domain/2, Epic/5, RnD/4

Sync with `/labels sync` command.

## Lessons Learned System

Stored in Gitea Wiki under `lessons-learned/sprints/`.

**Workflow:**
1. Orchestrator captures at sprint close via MCP tools
2. Planner searches at sprint start using `search_lessons`
3. Tags enable cross-project discovery

## Common Operations

### Adding a New Plugin

1. Create `plugins/{name}/.claude-plugin/plugin.json` (standard schema fields only — no custom fields)
2. Create `plugins/{name}/.claude-plugin/metadata.json` — must include `"domain"` field (`core`, `data`, `saas`, `ops`, or `debug`)
3. Add entry to `.claude-plugin/marketplace.json` with category, tags, license (no custom fields — Claude Code schema is strict)
4. Create `claude-md-integration.md`
5. If using new MCP server, add to root `mcp-servers/` and update `.mcp.json`
6. Run `./scripts/validate-marketplace.sh` — rejects plugins without valid `domain` field
7. Update `CHANGELOG.md`

**Domain field is required in metadata.json (v8.0.0+, moved from plugin.json in v9.1.2):**
```json
{
  "domain": "core"
}
```

**Naming convention:** New plugins use domain prefix (`saas-*`, `ops-*`, `data-*`, `debug-*`). Core plugins have no prefix.

### Domain Assignments

| Domain | Plugins |
|--------|---------|
| `core` | projman, git-flow, pr-review, code-sentinel, doc-guardian, clarity-assist, contract-validator, claude-config-maintainer, project-hygiene |
| `data` | data-platform, viz-platform, data-seed |
| `saas` | saas-api-platform, saas-db-migrate, saas-react-platform, saas-test-pilot |
| `ops` | cmdb-assistant, ops-release-manager, ops-deploy-pipeline |
| `debug` | debug-mcp |

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
| `docs/ARCHITECTURE.md` | System architecture and plugin reference |
| `docs/CANONICAL-PATHS.md` | **Single source of truth** for paths |
| `docs/COMMANDS-CHEATSHEET.md` | All commands quick reference |
| `docs/CONFIGURATION.md` | Centralized setup guide |
| `docs/DEBUGGING-CHECKLIST.md` | Systematic troubleshooting guide |
| `docs/MIGRATION-v9.md` | v8.x to v9.0.0 migration guide |
| `docs/UPDATING.md` | Update guide for the marketplace |
| `plugins/projman/CONFIGURATION.md` | Projman quick reference (links to central) |

## Installation Paths

Understanding where files live is critical for debugging:

| Context | Path | Purpose |
|---------|------|---------|
| **Source** | `~/claude-plugins-work/` | Development - edit here |
| **Installed** | `~/.claude/plugins/marketplaces/mktpl-claude-datasaas/` | Runtime - Claude uses this |
| **Cache** | `~/.claude/` | Plugin metadata and settings |

**Key insight:** Edits to source require reinstall/update to take effect at runtime.

## Debugging & Troubleshooting

See `docs/DEBUGGING-CHECKLIST.md` for systematic troubleshooting.

**Common Issues:**
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "X MCP servers failed" | Missing venv in installed path | `cd ~/.claude/plugins/marketplaces/mktpl-claude-datasaas && ./scripts/setup.sh` |
| MCP tools not available | Venv missing or .mcp.json misconfigured | Run `/cv status` to diagnose |
| Changes not taking effect | Editing source, not installed | Reinstall plugin or edit installed path |

**Diagnostic Commands:**
- `/cv status` - Marketplace-wide health check (installation, MCP, configuration)
- `/hygiene check` - Project file organization and cleanup check

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

**Last Updated:** 2026-02-07
