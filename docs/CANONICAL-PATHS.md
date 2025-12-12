# Canonical Paths - SINGLE SOURCE OF TRUTH

**This file defines ALL valid paths in this repository. No exceptions. No inference. No assumptions.**

Last Updated: 2025-12-12

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
├── mcp-servers/                # Shared MCP servers (AT ROOT)
│   ├── gitea/
│   ├── wikijs/
│   └── netbox/
├── plugins/                    # ALL plugins (INSIDE plugins/)
│   ├── projman/
│   ├── projman-pmo/
│   ├── project-hygiene/
│   └── cmdb-assistant/
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

### MCP Server Paths

| Context | Pattern | Example |
|---------|---------|---------|
| MCP server location | `mcp-servers/{server-name}/` | `mcp-servers/gitea/` |
| MCP server code | `mcp-servers/{server-name}/mcp_server/` | `mcp-servers/gitea/mcp_server/` |
| MCP venv | `mcp-servers/{server-name}/.venv/` | `mcp-servers/gitea/.venv/` |

### Relative Path Patterns (CRITICAL)

| From | To | Pattern |
|------|----|---------|
| Plugin .mcp.json | MCP server | `${CLAUDE_PLUGIN_ROOT}/../../mcp-servers/{server}` |
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

From `plugins/projman/.mcp.json` to `mcp-servers/gitea/`:
```
plugins/projman/.mcp.json
  ↑ go up to plugins/projman/     (../)
  ↑ go up to plugins/             (../)
  ↑ go up to root/                (../)
  → go down to mcp-servers/gitea/ (mcp-servers/gitea/)

Result: ../../mcp-servers/gitea/
With variable: ${CLAUDE_PLUGIN_ROOT}/../../mcp-servers/gitea/
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
| `../mcp-servers/` from plugin | Missing one level | `../../mcp-servers/` |
| `./../../../plugins/projman` in marketplace | Wrong (old nested structure) | `./plugins/projman` |
| Creating `docs/CORRECT-ARCHITECTURE.md` | This file replaces it | Use `docs/CANONICAL-PATHS.md` |

---

## Change Log

| Date | Change | By |
|------|--------|-----|
| 2025-12-12 | Initial creation | Claude Code |
