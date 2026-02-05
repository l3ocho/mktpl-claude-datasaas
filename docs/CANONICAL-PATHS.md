# Canonical Paths - SINGLE SOURCE OF TRUTH

**This file defines ALL valid paths in this repository. No exceptions. No inference. No assumptions.**

Last Updated: 2026-02-04 (v7.1.0)

---

## Repository Root Structure

```
leo-claude-mktplace/
├── .claude/                    # Claude Code local settings
├── .claude-plugin/             # Marketplace manifest
│   ├── marketplace.json
│   ├── marketplace-lean.json   # Lean profile (6 core plugins)
│   └── marketplace-full.json   # Full profile (all plugins)
├── .mcp-lean.json              # Lean profile MCP config (gitea only)
├── .mcp-full.json              # Full profile MCP config (all servers)
├── .scratch/                   # Transient work (auto-cleaned)
├── docs/                       # All documentation
│   ├── architecture/           # Draw.io diagrams and specs
│   ├── prompts/                # Shared prompt templates
│   │   └── INDEX.md            # Prompt template index
│   ├── project-lessons-learned/ # Project-level lessons (not sprint-specific)
│   │   └── INDEX.md            # Lessons index
│   ├── CANONICAL-PATHS.md      # This file - single source of truth
│   ├── COMMANDS-CHEATSHEET.md  # All commands quick reference
│   ├── CONFIGURATION.md        # Centralized configuration guide
│   ├── DEBUGGING-CHECKLIST.md  # Systematic troubleshooting guide
│   └── UPDATING.md             # Update guide
├── hooks/                      # Shared hooks (if any)
├── mcp-servers/                # SHARED MCP servers (v3.0.0+)
│   ├── gitea/                  # Gitea MCP server
│   │   ├── mcp_server/
│   │   │   ├── server.py
│   │   │   ├── gitea_client.py
│   │   │   ├── config.py
│   │   │   └── tools/
│   │   │       ├── issues.py
│   │   │       ├── labels.py
│   │   │       ├── wiki.py
│   │   │       ├── milestones.py
│   │   │       ├── dependencies.py
│   │   │       └── pull_requests.py  # NEW in v3.0.0
│   │   ├── requirements.txt
│   │   └── .venv/
│   ├── netbox/                 # NetBox MCP server
│   │   ├── mcp_server/
│   │   ├── requirements.txt
│   │   └── .venv/
│   ├── data-platform/          # Data engineering MCP (NEW v4.0.0)
│   │   ├── mcp_server/
│   │   │   ├── server.py
│   │   │   ├── pandas_tools.py
│   │   │   ├── postgres_tools.py
│   │   │   └── dbt_tools.py
│   │   ├── requirements.txt
│   │   └── .venv/
│   ├── contract-validator/     # Contract validation MCP (NEW v5.0.0)
│   │   ├── mcp_server/
│   │   │   ├── server.py
│   │   │   ├── parse_tools.py
│   │   │   ├── validation_tools.py
│   │   │   └── report_tools.py
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── .venv/
│   └── viz-platform/           # Visualization MCP (NEW v4.1.0)
│       ├── mcp_server/
│       │   ├── server.py
│       │   ├── config.py
│       │   ├── component_registry.py
│       │   ├── dmc_tools.py
│       │   ├── chart_tools.py
│       │   ├── layout_tools.py
│       │   ├── theme_tools.py
│       │   ├── theme_store.py
│       │   └── page_tools.py
│       ├── registry/           # DMC component JSON registries
│       ├── tests/              # 94 tests
│       ├── requirements.txt
│       └── .venv/
├── plugins/                    # ALL plugins
│   ├── projman/                # Sprint management
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── doc-guardian/           # Documentation drift detection
│   │   ├── .claude-plugin/
│   │   ├── hooks/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── code-sentinel/          # Security scanning & refactoring
│   │   ├── .claude-plugin/
│   │   ├── hooks/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── cmdb-assistant/         # NetBox CMDB integration
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   └── claude-md-integration.md
│   ├── claude-config-maintainer/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   └── claude-md-integration.md
│   ├── project-hygiene/
│   │   ├── .claude-plugin/
│   │   ├── hooks/
│   │   └── claude-md-integration.md
│   ├── clarity-assist/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── git-flow/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── pr-review/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── data-platform/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── hooks/
│   │   └── claude-md-integration.md
│   ├── contract-validator/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   └── claude-md-integration.md
│   └── viz-platform/
│       ├── .claude-plugin/
│       ├── commands/
│       ├── agents/
│       ├── hooks/
│       └── claude-md-integration.md
├── scripts/                    # Setup and maintenance scripts
│   ├── setup.sh                # Initial setup (create venvs, config templates)
│   ├── post-update.sh          # Post-update (clear cache, show changelog)
│   ├── check-venv.sh           # Check if venvs exist (read-only)
│   ├── validate-marketplace.sh # Marketplace compliance validation
│   ├── verify-hooks.sh         # Verify all hooks use correct event types
│   ├── setup-venvs.sh          # Setup MCP server venvs (create only, never delete)
│   ├── release.sh              # Release automation with version bumping
│   ├── claude-launch.sh        # Task-specific launcher with profile selection
│   └── switch-profile.sh       # DEPRECATED: use claude-launch.sh instead
├── CLAUDE.md
├── README.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore
```

