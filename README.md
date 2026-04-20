# mktpl-claude-datasaas — v12.0.0

A focused Claude Code plugin marketplace: sprint management, documentation, data engineering, and a Dash + DMC design system.

**v12.0.0 is a major cleanup release.** 16 plugins were removed because Claude Code now covers their use cases natively (see [docs/MIGRATION-v12.md](docs/MIGRATION-v12.md)). What's left is what actually pulls its weight.

## The 5 plugins

| Plugin | Purpose |
|---|---|
| [`projman`](plugins/projman) | Sprint planning, RFCs, ADRs, lessons learned — backed by a Gitea MCP server |
| [`doc-guardian`](plugins/doc-guardian) | Documentation drift detection and sync |
| [`git-guardrails`](plugins/git-guardrails) | Two `PreToolUse(Bash)` hooks — branch-name and commit-message validation |
| [`data-platform`](plugins/data-platform) | Data engineering toolkit: pandas / PostgreSQL / dbt (MCP server) |
| [`dmc-design`](plugins/dmc-design) | Dash Mantine Components design system with validation MCP |

## Quick start

```bash
git clone <repo>
cd mktpl-claude-datasaas
./scripts/setup.sh                      # creates venvs, config templates, skill aliases
# Edit ~/.config/claude/gitea.env with a real token
./scripts/validate-marketplace.sh       # sanity check
./scripts/verify-hooks.sh               # sanity check
# Restart Claude Code
```

Then in any project that has `.env` with `GITEA_ORG` and `GITEA_REPO`, run:

```
/sprint status
```

## Key commands

| What you want to do | Command |
|---|---|
| Plan the next sprint | `/sprint plan` |
| Start executing | `/sprint start` |
| Check progress | `/sprint status` |
| Review code before close | `/sprint review` |
| Close the sprint | `/sprint close` |
| New RFC | `/rfc create` |
| New ADR | `/adr create` |
| Audit docs | `/doc audit` |
| Profile a dataset | `/data profile` |
| Scaffold a DMC component | `/design component` |

Full list: [docs/COMMANDS-CHEATSHEET.md](docs/COMMANDS-CHEATSHEET.md).

## Rely on Claude Code built-ins (don't reinvent)

| Task | Built-in |
|---|---|
| Project setup | `/init` |
| Security audit | `/security-review` |
| PR review | `/review` or `/ultrareview` |
| Plan mode | `/plan <description>` or Shift+Tab to cycle |
| Task tracking | `TodoWrite` (projman orchestrator uses it automatically) |

## Repo layout

```
plugins/        5 plugins (projman, doc-guardian, git-guardrails, data-platform, dmc-design)
mcp-servers/    3 MCP servers (gitea, data-platform, dmc-design)
docs/           Architecture, paths, commands, configuration, debugging, migration
scripts/        Setup, validation, release automation
.claude-plugin/ marketplace.json (single profile)
.mcp.json       MCP server registration
```

Full detail: [docs/CANONICAL-PATHS.md](docs/CANONICAL-PATHS.md).

## Documentation

| Topic | Doc |
|---|---|
| Architecture & agent matrix | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Paths & schemas | [docs/CANONICAL-PATHS.md](docs/CANONICAL-PATHS.md) |
| All commands | [docs/COMMANDS-CHEATSHEET.md](docs/COMMANDS-CHEATSHEET.md) |
| Configuration | [docs/CONFIGURATION.md](docs/CONFIGURATION.md) |
| Debugging | [docs/DEBUGGING-CHECKLIST.md](docs/DEBUGGING-CHECKLIST.md) |
| Updates | [docs/UPDATING.md](docs/UPDATING.md) |
| v11 → v12 migration | [docs/MIGRATION-v12.md](docs/MIGRATION-v12.md) |

## License

MIT. See [LICENSE](LICENSE).
