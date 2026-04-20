# CLAUDE.md

Project instructions for Claude Code when working on this marketplace.

## Non-negotiable rules

| Rule | What it means |
|---|---|
| **Never edit `~/.claude/plugins/`** | That's the installed copy. All changes go to source under this repo. The installed copy is overwritten on every update. |
| **Never push to protected branches** | `main`, `master`, `development` — feature-branch → PR only. If you accidentally commit to one locally, branch off and reset. |
| **Never use CLI for external services** | No `gh`, `tea`, or `curl` to Gitea/GitHub APIs. Use MCP tools (`mcp__plugin_projman_gitea__*`). |
| **Never bypass hooks** | No `--no-verify`, `--no-gpg-sign`. If a hook fails, fix the cause. |
| **Allowed root files only** | `CLAUDE.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.env.example`. Everything else lives under `plugins/`, `docs/`, `scripts/`, `mcp-servers/`, `.claude-plugin/`, or `.scratch/` for throwaway work. |
| **`plugin.json` lives in `.claude-plugin/`** | Not in the plugin root. Hooks go in `hooks/hooks.json`, never inline in `plugin.json`. |
| **Verify before "done"** | Run the relevant validator (`scripts/validate-marketplace.sh`, `scripts/verify-hooks.sh`) and show output. |

Full path and schema reference: `docs/CANONICAL-PATHS.md`.

## Repository layout (source of truth)

- `plugins/` — 5 plugins: `projman`, `data-platform`, `dmc-design`, `doc-guardian`, `git-guardrails`
- `mcp-servers/` — 3 MCP servers: `gitea`, `data-platform`, `dmc-design`
- `.claude-plugin/marketplace.json` — single marketplace manifest (no profiles as of v12.0.0)
- `.mcp.json` — MCP server registration at repo root
- `scripts/` — setup, validation, release automation
- `docs/` — architecture, commands, configuration, debugging, migration guides

## Plugin inventory (v12.0.0)

| Plugin | Domain | Purpose |
|---|---|---|
| `projman` | core | Sprint planning, project/RFC/ADR workflow, Gitea integration |
| `doc-guardian` | core | Documentation drift detection |
| `git-guardrails` | core | Pre-commit branch-name + commit-message hooks only |
| `data-platform` | data | pandas/PostgreSQL/dbt MCP toolkit |
| `dmc-design` | data | Dash Mantine Components design system + validation MCP |

**Deleted in v12.0.0:** `pr-review`, `code-sentinel`, `clarity-assist`, `claude-config-maintainer`, `contract-validator`, `project-hygiene`, `git-flow`, `drawio-plugin`, `data-seed`, `saas-api-platform`, `saas-db-migrate`, `saas-react-platform`, `saas-test-pilot`, `ops-release-manager`, `ops-deploy-pipeline`, `debug-mcp`. Each was replaced by a Claude Code built-in or removed as prescriptive overhead. See `docs/MIGRATION-v12.md`.

## Built-ins we rely on (don't re-implement)

| Instead of (old plugin) | Use (built-in) |
|---|---|
| `/sentinel scan` | `/security-review` |
| `/pr review` | `/review` (local) or `/ultrareview` (cloud) |
| `/claude-config init` | `/init` + native auto-memory |
| `/gitflow commit` | Plain git via Bash — Claude writes good commits natively |
| `/hygiene check` | Ask Claude directly |
| `/clarity clarify` | Opus 4.7 clarifies natively in conversation |
| Manual task tracking | `TodoWrite` |
| Manual plan/execute split | `opusplan` model alias (already set in `.claude/settings.json`) |

## Plugins we build vs. plugins we use here

Since this IS the marketplace, we develop plugin source *and* dogfood them. When editing source, work under `plugins/<name>/`. When running commands like `/sprint plan`, you're using the installed copy — **never edit there**.

## Two-level configuration

| Level | Location | Purpose |
|---|---|---|
| System | `~/.config/claude/gitea.env` | Gitea credentials (`GITEA_API_URL`, `GITEA_API_TOKEN`) |
| Project | `.env` at repo root | Per-project values (`GITEA_ORG`, `GITEA_REPO`, git workflow config) |

## Branch security posture

| Branch pattern | Mode |
|---|---|
| `development`, `feat/*`, `fix/*`, `claude/*` | Development — full access |
| `staging` | Read-only code, can create issues |
| `main`, `master` | Read-only, emergency only |

## Before any breaking code change

1. Grep for the pattern you're changing — find all callers.
2. List files to modify and files you verified don't need changes.
3. After the change, grep again to prove no stale references remain.

Use judgment — trivial edits don't need a full audit.

## Development workflow

- Feature branch → commit → PR via Gitea MCP — never push to protected branches.
- After any change that touches plugin code, MCP servers, or hooks: ask the user to restart the Claude Code session. Do NOT clear cache mid-session.
- Run `./scripts/validate-marketplace.sh` before opening a PR.

## Versioning

SemVer + Keep a Changelog. All in-flight work sits under `## [Unreleased]` in `CHANGELOG.md`. Releases are cut with `./scripts/release.sh X.Y.Z` — it rewrites the Unreleased header, bumps `marketplace.json` and `README.md` title, commits, and tags.

## Further reading

| Topic | Doc |
|---|---|
| Full architecture and agent matrix | `docs/ARCHITECTURE.md` |
| Authoritative path reference | `docs/CANONICAL-PATHS.md` |
| Command cheatsheet | `docs/COMMANDS-CHEATSHEET.md` |
| Config setup | `docs/CONFIGURATION.md` |
| Troubleshooting | `docs/DEBUGGING-CHECKLIST.md` |
| Update procedure | `docs/UPDATING.md` |
| v11 → v12 migration | `docs/MIGRATION-v12.md` |
