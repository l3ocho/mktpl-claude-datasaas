# Configuration guide — v12.0.0

Everything you need to configure to make the 5 plugins + 3 MCP servers work.

## Two-layer config

- **System-level** (`~/.config/claude/*.env`) — credentials, one per machine.
- **Project-level** (`.env` at repo root + `.claude/settings.json`) — per-project overrides.

Projman reads both. Data-platform reads `postgres.env` optionally. Git-guardrails reads `git-flow.env` optionally.

## Required files

### `~/.config/claude/gitea.env`

```bash
GITEA_API_URL=https://gitea.example.com/api/v1
GITEA_API_TOKEN=ghp_xxxxxxxxxxxxxxxx
```

Permissions: `chmod 600`. `./scripts/setup.sh` creates a template.

### `<project>/.env`

```bash
GITEA_ORG=personal-projects
GITEA_REPO=mktpl-claude-datasaas

# Git-guardrails defaults (optional — see git-flow.env section below)
GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=main
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_PUSH=true
GIT_PROTECTED_BRANCHES=main
```

### `<project>/.claude/settings.json`

```json
{
  "model": "opusplan"
}
```

`opusplan` runs Opus in plan phase, Sonnet in execution. Recommended for projman workflows. You can override per-agent in agent frontmatter.

## Optional files

### `~/.config/claude/postgres.env` (for data-platform)

```bash
POSTGRES_URL=postgresql://user:password@localhost:5432/database
```

### `~/.config/claude/git-flow.env` (global git defaults)

```bash
GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_PUSH=false
GIT_PROTECTED_BRANCHES=main,master,development,staging,production
GIT_COMMIT_STYLE=conventional
GIT_CO_AUTHOR=true
```

Project-level `.env` values override these.

### `<project>/.claude/dmc-components.json` (for dmc-design)

Filter which DMC components end up in the generated registry:

```json
{
  "components": ["Button", "TextInput", "Select"],
  "categories": ["Layout", "Navigation"]
}
```

Empty = include everything.

## First-time setup flow

```bash
cd /path/to/mktpl-claude-datasaas
./scripts/setup.sh
```

What it does:

1. Creates/activates venvs under `~/.cache/claude-mcp-venvs/mktpl-claude-datasaas/` for the 3 MCP servers.
2. Writes `~/.config/claude/gitea.env`, `postgres.env`, `git-flow.env` if missing.
3. Verifies `.mcp.json` exists at repo root.
4. Installs personal skill aliases (`/sprint`, `/adr`, etc.) to `~/.claude/skills/`.
5. Prints a `TODO` list for anything that still needs manual attention (e.g., "fill in `GITEA_API_TOKEN`").

You still need to:

- Edit `~/.config/claude/gitea.env` and fill in a real token.
- In any consumer project, create `.env` with `GITEA_ORG` and `GITEA_REPO`.
- Restart Claude Code so the new MCP servers load.

## After an update

```bash
git pull
./scripts/setup-venvs.sh --quick   # reuses unchanged venvs
./scripts/post-update.sh           # clears plugin cache
```

Then restart Claude Code.

## Migrating from v11.x

See `docs/MIGRATION-v12.md` or run `/projman setup migrate` inside a Claude Code session.

## Troubleshooting

See `docs/DEBUGGING-CHECKLIST.md`. The common symptoms:

| Symptom | Likely cause | Fix |
|---|---|---|
| "X MCP servers failed to start" | Venv missing | `./scripts/setup-venvs.sh` |
| `/sprint` command not found | Skill aliases not installed, or session not restarted | `./scripts/install-skill-aliases.sh` then restart |
| Edits didn't take effect | Editing source vs. installed path | Edit source, reinstall / `./scripts/post-update.sh`, restart |
| Branch-check or commit-msg hook blocks | Branch name or commit message invalid | Fix the name/message — don't bypass |
