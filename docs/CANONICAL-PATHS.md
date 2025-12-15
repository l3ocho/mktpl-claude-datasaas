# Canonical Paths - SINGLE SOURCE OF TRUTH

**This file defines ALL valid paths in this repository. No exceptions. No inference. No assumptions.**

Last Updated: 2025-12-15

---

## Repository Root Structure

```
support-claude-mktplace/
├── .claude/                    # Claude Code local settings
├── .claude-plugin/             # Marketplace manifest (bandit-claude-marketplace)
│   └── marketplace.json
├── .scratch/                   # Transient work (auto-cleaned)
├── docs/                       # All documentation
│   ├── architecture/           # Draw.io diagrams and specs
│   ├── references/             # Reference specifications
│   └── workflows/              # Workflow documentation
├── hooks/                      # Shared hooks (if any)
├── plugins/                    # ALL plugins with bundled MCP servers
│   ├── projman/
│   │   ├── .claude-plugin/
│   │   ├── mcp-servers/        # MCP servers bundled IN plugin
│   │   │   ├── gitea/
│   │   │   └── wikijs/
│   │   ├── commands/
│   │   ├── agents/
│   │   └── skills/
│   ├── projman-pmo/
│   ├── project-hygiene/
│   └── cmdb-assistant/
│       ├── .claude-plugin/
│       ├── mcp-servers/        # MCP servers bundled IN plugin
│       │   └── netbox/
│       ├── commands/
│       └── agents/
├── scripts/                    # Setup and maintenance scripts
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

### MCP Server Paths (Bundled in Plugins)

MCP servers are now **bundled inside each plugin** to ensure they work when plugins are cached.

| Context | Pattern | Example |
|---------|---------|---------|
| MCP server location | `plugins/{plugin}/mcp-servers/{server}/` | `plugins/projman/mcp-servers/gitea/` |
| MCP server code | `plugins/{plugin}/mcp-servers/{server}/mcp_server/` | `plugins/projman/mcp-servers/gitea/mcp_server/` |
| MCP venv | `plugins/{plugin}/mcp-servers/{server}/.venv/` | `plugins/projman/mcp-servers/gitea/.venv/` |

### Relative Path Patterns (CRITICAL)

| From | To | Pattern |
|------|----|---------|
| Plugin .mcp.json | Bundled MCP server | `${CLAUDE_PLUGIN_ROOT}/mcp-servers/{server}` |
| marketplace.json | Plugin | `./plugins/{plugin-name}` |

### Documentation Paths

| Type | Location |
|------|----------|
| Reference specs | `docs/references/` |
| Architecture diagrams | `docs/architecture/` |
| Workflow docs | `docs/workflows/` |
| This file | `docs/CANONICAL-PATHS.md` |

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

From `plugins/projman/.mcp.json` to bundled `mcp-servers/gitea/`:
```
plugins/projman/.mcp.json
  → MCP servers are IN the plugin at mcp-servers/

Result: mcp-servers/gitea/
With variable: ${CLAUDE_PLUGIN_ROOT}/mcp-servers/gitea/
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
| `mcp-servers/` at root | MCP servers are bundled in plugins | `plugins/{plugin}/mcp-servers/` |
| `../../mcp-servers/` from plugin | Old pattern, doesn't work with caching | `${CLAUDE_PLUGIN_ROOT}/mcp-servers/` |
| `./../../../plugins/projman` in marketplace | Wrong (old nested structure) | `./plugins/projman` |

---

## Architecture Note

MCP servers are bundled inside each plugin (not shared at root) because:
- Claude Code caches only the plugin directory when installed
- Relative paths to parent directories break in the cache
- Each plugin must be self-contained to work properly

---

## Change Log

| Date | Change | By |
|------|--------|-----|
| 2025-12-15 | Restructured: MCP servers now bundled in plugins | Claude Code |
| 2025-12-12 | Initial creation | Claude Code |
