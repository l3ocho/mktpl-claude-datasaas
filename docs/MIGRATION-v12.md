# Migration: v11.x → v12.0.0

v12.0.0 is a major cleanup release. **16 plugins were removed** because Claude Code now covers their use cases natively, and their prompts were a measurable drag on context. What remains is what actually pulls its weight.

Nothing in your Gitea (issues, RFCs, ADRs, lessons-learned wiki, milestones) is affected. Only the plugin surface changes.

## TL;DR

1. `git pull && ./scripts/setup-venvs.sh --quick && ./scripts/post-update.sh`
2. Restart Claude Code.
3. Run `/projman setup migrate` inside Claude Code for a guided walkthrough of which old commands you used and what replaces them.
4. Run `./scripts/validate-marketplace.sh` and `./scripts/verify-hooks.sh` to confirm health.

## What was removed

| Removed plugin | Why |
|---|---|
| `pr-review` | `/review` and `/ultrareview` are native |
| `code-sentinel` | `/security-review` is native |
| `clarity-assist` | Opus 4.7 clarifies natively in conversation |
| `claude-config-maintainer` | `/init`, `/config`, and native auto-memory cover it |
| `contract-validator` | `./scripts/validate-marketplace.sh` does the static check |
| `project-hygiene` | Just ask Claude |
| `git-flow` | Native git + the two surviving hooks moved to `git-guardrails` |
| `drawio-plugin` | Never had a working backend — removed |
| `data-seed` | Claude generates seed data directly from schemas |
| `saas-api-platform` | Prescriptive REST style guide; Claude already knows REST |
| `saas-db-migrate` | Same — Alembic/Prisma workflow notes Claude can derive |
| `saas-react-platform` | Prescriptive React style guide |
| `saas-test-pilot` | Prescriptive testing manual |
| `ops-release-manager` | `./scripts/release.sh` covers it |
| `ops-deploy-pipeline` | Claude reads your compose/Caddy/systemd configs directly |
| `debug-mcp` | Read the server log file |

## What's new

- `git-guardrails` — a hook-only plugin carrying the two useful scripts from the retired `git-flow`: branch-name check + commit-message check. No commands.
- `/projman setup migrate` — guided walkthrough of which of your old commands have replacements.
- `TodoWrite` — now used by the projman orchestrator and executor so you can see the live task list.
- Projman skills converted to the real Claude Code SKILL.md format so they load lazily instead of eagerly.
- Top-level `CLAUDE.md` trimmed from 570 → ~100 lines.

## Command mapping (full table)

| Old command | New thing |
|---|---|
| `/pr review` | `/review` (local) or `/ultrareview` (cloud) |
| `/pr summary` | `/review` summarizes natively |
| `/pr diff`, `/pr findings`, `/pr sync`, `/pr init`, `/pr setup` | Use `/review` or standard git tooling |
| `/sentinel scan` | `/security-review` |
| `/sentinel refactor`, `/sentinel refactor-dry` | Ask Claude directly |
| `/clarity clarify`, `/clarity quick-clarify` | Describe the task — Opus 4.7 clarifies in-line |
| `/claude-config init` | `/init` |
| `/claude-config analyze`, `lint`, `optimize`, `diff`, `permissions-map`, `baseline`, `drift-check`, `audit-settings`, `optimize-settings` | `/config` + auto-memory |
| `/gitflow commit` | Plain `git commit -m "..."` — the `git-guardrails` hook enforces Conventional Commits format |
| `/gitflow branch-start`, `branch-cleanup` | Plain `git checkout -b ...` — the hook enforces naming |
| `/gitflow status`, `config`, `setup` | Plain `git status` / direct env editing |
| `/hygiene check` | "Claude, clean up temp files and debug artifacts" |
| `/cv validate`, `status`, `check-agent`, `list-interfaces`, `dependency-graph`, `setup` | `./scripts/validate-marketplace.sh` + `./scripts/verify-hooks.sh` |
| `/release prepare`, `validate`, `tag`, `rollback`, `status` | `./scripts/release.sh X.Y.Z` |
| `/deploy *` | Claude reads your compose/Caddy/systemd files directly |
| `/api *`, `/db-migrate *`, `/react *`, `/test *`, `/seed *` | Describe what you want — Claude works from your project's actual config |
| `/drawio parse`, `generate` | Removed — no replacement |
| `/debug-mcp *` | Read the MCP server log |

