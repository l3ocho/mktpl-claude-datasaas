# Canonical Paths - SINGLE SOURCE OF TRUTH

**This file defines ALL valid paths in this repository. No exceptions. No inference. No assumptions.**

Last Updated: 2026-01-27 (v5.1.0)

---

## Repository Root Structure

```
leo-claude-mktplace/
├── .claude/                    # Claude Code local settings
├── .claude-plugin/             # Marketplace manifest
│   └── marketplace.json
├── .scratch/                   # Transient work (auto-cleaned)
├── docs/                       # All documentation
│   ├── architecture/           # Draw.io diagrams and specs
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
│   │   ├── .mcp.json
│   │   ├── mcp-servers/
│   │   │   └── gitea -> ../../../mcp-servers/gitea  # SYMLINK
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
│   │   ├── .mcp.json
│   │   ├── mcp-servers/
│   │   │   └── netbox -> ../../../mcp-servers/netbox  # SYMLINK
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
│   ├── clarity-assist/         # NEW in v3.0.0
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── git-flow/               # NEW in v3.0.0
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── pr-review/              # NEW in v3.0.0
│   │   ├── .claude-plugin/
│   │   ├── .mcp.json
│   │   ├── mcp-servers/
│   │   │   └── gitea -> ../../../mcp-servers/gitea  # SYMLINK
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── data-platform/          # NEW in v4.0.0
│   │   ├── .claude-plugin/
│   │   ├── .mcp.json
│   │   ├── mcp-servers/
│   │   │   └── data-platform -> ../../../mcp-servers/data-platform  # SYMLINK
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── hooks/
│   │   └── claude-md-integration.md
│   ├── contract-validator/     # NEW in v5.0.0
│   │   ├── .claude-plugin/
│   │   ├── .mcp.json
│   │   ├── mcp-servers/
│   │   │   └── contract-validator -> ../../../mcp-servers/contract-validator  # SYMLINK
│   │   ├── commands/
│   │   ├── agents/
│   │   └── claude-md-integration.md
│   └── viz-platform/           # NEW in v4.1.0
│       ├── .claude-plugin/
│       ├── .mcp.json
│       ├── mcp-servers/
│       │   └── viz-platform -> ../../../mcp-servers/viz-platform  # SYMLINK
│       ├── commands/
│       ├── agents/
│       ├── hooks/
│       └── claude-md-integration.md
├── scripts/                    # Setup and maintenance scripts
│   ├── setup.sh                # Initial setup (create venvs, config templates)
│   ├── post-update.sh          # Post-update (rebuild venvs, verify symlinks)
│   ├── check-venv.sh           # Check if venvs exist (for hooks)
│   ├── validate-marketplace.sh # Marketplace compliance validation
│   ├── verify-hooks.sh         # Verify all hooks use correct event types
│   ├── setup-venvs.sh          # Setup/repair MCP server venvs
│   ├── venv-repair.sh          # Repair broken venv symlinks
│   └── release.sh              # Release automation with version bumping
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
| Plugin commands | `plugins/{plugin-name}/commands/` | `plugins/projman/commands/` |
| Plugin agents | `plugins/{plugin-name}/agents/` | `plugins/projman/agents/` |
| Plugin .mcp.json | `plugins/{plugin-name}/.mcp.json` | `plugins/projman/.mcp.json` |
| Plugin integration snippet | `plugins/{plugin-name}/claude-md-integration.md` | `plugins/projman/claude-md-integration.md` |

### MCP Server Paths (v3.0.0 Architecture)

MCP servers are **shared at repository root** with **symlinks** from plugins.

| Context | Pattern | Example |
|---------|---------|---------|
| Shared MCP server | `mcp-servers/{server}/` | `mcp-servers/gitea/` |
| MCP server code | `mcp-servers/{server}/mcp_server/` | `mcp-servers/gitea/mcp_server/` |
| MCP venv | `mcp-servers/{server}/.venv/` | `mcp-servers/gitea/.venv/` |
| Plugin symlink | `plugins/{plugin}/mcp-servers/{server}` | `plugins/projman/mcp-servers/gitea` |

### Symlink Pattern

Plugins that use MCP servers create symlinks:
```bash
# From plugin directory
ln -s ../../../mcp-servers/gitea plugins/projman/mcp-servers/gitea
```

The symlink target is relative: `../../../mcp-servers/{server}`

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

### Relative Path Calculation (v3.0.0)

From `plugins/projman/.mcp.json` to shared `mcp-servers/gitea/`:
```
plugins/projman/.mcp.json
  → Uses ${CLAUDE_PLUGIN_ROOT}/mcp-servers/gitea/
  → Symlink at plugins/projman/mcp-servers/gitea points to ../../../mcp-servers/gitea

Result in .mcp.json: ${CLAUDE_PLUGIN_ROOT}/mcp-servers/gitea/.venv/bin/python
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
| Direct path in .mcp.json to root mcp-servers | Use symlink | Symlink at `plugins/{plugin}/mcp-servers/` |
| Creating new mcp-servers inside plugins | Use shared + symlink | Symlink to `mcp-servers/` |
| Hardcoding absolute paths | Breaks portability | Use `${CLAUDE_PLUGIN_ROOT}` |

---

## Architecture Note (v3.0.0)

MCP servers are now **shared at repository root** with **symlinks** from plugins:

**Benefits:**
- Single source of truth for each MCP server
- Updates apply to all plugins automatically
- Reduced duplication
- Symlinks work with Claude Code caching

**Symlink Pattern:**
```
plugins/projman/mcp-servers/gitea -> ../../../mcp-servers/gitea
plugins/cmdb-assistant/mcp-servers/netbox -> ../../../mcp-servers/netbox
plugins/pr-review/mcp-servers/gitea -> ../../../mcp-servers/gitea
plugins/data-platform/mcp-servers/data-platform -> ../../../mcp-servers/data-platform
plugins/viz-platform/mcp-servers/viz-platform -> ../../../mcp-servers/viz-platform
plugins/contract-validator/mcp-servers/contract-validator -> ../../../mcp-servers/contract-validator
```

---

## Change Log

| Date | Change | By |
|------|--------|-----|
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
