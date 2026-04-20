---
name: projman setup
description: Configure projman - full setup, quick project init, sync, or migrate from v11
---

# Projman Setup

Unified setup command for all configuration needs.

**Important:**
- Uses Bash, Read, Write, AskUserQuestion — not MCP tools
- MCP tools don't work until after setup + session restart
- Tokens are entered manually for security

## Invocation

```
/projman setup              # Auto-detect appropriate mode
/projman setup --full       # Full wizard (MCP + system + project)
/projman setup --quick      # Project-only setup
/projman setup --sync       # Update after repo move
/projman setup --clear-cache # Clear plugin cache (between sessions only)
/projman setup migrate      # Guided migration from v11.x → v12.0.0
```

## Mode detection

If no argument, auto-detect:
1. `~/.config/claude/gitea.env` missing → **full**
2. Project `.env` missing → **quick**
3. `.env` disagrees with `git remote` → **sync**
4. Otherwise → offer reconfigure or exit

## Mode: full

Use the `setup-workflows` skill → Full Setup Workflow:
1. Environment validation (Python 3.10+)
2. MCP server setup (venv + requirements) for `gitea`, `data-platform`, `dmc-design`
3. System-level config (`~/.config/claude/gitea.env`)
4. Project-level config (`.env`)
5. Final validation

## Mode: quick

Use the `setup-workflows` skill → Quick Setup:
1. Verify system config exists
2. Verify git repository
3. Check existing `.env`
4. Detect org/repo from `git remote`
5. Validate via Gitea API
6. Create/update `.env`
7. Check `.gitignore`

## Mode: sync

Use the `setup-workflows` skill → Sync Workflow:
1. Read current config
2. Detect git remote
3. Compare values
4. Show changes
5. Validate new values
6. Update `.env`
7. Confirm

## Mode: clear-cache

Clear the plugin cache so configuration reloads fresh.

**WARNING:** only run between sessions, never mid-session. Clearing cache mid-session destroys MCP tool venv paths and breaks all MCP operations.

Steps:
1. Run: `rm -rf ~/.claude/plugins/cache/mktpl-claude-datasaas/`
2. Print: "Cache cleared. Restart Claude Code for changes to take effect."

Use after `git pull`/reinstall, when MCP servers show stale config, or when plugin changes don't take effect.

## Mode: migrate (v11.x → v12.0.0)

Run this after pulling v12.0.0 to understand what changed in your workflow.

### Step 1 — announce scope

Print a summary: v12 removed 16 plugins that duplicated Claude Code built-ins. Your existing projman sprints, wiki lessons, RFCs, and ADRs are untouched. What changed is which *commands* still exist.

### Step 2 — inventory old commands the user might type

For each removed command family, ask whether the user had it in muscle memory:

| If you used... | Now do... |
|---|---|
| `/pr review`, `/pr summary`, `/pr diff`, `/pr findings` | `/review` (local) or `/ultrareview` (cloud) |
| `/sentinel scan`, `/sentinel refactor`, `/sentinel refactor-dry` | `/security-review`; Claude refactors naturally in conversation |
| `/clarity clarify`, `/clarity quick-clarify` | Just describe the task — Opus 4.7 clarifies natively |
| `/claude-config init`, `analyze`, `optimize`, `lint`, `diff`, `permissions-map`, `baseline`, `drift-check`, `audit-settings`, `optimize-settings` | `/init`, `/config`, and Claude Code's native auto-memory |
| `/gitflow commit`, `branch-start`, `branch-cleanup`, `config`, `status`, `setup` | Plain git via Bash. Branch-name and commit-message validation now come from the `git-guardrails` hooks. |
| `/hygiene check` | Ask Claude directly: "clean up temp files and debug artifacts" |
| `/cv validate`, `status`, `check-agent`, `list-interfaces`, `dependency-graph` | `./scripts/validate-marketplace.sh` + `./scripts/verify-hooks.sh` |
| `/release prepare`, `validate`, `tag`, `rollback`, `status` | `./scripts/release.sh X.Y.Z` |
| `/deploy setup`, `generate`, `validate`, `env`, `check`, `rollback` | Manual deployment; Claude reads your `docker-compose.yml` / Caddyfile / systemd units directly |
| `/api scaffold`, `docs`, `middleware`, `validate`, `setup` | Ask Claude to scaffold — it reads your existing FastAPI/Express structure |
| `/db-migrate generate`, `plan`, `validate`, `setup` | Same — Claude reads your Alembic/Prisma config and generates directly |
| `/react component`, `route`, `state`, `hook`, `lint`, `setup` | Same — Claude reads your Next.js/Vite project and scaffolds |
| `/test generate`, `coverage`, `fixtures`, `e2e`, `run`, `setup` | Same |
| `/seed *` | Same |
| `/drawio parse`, `generate` | No replacement — feature removed |
| `/debug-mcp *` | Read the MCP server's log file directly |

### Step 3 — new habits to adopt

- Plan-then-execute is now native via `/plan <description>` or by cycling to plan mode with Shift+Tab. The `.claude/settings.json` already pins `"model": "opusplan"`, so Opus runs in plan phase and Sonnet in execution.
- `TodoWrite` is a native tool — the projman orchestrator and executor now use it automatically. You'll see live todo lists during sprints.
- Skill aliases are installed by `./scripts/install-skill-aliases.sh`. After v12 the short-form commands that still exist are: `/sprint`, `/adr`, `/project`, `/labels`, `/rfc`, `/projman`, `/doc`, `/data`, `/design`.

### Step 4 — environment sanity check

Run (as Bash):

```bash
./scripts/validate-marketplace.sh
./scripts/verify-hooks.sh
```

Both must exit `0`. If either fails, ask the user to share the output and stop.

### Step 5 — clear stale cache

```bash
./scripts/post-update.sh
```

Then print: "Restart Claude Code now. After restart, run `/sprint status` to verify projman is live."

### Step 6 — remove obsolete personal skill aliases (optional)

If the user previously ran the v11 alias installer, they have stale aliases at `~/.claude/skills/pr/`, `.../sentinel/`, `.../clarity/`, `.../claude-config/`, etc. Offer to delete them by running the refreshed `./scripts/install-skill-aliases.sh` (which only installs the 9 aliases that still make sense in v12) and then removing leftover subdirectories.

Ask for confirmation before deleting anything under `~/.claude/skills/`.

## Visual output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  ⚙️ SETUP                                                        ║
║  [Mode: Full | Quick | Sync | Clear-Cache | Migrate]             ║
╚══════════════════════════════════════════════════════════════════╝
```
