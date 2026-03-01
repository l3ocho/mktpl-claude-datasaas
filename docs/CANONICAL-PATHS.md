# Canonical Paths - SINGLE SOURCE OF TRUTH

**This file defines ALL valid paths in this repository. No exceptions. No inference. No assumptions.**

Last Updated: 2026-02-07 (v9.1.0)

---

## Repository Root Structure

```
mktpl-claude-datasaas/
├── .claude/                    # Claude Code local settings
├── .claude-plugin/             # Marketplace manifest
│   ├── marketplace.json
│   ├── marketplace-lean.json   # Lean profile (6 core plugins)
│   └── marketplace-full.json   # Full profile (all plugins)
├── .mcp-lean.json              # Lean profile MCP config (gitea only)
├── .mcp-full.json              # Full profile MCP config (all servers)
├── .scratch/                   # Transient work (auto-cleaned)
├── docs/                       # All documentation
│   ├── ARCHITECTURE.md         # System architecture and plugin reference
│   ├── CANONICAL-PATHS.md      # This file - single source of truth
│   ├── COMMANDS-CHEATSHEET.md  # All commands quick reference
│   ├── CONFIGURATION.md        # Centralized configuration guide
│   ├── DEBUGGING-CHECKLIST.md  # Systematic troubleshooting guide
│   ├── MIGRATION-v9.md         # v8.x → v9.0.0 migration guide
│   └── UPDATING.md             # Update guide
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
│   │   ├── commands/
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
│   │   ├── skills/
│   │   │   ├── data-integrity-audit.md
│   │   │   ├── data-profiling.md
│   │   │   ├── dbt-workflow.md
│   │   │   ├── lineage-analysis.md
│   │   │   ├── mcp-tools-reference.md
│   │   │   ├── setup-workflow.md
│   │   │   ├── visual-header.md
│   │   │   ├── data-exploration-workflow.md
│   │   │   └── notebook-authoring.md
│   │   └── claude-md-integration.md
│   ├── contract-validator/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   └── claude-md-integration.md
│   ├── viz-platform/
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   │   ├── accessibility-rules.md
│   │   │   ├── chart-types.md
│   │   │   ├── design-system-audit.md
│   │   │   ├── dmc-components.md
│   │   │   ├── layout-templates.md
│   │   │   ├── mcp-tools-reference.md
│   │   │   ├── responsive-design.md
│   │   │   ├── theming-system.md
│   │   │   ├── analytical-chart-selection.md
│   │   │   ├── notebook-design-system.md
│   │   │   └── choropleth-map-patterns.md
│   │   └── claude-md-integration.md
│   ├── saas-api-platform/       # REST/GraphQL API scaffolding (scaffold)
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── saas-db-migrate/         # Database migration management (scaffold)
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── saas-react-platform/     # React frontend toolkit (scaffold)
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── saas-test-pilot/         # Test automation (scaffold)
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── data-seed/               # Test data generation (scaffold)
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── ops-release-manager/     # Release management (scaffold)
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   ├── ops-deploy-pipeline/     # Deployment pipeline (scaffold)
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── skills/
│   │   └── claude-md-integration.md
│   └── debug-mcp/               # MCP debugging toolkit (scaffold)
│       ├── .claude-plugin/
│       ├── commands/
│       ├── agents/
│       ├── skills/
│       └── claude-md-integration.md
├── scripts/                    # Setup and maintenance scripts
│   ├── setup.sh                # Initial setup (create venvs, config templates)
│   ├── post-update.sh          # Post-update (clear cache, show changelog)
│   ├── setup-venvs.sh          # Setup MCP server venvs (create only, never delete)
│   ├── validate-marketplace.sh # Marketplace compliance validation
│   ├── verify-hooks.sh         # Verify all hooks use correct event types
│   ├── release.sh              # Release automation with version bumping
│   ├── claude-launch.sh        # Task-specific launcher with profile selection
│   ├── install-plugin.sh       # Install plugin to consumer project
│   ├── list-installed.sh       # Show installed plugins in a project
│   └── uninstall-plugin.sh     # Remove plugin from consumer project
├── CLAUDE.md
├── README.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore
```

---

## Path Patterns (MANDATORY)

### Phase 1a Paths (v8.1.0)

New files added in v8.1.0:

```
plugins/projman/commands/project.md
plugins/projman/commands/project-initiation.md
plugins/projman/commands/project-plan.md
plugins/projman/commands/project-status.md
plugins/projman/commands/project-close.md
plugins/projman/commands/adr.md
plugins/projman/commands/adr-create.md
plugins/projman/commands/adr-list.md
plugins/projman/commands/adr-update.md
plugins/projman/commands/adr-supersede.md
plugins/projman/skills/source-analysis.md
plugins/projman/skills/project-charter.md
plugins/projman/skills/adr-conventions.md
plugins/projman/skills/epic-conventions.md
plugins/projman/skills/wbs.md
plugins/projman/skills/risk-register.md
plugins/projman/skills/sprint-roadmap.md
plugins/projman/skills/wiki-conventions.md
plugins/project-hygiene/commands/hygiene-check.md
plugins/contract-validator/commands/cv-status.md
```

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
| MCP server code | `mcp-servers/{server}/mcp_server/` | `mcp-servers/netbox/mcp_server/` |
| MCP venv (local) | `mcp-servers/{server}/.venv/` | `mcp-servers/gitea/.venv/` |

**Note:** `mcp-servers/gitea/` is a thin wrapper — source code is in the published `gitea-mcp` package (Gitea PyPI). Other MCP servers still have local source code.

**Note:** Plugins do NOT have their own `mcp-servers/` directories. All MCP servers are shared at root and configured via `.mcp.json`.

### MCP Venv Paths - CRITICAL

