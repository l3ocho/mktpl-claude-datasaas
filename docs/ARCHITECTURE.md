# Architecture — Leo Claude Marketplace v9.1.2

## Overview

Plugin marketplace for Claude Code. 20 plugins across 5 domains, 5 shared MCP servers,
4 PreToolUse safety hooks + 1 UserPromptSubmit quality hook.

## System Architecture

### Plugin Domains

| Domain | Purpose | Plugins |
|--------|---------|---------|
| core | Development workflow | projman, git-flow, pr-review, code-sentinel, doc-guardian, clarity-assist, contract-validator, claude-config-maintainer, project-hygiene |
| data | Data engineering | data-platform, viz-platform, data-seed |
| saas | SaaS development | saas-api-platform, saas-db-migrate, saas-react-platform, saas-test-pilot |
| ops | Operations | cmdb-assistant, ops-release-manager, ops-deploy-pipeline |
| debug | Diagnostics | debug-mcp |

### MCP Servers (Shared at Root)

| Server | Plugins Using It | External System |
|--------|-------------------|-----------------|
| gitea | projman, pr-review | Gitea (issues, PRs, wiki) — uses published `gitea-mcp` package |
| netbox | cmdb-assistant | NetBox (DCIM, IPAM) |
| data-platform | data-platform | PostgreSQL, dbt |
| viz-platform | viz-platform | DMC registry |
| contract-validator | contract-validator | (internal validation) |

### Hook Architecture

| Plugin | Event | Trigger | Script |
|--------|-------|---------|--------|
| code-sentinel | PreToolUse | Write\|Edit\|MultiEdit | security-check.sh |
| git-flow | PreToolUse | Bash (branch naming) | branch-check.sh |
| git-flow | PreToolUse | Bash (git commit) | commit-msg-check.sh |
| cmdb-assistant | PreToolUse | MCP create/update | validate-input.sh |
| clarity-assist | UserPromptSubmit | All prompts | vagueness-check.sh |

No other hook types permitted. All workflow automation is via explicit commands.

### Agent Model (projman)

| Agent | Model | Permission Mode | Role |
|-------|-------|-----------------|------|
| Planner | opus | default | Sprint planning, architecture analysis, issue creation |
| Orchestrator | sonnet | acceptEdits | Sprint execution, parallel batching, lesson capture |
| Executor | sonnet | bypassPermissions | Code implementation, branch management |
| Code Reviewer | opus | default | Pre-close quality review, security, tests |

### Config Hierarchy

| Level | Location | Contains |
|-------|----------|----------|
| System | ~/.config/claude/{service}.env | Credentials |
| Project | .env in project root | Repo-specific config |

### Branch Security

