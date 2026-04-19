# Architecture — Leo Claude Marketplace v9.2.0

## Overview

Plugin marketplace for Claude Code. 21 plugins across 5 domains, 5 shared MCP servers,
3 PreToolUse safety hooks across 2 plugins.

## System Architecture

### Plugin Domains

| Domain | Purpose | Plugins |
|--------|---------|---------|
| core | Development workflow | projman, git-flow, pr-review, code-sentinel, doc-guardian, clarity-assist, contract-validator, claude-config-maintainer, project-hygiene |
| data | Data engineering | data-platform, viz-platform, drawio-plugin, data-seed |
| saas | SaaS development | saas-api-platform, saas-db-migrate, saas-react-platform, saas-test-pilot |
| ops | Operations | ops-release-manager, ops-deploy-pipeline |
| debug | Diagnostics | debug-mcp |

### MCP Servers (Shared at Root)

| Server | Plugins Using It | External System |
|--------|-------------------|-----------------|
| gitea | projman, pr-review | Gitea (issues, PRs, wiki) — uses published `gitea-mcp` package |
| data-platform | data-platform | PostgreSQL, dbt |
| viz-platform | viz-platform | DMC registry |
| contract-validator | contract-validator | (internal validation) |

### Hook Architecture

| Plugin | Event | Trigger | Script |
|--------|-------|---------|--------|
| code-sentinel | PreToolUse | Write\|Edit\|MultiEdit | security-check.sh |
| git-flow | PreToolUse | Bash (branch naming) | branch-check.sh |
| git-flow | PreToolUse | Bash (git commit) | commit-msg-check.sh |

No other hook types permitted. All workflow automation is via explicit commands.
UserPromptSubmit hooks removed in RFC-10 — native Opus 4.7/Sonnet 4.6 handles vague-prompt detection.

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
| ops | ops-release-manager, ops-deploy-pipeline |
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

#### code-sentinel (v10.0.0)
Code refactoring and automatic secrets detection. Full security audits use built-in `/security-review`.
- **Commands:** /sentinel (refactor|refactor-dry)
- **Agents:** refactor-advisor
- **Hooks:** PreToolUse (security-check.sh)

#### doc-guardian (v9.0.1)
Documentation drift detection and synchronization.
- **Commands:** /doc (audit|sync|changelog-gen|coverage|stale-docs)
- **Agents:** doc-analyzer

#### clarity-assist (v10.0.0)
Prompt optimization with ND-friendly accommodations.
- **Commands:** /clarity (clarify|quick-clarify)
- **Agents:** clarity-coach

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

#### viz-platform (v10.0.0)
DMC validation, Plotly charts, theming, and design-contract-driven layout for Dash/Jupyter projects.
- **Commands:** /viz (setup|chart|chart-export|dashboard|theme|breakpoints) — 6 commands total
- **Agents:**
  - **layout-builder** — Dashboard grid construction and responsiveness
- **MCP:** viz-platform (adds 5 new contract tools in v10.0.0)
- **Design Contract (v10.0.0):** Surface hierarchy resolver at `mcp-servers/viz-platform/resolver.py`. Consumer projects define `.claude/design-contract.json` during `/viz setup` Phase 3. The resolver enforces `base → raised → overlay → nested_in_overlay` surface tokens and component locks across all component-generating MCP tools. Contract wins over caller-supplied props. See `skills/theming-system.md` for full spec.
- **New MCP tools (v10.0.0):** `contract_load`, `contract_validate`, `contract_resolve_component`, `contract_lock_component`, `contract_get_surface`
- **Registry loading (v9.3.0+):** MCP server discovers `dmc_*.json` registry files dynamically via glob — no fixed filename. New registries generated by `generate-dmc-refs.py` are picked up automatically.
- **Skills (v9.1.0+):** analytical-chart-selection, notebook-design-system, choropleth-map-patterns, color-scheme-validation

#### drawio-plugin (v1.2.0)
Wireframe design tools bridging draw.io files and DMC scaffolding via viz-platform.
- **Commands:** /drawio (parse|generate)
- **Skills:** drawio-conventions, wireframe-schema, dmc-domain-files
- **References:** `references/dmc/` — AUTO-GENERATED DMC documentation. Files follow `dmc-*.txt` naming; the set is determined by `DOMAIN_CATEGORY_MAP` in `generate-dmc-refs.py`. Parser discovers files dynamically — no fixed list.
- **Output contract:** `/drawio parse` produces `WIREFRAME.md` — upstream input for viz-platform DMC scaffolding
- **Wireframe convention:** App project wireframes are stored in `docs/design/{project-name}.drawio`. The generated `WIREFRAME.md` lands in the same directory (`docs/design/WIREFRAME.md`). This folder is synced via Nextcloud and shared across all development environments.

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

#### ops-release-manager (v0.1.0)
Release management with SemVer and changelog automation. *Scaffold.*

#### ops-deploy-pipeline (v0.1.0)
Deployment pipeline for Docker Compose and systemd. *Scaffold.*

### Debug Domain

#### debug-mcp (v0.1.0)
MCP server debugging and diagnostics. *Scaffold.*