**Venvs live in a CACHE directory that SURVIVES marketplace updates.**

When checking for venvs, ALWAYS check in this order:

| Priority | Path | Survives Updates? |
|----------|------|-------------------|
| 1 (CHECK FIRST) | `~/.cache/claude-mcp-venvs/mktpl-claude-datasaas/{server}/.venv/` | YES |
| 2 (fallback) | `{marketplace}/mcp-servers/{server}/.venv/` | NO |

**Why cache first?**
- Marketplace directory gets WIPED on every update/reinstall
- Cache directory SURVIVES updates
- False "venv missing" errors waste hours of debugging

**Pattern for hooks checking venvs:**
```bash
CACHE_VENV="$HOME/.cache/claude-mcp-venvs/mktpl-claude-datasaas/{server}/.venv/bin/python"
LOCAL_VENV="$MARKETPLACE_ROOT/mcp-servers/{server}/.venv/bin/python"

if [[ -f "$CACHE_VENV" ]]; then
    VENV_PATH="$CACHE_VENV"
elif [[ -f "$LOCAL_VENV" ]]; then
    VENV_PATH="$LOCAL_VENV"
else
    echo "venv missing"
fi
```

**See lesson learned:** [Startup Hooks Must Check Venv Cache Path First](https://gitea.hotserv.cloud/personal-projects/mktpl-claude-datasaas/wiki/lessons/patterns/startup-hooks-must-check-venv-cache-path-first)

### Documentation Paths

| Type | Location |
|------|----------|
| Architecture & plugin reference | `docs/ARCHITECTURE.md` |
| This file | `docs/CANONICAL-PATHS.md` |
| Update guide | `docs/UPDATING.md` |
| Configuration guide | `docs/CONFIGURATION.md` |
| Commands cheat sheet | `docs/COMMANDS-CHEATSHEET.md` |
| Debugging checklist | `docs/DEBUGGING-CHECKLIST.md` |
| Migration guide (v8→v9) | `docs/MIGRATION-v9.md` |

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

## Domain Metadata

### Domain Field Location

Domain metadata is stored in `metadata.json` (v9.1.2+, moved from plugin.json/marketplace.json for Claude Code schema compliance):

| Location | Field | Example |
|----------|-------|---------|
| `plugins/{name}/.claude-plugin/metadata.json` | `"domain": "core"` | `plugins/projman/.claude-plugin/metadata.json` |

### Allowed Domain Values

| Domain | Purpose | Existing Plugins |
|--------|---------|-----------------|
| `core` | Development workflow plugins | projman, git-flow, pr-review, code-sentinel, doc-guardian, clarity-assist, contract-validator, claude-config-maintainer, project-hygiene |
| `data` | Data engineering and visualization | data-platform, viz-platform, data-seed |
| `ops` | Operations and infrastructure | cmdb-assistant, ops-release-manager, ops-deploy-pipeline |
| `saas` | SaaS application development | saas-api-platform, saas-db-migrate, saas-react-platform, saas-test-pilot |
| `debug` | Debugging and diagnostics | debug-mcp |

### Plugin Naming Convention

- **Core plugins:** No prefix (existing names never change)
- **New plugins:** Domain prefix: `saas-*`, `ops-*`, `data-*`, `debug-*`
- Domain is always in metadata — prefix is a naming convention, not a requirement

### Domain Query Examples

```bash
# List all plugins in a domain
for p in plugins/*; do
  d=$(jq -r '.domain // empty' "$p/.claude-plugin/metadata.json" 2>/dev/null)
  [[ "$d" == "saas" ]] && basename "$p"
done

# Count plugins per domain
for p in plugins/*; do
  jq -r '.domain // empty' "$p/.claude-plugin/metadata.json" 2>/dev/null
done | sort | uniq -c | sort -rn
```

---

## Change Log

| Date | Change | By |
|------|--------|-----|
| 2026-02-07 | v9.1.2: Moved domain field from plugin.json/marketplace.json to metadata.json for Claude Code schema compliance | Claude Code |
| 2026-02-07 | v9.1.0: Removed deleted dirs (architecture/, prompts/, project-lessons-learned/), added Phase 3 plugins, added ARCHITECTURE.md, MIGRATION-v9.md, updated Domain table, removed stale hooks/ dirs | Claude Code |
| 2026-02-06 | v8.0.0: Added domain metadata section, Phase 1a paths, future plugin paths | Claude Code |
| 2026-02-04 | v7.1.0: Added profile configs, prompts/, project-lessons-learned/, metadata.json, deprecated switch-profile.sh | Claude Code |
| 2026-01-30 | v5.5.0: Removed plugin-level mcp-servers symlinks - all MCP config now in root .mcp.json | Claude Code |
| 2026-01-26 | v5.0.0: Added contract-validator plugin and MCP server | Claude Code |
| 2026-01-26 | v4.1.0: Added viz-platform plugin and MCP server | Claude Code |
| 2026-01-25 | v4.0.0: Added data-platform plugin and MCP server | Claude Code |
| 2026-01-20 | v3.0.0: MCP servers moved to root with symlinks | Claude Code |
| 2026-01-20 | v3.0.0: Added clarity-assist, git-flow, pr-review plugins | Claude Code |
| 2026-01-20 | v3.0.0: Added docs/CONFIGURATION.md | Claude Code |
| 2026-01-20 | v3.0.0: Renamed marketplace to mktpl-claude-datasaas | Claude Code |
| 2026-01-20 | Removed docs/references/ (obsolete planning docs) | Claude Code |
| 2026-01-19 | Added claude-md-integration.md path pattern | Claude Code |
| 2025-12-15 | Restructured: MCP servers bundled in plugins | Claude Code |
| 2025-12-12 | Initial creation | Claude Code |