| Pattern | Access |
|---------|--------|
| development, feat/*, fix/* | Full |
| staging, stage/* | Read-only code, can create issues |
| main, master, prod/* | READ-ONLY. Emergency only. |

### Launch Profiles

| Profile | Plugins |
|---------|---------|
| sprint | projman, git-flow, pr-review, code-sentinel, doc-guardian, clarity-assist |
| data | data-platform, viz-platform, data-seed |
| saas | saas-api-platform, saas-react-platform, saas-db-migrate, saas-test-pilot |
| ops | cmdb-assistant, ops-release-manager, ops-deploy-pipeline |
| review | pr-review, code-sentinel |
| debug | debug-mcp |
| full | all plugins |

---

## Plugin Reference

### Core Domain

#### projman (v9.0.1)
Sprint planning and project management with Gitea integration.
- **Commands:** /sprint (plan|start|status|close|review|test), /project (initiation|plan|status|close), /adr (create|list|update|supersede), /rfc (create|list|review|approve|reject), /labels sync, /projman setup
- **Agents:** planner, orchestrator, executor, code-reviewer
- **MCP:** gitea

#### git-flow (v9.0.1)
Git workflow automation with smart commits and branch management.
- **Commands:** /gitflow (commit|branch-start|branch-cleanup|status|config)
- **Commit flags:** --push, --merge, --sync
- **Agents:** git-assistant
- **Hooks:** PreToolUse (branch-check.sh, commit-msg-check.sh)

#### pr-review (v9.0.1)
Multi-agent PR review with confidence scoring.
- **Commands:** /pr (review|summary|findings|diff|setup|init|sync)
- **Agents:** coordinator, security-reviewer, performance-analyst, maintainability-auditor, test-validator
- **MCP:** gitea

#### code-sentinel (v9.0.1)
Security scanning and code refactoring.
- **Commands:** /sentinel (scan|refactor|refactor-dry)
- **Agents:** security-reviewer, refactor-advisor
- **Hooks:** PreToolUse (security-check.sh)

#### doc-guardian (v9.0.1)
Documentation drift detection and synchronization.
- **Commands:** /doc (audit|sync|changelog-gen|coverage|stale-docs)
- **Agents:** doc-analyzer

#### clarity-assist (v9.0.1)
Prompt optimization with ND-friendly accommodations.
- **Commands:** /clarity (clarify|quick-clarify)
- **Agents:** clarity-coach
- **Hooks:** UserPromptSubmit (vagueness-check.sh)

#### contract-validator (v9.0.1)
Cross-plugin compatibility validation.
- **Commands:** /cv (validate|check-agent|list-interfaces|dependency-graph|setup|status)
- **Agents:** full-validation, agent-check
- **MCP:** contract-validator

#### claude-config-maintainer (v9.0.1)
CLAUDE.md and settings optimization.
- **Commands:** /claude-config (analyze|optimize|init|diff|lint|audit-settings|optimize-settings|permissions-map)
- **Agents:** maintainer

#### project-hygiene (v9.0.1)
Manual project file cleanup checks.
- **Commands:** /hygiene check (--fix flag for auto-fix)

### Data Domain

#### data-platform (v9.1.0)
pandas, PostgreSQL, and dbt integration with autonomous exploratory analytics.
- **Commands:** /data (ingest|profile|schema|explain|lineage|lineage-viz|run|dbt-test|quality|review|gate|setup)
- **Agents:**
  - **data-advisor** — Query planning and optimization suggestions
  - **data-analysis** — Autonomous analyst for exploration, hypothesis testing, and statistical discovery. Supports two modes: (1) Exploration Mode—five-phase methodology from schema discovery through hypothesis testing to insight synthesis; (2) Profiling Mode—quality scoring and threshold checks. Generates Jupyter notebooks with analytical narratives.
  - **data-ingestion** — Data loading and validation from external sources
- **MCP:** data-platform
- **New skills (v9.1.0):** data-exploration-workflow (5-phase analytical methodology), notebook-authoring (Jupyter cell patterns)

#### viz-platform (v9.1.0)
DMC validation, Plotly charts, theming, and analytical visualization for Jupyter notebooks.
- **Commands:** /viz (setup|chart|chart-export|dashboard|theme|theme-new|theme-css|component|accessibility-check|breakpoints|design-review|design-gate)
- **Agents:**
  - **design-reviewer** — Dash component and layout accessibility audits
  - **layout-builder** — Dashboard grid construction and responsiveness
  - **component-check** — DMC component validation and registry lookup
  - **theme-setup** — Theme generation and customization
- **MCP:** viz-platform
- **New skills (v9.1.0+):** analytical-chart-selection (graph_objects trace type selection guide), notebook-design-system (dark-theme design system for Plotly), choropleth-map-patterns (go.Choroplethmap tile-based map background control and valid styles)

#### data-seed (v0.1.0)
Test data generation and database seeding. *Scaffold — not yet implemented.*

### SaaS Domain

#### saas-api-platform (v0.1.0)
REST/GraphQL API scaffolding for FastAPI and Express. *Scaffold.*

#### saas-db-migrate (v0.1.0)
Database migration management for Alembic, Prisma, raw SQL. *Scaffold.*

#### saas-react-platform (v0.1.0)
React frontend toolkit for Next.js and Vite. *Scaffold.*

#### saas-test-pilot (v0.1.0)
Test automation for pytest, Jest, Vitest, Playwright. *Scaffold.*

### Ops Domain

#### cmdb-assistant (v9.0.1)
NetBox CMDB integration for infrastructure management.
- **Commands:** /cmdb (search|device|ip|site|audit|register|sync|topology|change-audit|ip-conflicts|setup)
- **Agents:** cmdb-assistant
- **MCP:** netbox
- **Hooks:** PreToolUse (validate-input.sh)

#### ops-release-manager (v0.1.0)
Release management with SemVer and changelog automation. *Scaffold.*

#### ops-deploy-pipeline (v0.1.0)
Deployment pipeline for Docker Compose and systemd. *Scaffold.*

### Debug Domain

#### debug-mcp (v0.1.0)
MCP server debugging and diagnostics. *Scaffold.*