Projman commands are unchanged: `/sprint plan|start|status|review|close|test`, `/project *`, `/adr *`, `/rfc *`, `/labels sync`, `/projman setup`.

doc-guardian, data-platform, dmc-design commands are unchanged. Only their internal skills folders were restructured (transparent to users).

## Hooks

Before: 3 hooks across 2 plugins (`code-sentinel` security-check, `git-flow` branch-check + commit-msg-check).

After: 2 hooks in `git-guardrails`:

| Hook | Purpose |
|---|---|
| `branch-check.sh` | Block `git checkout -b` / `git switch -c` for invalid names |
| `commit-msg-check.sh` | Block `git commit -m` if not Conventional Commits |

The pre-write security scan from `code-sentinel` is gone. If you specifically want a commit-time secrets scan, add a git pre-commit hook in your consumer project — don't put it in a Claude Code PreToolUse hook.

## Personal skill aliases

`./scripts/install-skill-aliases.sh` previously installed 24 short-form aliases (`/pr`, `/sentinel`, `/clarity`, `/claude-config`, `/cv`, `/api`, `/db-migrate`, `/react`, `/test`, `/seed`, `/release`, `/deploy`, `/debug-mcp`, `/gitflow`, `/hygiene`, ...). Now it installs 9: `/sprint`, `/adr`, `/project`, `/labels`, `/rfc`, `/projman`, `/doc`, `/data`, `/design`.

Re-run the script to refresh:

```bash
./scripts/install-skill-aliases.sh
```

Manually remove any stale `~/.claude/skills/<name>/` directories you no longer need. Nothing enforces this — they just become dead entries.

## Token / context impact

Before v12.0.0, a typical projman sprint session loaded:
- `CLAUDE.md` at ~27 KB
- ~16 plugins' `claude-md-integration.md` contents referenced across docs
- projman agents eagerly preloading 4+ skills each via "Phase X skills" body text
- Approximately 4,100 lines of projman skill content loaded before any work began

After v12.0.0:
- `CLAUDE.md` ~3 KB (~100 lines)
- 5 plugins
- Projman agents load 4–7 safety-critical skills via frontmatter, everything else is lazy via SKILL.md description-based invocation

Expect a noticeable drop in how often context gets compressed.

## What didn't change

- `.env` schema — still `GITEA_ORG`, `GITEA_REPO`, `GIT_*`
- `~/.config/claude/gitea.env`, `postgres.env`, `git-flow.env` schemas
- Gitea wiki layout (`RFC-Index`, `ADR-NNNN: …`, `lessons-learned/sprints/...`)
- Sprint milestone conventions
- Label taxonomy
- Agent frontmatter schema — `name`, `description`, `model`, `permissionMode`, `skills`, `disallowedTools`

## Rolling back

If v12.0.0 breaks your workflow, check out the last v11 tag:

```bash
cd ~/Projects/personal/mktpl-claude-datasaas
git checkout v11.0.0
./scripts/setup-venvs.sh
./scripts/post-update.sh
```

Then restart Claude Code. File an issue describing what broke so the v12.x series can fix it without you having to stay on v11.

## Quick post-migrate checklist

- [ ] `./scripts/validate-marketplace.sh` exits 0
- [ ] `./scripts/verify-hooks.sh` exits 0
- [ ] `/sprint status` runs (confirms projman + gitea MCP is live)
- [ ] `/doc audit` runs (confirms doc-guardian)
- [ ] `/data profile` against a small CSV runs (confirms data-platform MCP)
- [ ] `/design setup` runs (confirms dmc-design MCP)
- [ ] A feature-branch creation with a bad name is blocked (confirms git-guardrails)
- [ ] A non-Conventional-Commits message is blocked (confirms git-guardrails)