---

## Path Patterns (MANDATORY)

### Plugin Paths

| Context | Pattern | Example |
|---------|---------|---------|
| Plugin location | `plugins/{plugin-name}/` | `plugins/projman/` |
| Plugin manifest | `plugins/{plugin-name}/.claude-plugin/plugin.json` | `plugins/projman/.claude-plugin/plugin.json` |
| Plugin MCP mapping (optional) | `plugins/{plugin-name}/.claude-plugin/metadata.json` | `plugins/projman/.claude-plugin/metadata.json` |
| Plugin commands | `plugins/{plugin-name}/commands/` | `plugins/projman/commands/` |
| Plugin agents | `plugins/{plugin-name}/agents/` | `plugins/projman/agents/` |
| Plugin skills | `plugins/{plugin-name}/skills/` | `plugins/projman/skills/` |
| Plugin integration snippet | `plugins/{plugin-name}/claude-md-integration.md` | `plugins/projman/claude-md-integration.md` |

### MCP Server Paths

MCP servers are **shared at repository root** and configured in `.mcp.json`.

| Context | Pattern | Example |
|---------|---------|---------|
| MCP configuration | `.mcp.json` | `.mcp.json` (at repo root) |
| Shared MCP server | `mcp-servers/{server}/` | `mcp-servers/gitea/` |
| MCP server code | `mcp-servers/{server}/mcp_server/` | `mcp-servers/gitea/mcp_server/` |
| MCP venv (local) | `mcp-servers/{server}/.venv/` | `mcp-servers/gitea/.venv/` |

**Note:** Plugins do NOT have their own `mcp-servers/` directories. All MCP servers are shared at root and configured via `.mcp.json`.

### MCP Venv Paths - CRITICAL

**Venvs live in a CACHE directory that SURVIVES marketplace updates.**

When checking for venvs, ALWAYS check in this order:

| Priority | Path | Survives Updates? |
|----------|------|-------------------|
| 1 (CHECK FIRST) | `~/.cache/claude-mcp-venvs/leo-claude-mktplace/{server}/.venv/` | YES |
| 2 (fallback) | `{marketplace}/mcp-servers/{server}/.venv/` | NO |

**Why cache first?**
- Marketplace directory gets WIPED on every update/reinstall
- Cache directory SURVIVES updates
- False "venv missing" errors waste hours of debugging

**Pattern for hooks checking venvs:**
```bash
CACHE_VENV="$HOME/.cache/claude-mcp-venvs/leo-claude-mktplace/{server}/.venv/bin/python"
LOCAL_VENV="$MARKETPLACE_ROOT/mcp-servers/{server}/.venv/bin/python"

if [[ -f "$CACHE_VENV" ]]; then
    VENV_PATH="$CACHE_VENV"
elif [[ -f "$LOCAL_VENV" ]]; then
    VENV_PATH="$LOCAL_VENV"
else
    echo "venv missing"
fi
```

