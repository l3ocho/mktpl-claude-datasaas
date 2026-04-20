# Updating the marketplace

How to update an installed marketplace when a new version ships.

## Normal update (minor / patch)

```bash
cd ~/Projects/personal/mktpl-claude-datasaas   # or wherever you cloned it
git pull origin main

./scripts/setup-venvs.sh --quick               # reuses cached venvs where requirements unchanged
./scripts/post-update.sh                       # clears ~/.claude/plugins/cache/mktpl-claude-datasaas
```

Then **restart Claude Code**. MCP servers and plugin settings only reload at session start.

## Major update

For v11.x → v12.0.0 specifically, follow `docs/MIGRATION-v12.md` step-by-step — 16 plugins were removed and some workflow commands changed.

For other major versions, check the corresponding `docs/MIGRATION-vX.md` file.

## Verify after update

```bash
./scripts/validate-marketplace.sh
./scripts/verify-hooks.sh
```

Both should exit `0`. If either fails, the marketplace is in a broken state — report the output.

## Updating a consumer project

A consumer project has `~/.claude/plugins/` populated from the marketplace install. After updating the marketplace:

```bash
# From inside the consumer project
./scripts/post-update.sh   # if the consumer has the script symlinked; otherwise run it from the marketplace directory
```

Consumer-project `.env` files are not touched. Your `GITEA_ORG`, `GITEA_REPO`, and `GIT_*` values survive.

## Rollback

```bash
cd ~/Projects/personal/mktpl-claude-datasaas
git checkout v11.0.0                           # or the previous known-good tag
./scripts/setup-venvs.sh                       # rebuild venvs for that version
./scripts/post-update.sh
```

Restart Claude Code.

## What gets cleared vs. preserved

| Location | On update | On rollback |
|---|---|---|
| `~/.claude/plugins/marketplaces/mktpl-claude-datasaas/` | Replaced | Replaced |
| `~/.claude/plugins/cache/mktpl-claude-datasaas/` | Cleared | Cleared |
| `~/.cache/claude-mcp-venvs/mktpl-claude-datasaas/` | Preserved (rebuilt incrementally) | Preserved |
| `~/.config/claude/*.env` | Untouched | Untouched |
| `<project>/.env` | Untouched | Untouched |
| `<project>/.claude/settings.json` | Untouched | Untouched |

## Never

- Never edit `~/.claude/plugins/marketplaces/mktpl-claude-datasaas/` — your edits are wiped on next update.
- Never force-push or rewrite history on the marketplace `main` branch — consumers will get broken pulls.
- Never use `--no-verify` to bypass the git-guardrails hooks.
