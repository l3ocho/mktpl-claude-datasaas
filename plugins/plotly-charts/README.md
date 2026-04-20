# plotly-charts v1.0.0

Plotly chart scaffolding plugin for Claude Code Dash applications.

## Scope

Plotly chart creation and export, theme-aware via dmc-design's design contract.

## Commands

| Command | Description |
|---------|-------------|
| `/chart create <type>` | Scaffold a Plotly chart |
| `/chart export <format>` | Export chart configuration |

## Skills

`chart-types.md`

## MCP

None — skill-driven only.

## Migration from viz-platform

`/viz chart` → `/chart create`, `/viz chart-export` → `/chart export`.
See `docs/MIGRATION-v11.md`.