**See lesson learned:** [Startup Hooks Must Check Venv Cache Path First](https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/wiki/lessons/patterns/startup-hooks-must-check-venv-cache-path-first)

### Documentation Paths

| Type | Location |
|------|----------|
| Architecture diagrams | `docs/architecture/` |
| This file | `docs/CANONICAL-PATHS.md` |
| Update guide | `docs/UPDATING.md` |
| Configuration guide | `docs/CONFIGURATION.md` |
| Commands cheat sheet | `docs/COMMANDS-CHEATSHEET.md` |
| Debugging checklist | `docs/DEBUGGING-CHECKLIST.md` |

---

## Validation Rules

### Before Creating Any File

1. Check this file for the correct path pattern
2. Verify the parent directory exists in the structure above
3. If path not listed here, **STOP AND ASK**

### Before Generating Any Prompt

1. List all file paths the prompt will create/modify
2. Verify each path against patterns in this file
3. Show verification to user before proceeding

### Relative Path Calculation

From `.mcp.json` (at root) to `mcp-servers/gitea/`:
```
.mcp.json (at repository root)
  → Uses absolute installed path: ~/.claude/plugins/marketplaces/.../mcp-servers/gitea/run.sh
```

From `.claude-plugin/marketplace.json` to `plugins/projman/`:
```
.claude-plugin/marketplace.json
  ↑ marketplace.json is at repo root level
  → go down to plugins/projman/           (./plugins/projman/)

Result: ./plugins/projman
```

---

## Anti-Patterns (NEVER DO THIS)

| Wrong | Why | Correct |
|-------|-----|---------|
| `projman/` at root | Plugins go in `plugins/` | `plugins/projman/` |
| `mcp-servers/` inside plugins | MCP servers are shared at root | Use root `mcp-servers/` |
| Plugin-level `.mcp.json` | MCP config is at root | Use root `.mcp.json` |
| Hardcoding absolute paths in source | Breaks portability | Use relative paths or `${CLAUDE_PLUGIN_ROOT}` |

---

## Architecture Note

MCP servers are **shared at repository root** and configured in a single `.mcp.json` file.

**Benefits:**
- Single source of truth for each MCP server
- Updates apply to all plugins automatically
- No duplication - clean plugin structure
- Simple configuration in one place

**Configuration:**
All MCP servers are defined in `.mcp.json` at repository root:
```json
{
  "mcpServers": {
    "gitea": { "command": ".../mcp-servers/gitea/run.sh" },
    "netbox": { "command": ".../mcp-servers/netbox/run.sh" },
    "data-platform": { "command": ".../mcp-servers/data-platform/run.sh" },
    "viz-platform": { "command": ".../mcp-servers/viz-platform/run.sh" },
    "contract-validator": { "command": ".../mcp-servers/contract-validator/run.sh" }
  }
}
```

---

## Change Log

| Date | Change | By |
|------|--------|-----|
| 2026-02-04 | v7.1.0: Added profile configs, prompts/, project-lessons-learned/, metadata.json, deprecated switch-profile.sh | Claude Code |
| 2026-01-30 | v5.5.0: Removed plugin-level mcp-servers symlinks - all MCP config now in root .mcp.json | Claude Code |
| 2026-01-26 | v5.0.0: Added contract-validator plugin and MCP server | Claude Code |
| 2026-01-26 | v4.1.0: Added viz-platform plugin and MCP server | Claude Code |
| 2026-01-25 | v4.0.0: Added data-platform plugin and MCP server | Claude Code |
| 2026-01-20 | v3.0.0: MCP servers moved to root with symlinks | Claude Code |
| 2026-01-20 | v3.0.0: Added clarity-assist, git-flow, pr-review plugins | Claude Code |
| 2026-01-20 | v3.0.0: Added docs/CONFIGURATION.md | Claude Code |
| 2026-01-20 | v3.0.0: Renamed marketplace to leo-claude-mktplace | Claude Code |
| 2026-01-20 | Removed docs/references/ (obsolete planning docs) | Claude Code |
| 2026-01-19 | Added claude-md-integration.md path pattern | Claude Code |
| 2025-12-15 | Restructured: MCP servers bundled in plugins | Claude Code |
| 2025-12-12 | Initial creation | Claude Code |
