# Commands cheatsheet — v12.0.0

Quick reference for every command across the 5 plugins. Use the fully-qualified `/projman:sprint` form, or install the short aliases via `./scripts/install-skill-aliases.sh` so `/sprint` works directly.

## projman (22 commands)

### Setup
| Command | Purpose |
|---|---|
| `/projman setup` | Initial setup — Gitea token, labels, per-project `.env` |
| `/projman setup --full` | Full setup including label sync |
| `/projman setup --quick` | Config-only, skip label sync |
| `/projman setup --sync` | Resync after repo move/rename |
| `/projman setup migrate` | **New in v12** — migrate from v11 (remove obsolete commands from muscle memory) |

### Sprint lifecycle
| Command | Purpose |
|---|---|
| `/sprint plan` | Plan next sprint — AI-guided architecture, lesson search, issue creation |
| `/sprint start` | Begin execution — load relevant lessons from prior sprints |
| `/sprint status` | Progress view, blockers. `--diagram` for dependency graph |
| `/sprint review` | Pre-close quality review (delegates to `code-reviewer` agent) |
| `/sprint close` | Close sprint, capture lessons to wiki |
| `/sprint test` | Run tests with coverage, or generate tests for code |

### Project lifecycle
| Command | Purpose |
|---|---|
| `/project initiation` | Charter a new project (WBS, risks, roadmap) |
| `/project plan` | Create WBS, risk register, sprint roadmap |
| `/project status` | Hierarchy view of project/epics/sprints/issues |
| `/project close` | Archive a completed project with retrospective |

### ADR
| Command | Purpose |
|---|---|
| `/adr create` | New Architecture Decision Record in wiki |
| `/adr list` | List ADRs by status |
| `/adr update` | Update an ADR's content or status |
| `/adr supersede` | Supersede an ADR with a newer one |

### RFC
| Command | Purpose |
|---|---|
| `/rfc create` | New RFC in wiki (`RFC-NNNN: <title>`) |
| `/rfc list` | Show RFCs by status |
| `/rfc review` | Move RFC to Review state |
| `/rfc approve` | Approve an RFC |
| `/rfc reject` | Reject with reason |

### Labels
| Command | Purpose |
|---|---|
| `/labels sync` | Fetch Gitea labels, create missing required labels |

## doc-guardian (6 commands)

| Command | Purpose |
|---|---|
| `/doc audit` | Scan for drift between docs and code |
| `/doc sync` | Propose or apply drift fixes |
| `/doc changelog-gen` | Generate CHANGELOG entry from recent commits |
| `/doc coverage` | Show documentation coverage metrics |
| `/doc stale-docs` | Identify stale documentation |

## data-platform (13 commands)

| Command | Purpose |
|---|---|
| `/data setup` | Initialize data-platform config |
| `/data ingest` | Ingest CSV/Parquet into a pandas/PG target |
| `/data profile` | Profile a dataset (nulls, uniqueness, types) |
| `/data schema` | Extract schema from a dataset |
| `/data explain` | Explain SQL or pandas code |
| `/data quality` | Data quality gates |
| `/data gate` | Hard-block on quality issues |
| `/data review` | Review a data pipeline |
| `/data run` | Run a dbt / pandas / SQL job |
| `/data lineage` | Show dataset lineage |
| `/data lineage-viz` | Visualize lineage as a graph |
| `/data dbt-test` | Run `dbt test` with grouped output |

## dmc-design (13 commands)

| Command | Purpose |
|---|---|
| `/design setup` | Initialize design config (`.claude/dmc-components.json`) |
| `/design theme` | Generate / validate theme |
| `/design component` | Scaffold a DMC component |
| `/design pattern` | Enforce a design pattern |
| `/design accessibility` | Accessibility validation |
| `/dash dashboard` | Generate a Dash dashboard skeleton |
| `/dash page` | New Dash page + route |
| `/dash breakpoints` | Responsive breakpoint helpers |
| `/chart create` | Create a Plotly chart with validation |
| `/chart export` | Export a chart (PNG/HTML) |

## git-guardrails

No commands — hooks only. See `plugins/git-guardrails/README.md`.

## Claude Code built-ins we rely on

| Command | Purpose |
|---|---|
| `/init` | Initialize CLAUDE.md (replaces `/claude-config init`) |
| `/review` | Local PR review (replaces `/pr review`) |
| `/ultrareview` | Cloud-based PR review |
| `/security-review` | Full security audit (replaces `/sentinel scan`) |
| `/agents` | Manage subagents |
| `/plan <desc>` | Enter plan mode |
| `/clear`, `/compact` | Context management |
| `/config` | Settings UI |
| `/fast` | Toggle fast mode |

## Removed in v12.0.0

These commands no longer exist. Use the Claude Code built-in listed under each:

| Removed | Replacement |
|---|---|
| `/pr *` | `/review` / `/ultrareview` |
| `/sentinel scan`, `/sentinel refactor` | `/security-review` + natural conversation |
| `/clarity *` | Opus 4.7 natively clarifies prompts |
| `/claude-config *` | `/init`, `/config`, native auto-memory |
| `/gitflow commit`, `/gitflow branch-start`, etc. | Plain git via Bash — Claude writes good commits natively; `git-guardrails` hooks catch bad branches/messages |
| `/hygiene check` | Ask Claude directly |
| `/cv *` (contract-validator) | `./scripts/validate-marketplace.sh` |
| `/debug-mcp *` | Read MCP server logs |
| `/release *`, `/deploy *` | `./scripts/release.sh`, manual deployment |
| `/api *`, `/db-migrate *`, `/react *`, `/test *`, `/seed *` | — (scaffold plugins removed; Claude works directly from project code) |
| `/drawio parse`, `/drawio generate` | — (no replacement — feature removed) |
