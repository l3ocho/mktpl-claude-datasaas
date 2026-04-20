# Architecture — v12.0.0

## Plugins (5)

| Plugin | Domain | Commands | Agents | Skills | MCP |
|---|---|---|---|---|---|
| `projman` | core | 22 | 4 | 31 | gitea |
| `doc-guardian` | core | 6 | 1 | 6 | — |
| `git-guardrails` | core | — | — | — | — (hooks only) |
| `data-platform` | data | 13 | 3 | 12 | data-platform |
| `dmc-design` | data | 13 | 2 | 9 | dmc-design |

## MCP servers (3)

| Server | Consumed by | Role |
|---|---|---|
| `gitea` | projman | Issues, milestones, labels, PRs, wiki (RFCs, lessons, ADRs) |
| `data-platform` | data-platform | pandas / PostgreSQL / PostGIS / dbt tools |
| `dmc-design` | dmc-design | Dash Mantine Components registry + validation |

Server paths: `mcp-servers/<name>/run.sh`. Registered at repo root in `.mcp.json`.

## Hooks (2)

| Plugin | Event | Matcher | Script | Purpose |
|---|---|---|---|---|
| `git-guardrails` | PreToolUse | Bash | `branch-check.sh` | Enforce `<type>/<desc>` branch naming |
| `git-guardrails` | PreToolUse | Bash | `commit-msg-check.sh` | Enforce Conventional Commits |

No SessionStart, PostToolUse, UserPromptSubmit, or prompt-type hooks are allowed (verified by `scripts/verify-hooks.sh`).

## Agent matrix (projman)

| Agent | Model | Permission mode | Purpose |
|---|---|---|---|
| `planner` | opus | `default` | Sprint planning, architecture analysis, issue creation, lesson search |
| `orchestrator` | sonnet | `acceptEdits` | Sprint execution, parallel batching, git ops, lesson capture |
| `executor` | sonnet | `bypassPermissions` | Implementation; has safety net of git-guardrails hooks + code-reviewer |
| `code-reviewer` | opus | `default` (disallowedTools: Write/Edit) | Pre-close quality review |

Agents in other plugins follow the same schema; see each plugin's `agents/` directory.

**Note:** `.claude/settings.json` uses `"model": "opusplan"` so Claude Code runs Opus during plan phase and Sonnet during execution automatically. Projman agents keep per-agent model overrides where they matter.

## Gitea MCP tool inventory (projman)

| Category | Tools |
|---|---|
| Issues | `list_issues`, `get_issue`, `create_issue`, `update_issue`, `add_comment`, `aggregate_issues` |
| Labels | `get_labels`, `suggest_labels`, `create_label`, `create_label_smart` |
| Milestones | `list_milestones`, `get_milestone`, `create_milestone`, `update_milestone`, `delete_milestone` |
| Dependencies | `list_issue_dependencies`, `create_issue_dependency`, `remove_issue_dependency`, `get_execution_order` |
| Wiki | `list_wiki_pages`, `get_wiki_page`, `create_wiki_page`, `update_wiki_page`, `create_lesson`, `search_lessons`, `allocate_rfc_number` |
| PRs | `list_pull_requests`, `get_pull_request`, `get_pr_diff`, `get_pr_comments`, `create_pr_review`, `add_pr_comment` |
| Validation | `validate_repo_org`, `get_branch_protection` |

## Branch security posture

| Branch pattern | Mode | Allowed |
|---|---|---|
| `development`, `feat/*`, `fix/*`, `claude/*` | Development | Full access |
| `staging` | Staging | Read-only code, can create issues |
| `main`, `master` | Production | Read-only, emergency only |

## Configuration layers

| Level | Path | Content |
|---|---|---|
| System | `~/.config/claude/gitea.env` | `GITEA_API_URL`, `GITEA_API_TOKEN` |
| System | `~/.config/claude/postgres.env` | (optional) `POSTGRES_URL` for data-platform |
| System | `~/.config/claude/git-flow.env` | (optional) git workflow defaults |
| Project | `.env` at repo root | `GITEA_ORG`, `GITEA_REPO`, `GIT_*` per-project overrides |
| Project | `.claude/settings.json` | Per-project Claude Code settings (model, permissions) |

## RFC / ADR / Sprint lifecycle

- **RFCs** live in Gitea wiki as `RFC-NNNN: <title>`, indexed by `RFC-Index`. States: `Draft → Review → Approved → Implementing → Implemented`. Projman's `/sprint plan` detects approved RFCs and offers selection.
- **ADRs** live in wiki as `ADR-NNNN: <title>`, managed via `/adr create|update|supersede|list`.
- **Sprints** are Gitea milestones. `/sprint plan → start → status → review → close`. Lessons learned are captured to wiki on close and searched on start.

## Label taxonomy

Organization and repository labels total 58: Agent/Complexity/Efforts/Priority/Risk/Source/Status/Type (org) + Component/Tech/Domain/Epic/RnD (repo). Sync with `/labels sync`.

## Versioning

SemVer + Keep a Changelog. In-flight work sits under `## [Unreleased]` in `CHANGELOG.md`. `scripts/release.sh X.Y.Z` cuts the release — bumps `marketplace.json`, `README.md` title, commits, and tags.

## Directory layout

See `docs/CANONICAL-PATHS.md` for the authoritative path reference.
