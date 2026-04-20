# Migration Guide: v10.x to v11.0.0

## Overview

`viz-platform` has been split into three focused plugins. This is a breaking change.

## Plugin Mapping

| Old | New |
|-----|-----|
| `viz-platform` | `dmc-design` + `dash-scaffold` + `plotly-charts` |

## Command Mapping

| Old Command | New Command | Plugin |
|-------------|-------------|--------|
| `/viz setup` | `/design setup` | dmc-design |
| `/viz theme` | `/design theme` | dmc-design |
| `/viz component` | `/design component` | dmc-design |
| `/viz accessibility` | `/design accessibility` | dmc-design |
| `/viz dashboard` | `/dash dashboard` | dash-scaffold |
| `/viz breakpoints` | `/dash breakpoints` | dash-scaffold |
| `/viz chart` | `/chart create` | plotly-charts |
| `/viz chart-export` | `/chart export` | plotly-charts |

## New Features (v11.0.0)

### /design pattern (dmc-design)

User-declared design patterns persisted in `.claude/design-patterns.json`.

```
/design pattern scan    — Extract patterns from CSS + Python
/design pattern lock    — Declare a rule
/design pattern check   — Verify all rules hold
/design pattern list    — Show all rules
/design pattern unlock  — Remove a rule
```

### design-reviewer Agent

Resurrected from viz-platform v9.4.0. Audits Python + CSS against design contract
and locked patterns.

## Skill Migrations

Three notebook skills moved from `viz-platform/skills/` to `data-platform/skills/`:
- `analytical-chart-selection.md`
- `notebook-design-system.md`
- `choropleth-map-patterns.md`

The `data-analysis.md` agent has been updated to reference them from their new location.

## Consumer Project Steps

1. Remove `viz-platform` from your `.claude/plugins/` installation
2. Install `dmc-design` (if using DMC/theming/pattern enforcement)
3. Install `dash-scaffold` (if building Dash layouts)
4. Install `plotly-charts` (if using Plotly charts)
5. Update CLAUDE.md integration snippets (see each plugin's `claude-md-integration.md`)

## MCP Server

The `viz-platform` MCP server has been renamed to `dmc-design`. Update `.mcp.json`:

```json
// Old
"viz-platform": { "command": ".../mcp-servers/viz-platform/run.sh" }

// New
"dmc-design": { "command": ".../mcp-servers/dmc-design/run.sh" }
```

## drawio-plugin

drawio-plugin bumped to v1.3.0. References to `viz-platform` updated to `dmc-design`.
The `WIREFRAME.md` contract is now consumed by `dmc-design` (previously `viz-platform`).
