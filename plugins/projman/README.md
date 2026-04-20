# projman

Sprint planning and project management for Claude Code, backed by a Gitea MCP server.

## What it does

Gives you `/sprint plan → start → status → review → close`, project lifecycle commands (`/project *`), RFCs (`/rfc *`) and ADRs (`/adr *`) stored in Gitea wiki, lessons-learned capture and retrieval, and label-taxonomy sync.

## Agents (4)

| Agent | Model | Role |
|---|---|---|
| `planner` | opus | Thoughtful architecture analysis + issue creation; refuses L/XL tasks without breakdown |
| `orchestrator` | sonnet | Parallel dispatch, `TodoWrite` tracking, progress comments, lesson capture |
| `executor` | sonnet | Implementation — feature branch, tests, PR; `bypassPermissions` with git-guardrails + code-reviewer as safety nets |
| `code-reviewer` | opus | Read-only pre-close review (Write/Edit disallowed in frontmatter) |

## Commands

See `docs/COMMANDS-CHEATSHEET.md` in the marketplace root for the full list. Quick headliners:

- `/sprint plan`, `/sprint start`, `/sprint status`, `/sprint review`, `/sprint close`
- `/rfc create`, `/rfc list`, `/rfc approve`, `/rfc reject`
- `/adr create`, `/adr update`, `/adr supersede`, `/adr list`
- `/project initiation`, `/project plan`, `/project status`, `/project close`
- `/labels sync`
- `/projman setup`, `/projman setup migrate` (for v11 → v12)

## Setup

```
/projman setup
```

or from a shell:

```
cd mktpl-claude-datasaas
./scripts/setup.sh
```

## MCP server

Uses `gitea` at `mcp-servers/gitea/`. Set `GITEA_API_URL` + `GITEA_API_TOKEN` in `~/.config/claude/gitea.env`, and `GITEA_ORG` + `GITEA_REPO` in your project's `.env`.

## Configuration

See `plugins/projman/CONFIGURATION.md` and the marketplace-wide `docs/CONFIGURATION.md`.
