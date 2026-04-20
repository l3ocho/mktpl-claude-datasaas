# Canonical paths — v12.0.0

Authoritative reference for every directory and file in this repo. If a path isn't listed here, it shouldn't exist.

## Top-level

```
mktpl-claude-datasaas/
├── .claude/settings.json              # Per-project Claude Code settings (model, etc.)
├── .claude-plugin/marketplace.json    # Marketplace manifest (single profile)
├── .mcp.json                          # MCP server registration at repo root
├── .env                               # Per-project values (GITEA_ORG, GITEA_REPO, GIT_*)
├── .env.example                       # Template for .env
├── .gitignore
├── CLAUDE.md                          # Top-level project instructions
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .scratch/                          # Throwaway work — ignored by git
├── plugins/                           # 5 plugins (see below)
├── mcp-servers/                       # 3 shared MCP servers
├── docs/                              # This folder
└── scripts/                           # Setup, validation, release
```

**Allowed root files:** `CLAUDE.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`, `.env`, `.env.example`. Everything else must live under a subdirectory.

## `plugins/`

```
plugins/
├── projman/
│   ├── .claude-plugin/
│   │   ├── plugin.json
│   │   └── metadata.json              # {"domain": "core", "mcp_servers": ["gitea"]}
│   ├── claude-md-integration.md
│   ├── CONFIGURATION.md
│   ├── README.md
│   ├── commands/                      # 22 command .md files
│   ├── agents/                        # planner, orchestrator, executor, code-reviewer
│   └── skills/                        # SKILL.md subdirectories (v12.0.0+)
├── doc-guardian/
│   ├── .claude-plugin/{plugin,metadata}.json
│   ├── commands/                      # 6 command .md files
│   ├── agents/doc-analyzer.md
│   └── skills/                        # SKILL.md subdirectories
├── git-guardrails/
│   ├── .claude-plugin/{plugin,metadata}.json
│   ├── hooks/
│   │   ├── hooks.json
│   │   ├── branch-check.sh
│   │   └── commit-msg-check.sh
│   └── README.md
├── data-platform/
│   ├── .claude-plugin/{plugin,metadata}.json
│   ├── commands/                      # 13 commands
│   ├── agents/                        # data-advisor, data-analysis, data-ingestion
│   └── skills/
└── dmc-design/
    ├── .claude-plugin/{plugin,metadata}.json
    ├── commands/                      # 13 commands
    ├── agents/                        # design-reviewer, layout-builder
    └── skills/
```

## `mcp-servers/`

```
mcp-servers/
├── gitea/                             # Gitea integration (projman)
│   ├── run.sh
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── mcp_server/
├── data-platform/                     # pandas/PG/dbt tools
│   ├── run.sh
│   ├── pyproject.toml
│   └── mcp_server/
└── dmc-design/                        # DMC registry + validation
    ├── run.sh
    ├── pyproject.toml
    ├── mcp_server/
    └── registry/                      # Generated: dmc_X_Y.json
```

## `scripts/`

```
scripts/
├── setup.sh                           # Full setup (venvs, config, skill aliases)
├── setup-venvs.sh                     # Venv cache management (~/.cache/claude-mcp-venvs)
├── post-update.sh                     # Post-pull cache clear + changelog view
├── validate-marketplace.sh            # Validate all plugin manifests + file refs
├── verify-hooks.sh                    # Verify only 2 hooks exist in git-guardrails
├── install-plugin.sh                  # Install a plugin into a consumer project
├── uninstall-plugin.sh                # Remove a plugin from a consumer project
├── list-installed.sh                  # Show installed plugins in a project
├── install-skill-aliases.sh           # Install /sprint, /adr, etc. aliases to ~/.claude/skills
├── generate-dmc-refs.py               # Build DMC registry from llms.json
└── release.sh                         # Release automation (version bump + tag)
```

## `docs/`

```
docs/
├── ARCHITECTURE.md                    # System architecture, agent matrix, MCP inventory
├── CANONICAL-PATHS.md                 # This file
├── COMMANDS-CHEATSHEET.md             # All commands quick reference
├── CONFIGURATION.md                   # Env setup (Gitea, Postgres, git)
├── DEBUGGING-CHECKLIST.md             # Troubleshooting guide
├── UPDATING.md                        # How to update an installed marketplace
├── MIGRATION-v9.md                    # Historical: v8.x → v9.0.0
├── MIGRATION-v11.md                   # Historical: v10.x → v11.0.0 (viz-platform split)
└── MIGRATION-v12.md                   # v11.x → v12.0.0 (native-overlap removal)
```

## Installation paths (on a consumer's machine)

| Context | Path | Purpose |
|---|---|---|
| Source | `~/Projects/personal/mktpl-claude-datasaas/` | Edit here only |
| Installed | `~/.claude/plugins/marketplaces/mktpl-claude-datasaas/` | Runtime — never edit |
| Cache | `~/.claude/plugins/cache/mktpl-claude-datasaas/` | Plugin metadata snapshots; clear via `./scripts/post-update.sh` |
| Venvs | `~/.cache/claude-mcp-venvs/mktpl-claude-datasaas/` | Persistent MCP venvs |

## Plugin manifest schemas

### `plugin.json` (required in `.claude-plugin/`)

Strict Claude Code schema. Only these fields are allowed:

```json
{
  "name": "string",
  "version": "semver",
  "description": "string",
  "author": { "name": "string", "email": "string" },
  "homepage": "url",
  "repository": "url",
  "license": "string",
  "keywords": ["string"],
  "commands": ["./commands/"],
  "hooks": ["./hooks/hooks.json"]
}
```

Custom fields are forbidden. Domain/mcp_servers metadata moved to `metadata.json`.

### `metadata.json` (required in `.claude-plugin/`)

```json
{
  "domain": "core|data|saas|ops|debug",
  "mcp_servers": ["gitea"]
}
```

`domain` is required. `mcp_servers` lists MCP servers the plugin expects to be available at repo root.

### `hooks/hooks.json` (required if plugin has hooks)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/foo.sh" }
        ]
      }
    ]
  }
}
```

Only `PreToolUse` is allowed in v12.0.0. No `SessionStart`, `PostToolUse`, `UserPromptSubmit`, or prompt-type hooks.

## Version sync points

When cutting a release, these files must match:

| File | Where |
|---|---|
| Git tag | `vX.Y.Z` |
| `marketplace.json` | `metadata.version` |
| `README.md` | Title `# ... vX.Y.Z` |
| `CHANGELOG.md` | `## [X.Y.Z] - YYYY-MM-DD` |

`scripts/release.sh` handles all four.

## Forbidden locations

- `~/.claude/plugins/*` — never edit; always overwritten on reinstall.
- Editing `plugin.json` to include custom fields (schema will reject).
- Files at repo root not in the allowed list above.
- `hooks/*.sh` outside the `git-guardrails` plugin.
