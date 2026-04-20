# dmc-design v1.0.0

Dash Mantine Components (DMC) design system plugin for Claude Code.

## Scope

DMC validation, theme management, CSS pattern enforcement, design contract, and
user-declared pattern persistence.

## Commands

| Command | Description |
|---------|-------------|
| `/design setup` | Initialize design contract + environment |
| `/design theme apply\|create\|export-css` | Theme management |
| `/design pattern scan\|lock\|check\|list\|unlock` | Pattern enforcement |
| `/design component <n>` | Validate DMC component usage |
| `/design accessibility` | WCAG contrast audit |

## Agents

| Agent | Description |
|-------|-------------|
| `design-reviewer` | Audits Python + CSS against design contract and locked patterns |

## MCP Tools (~12)

`list_components`, `get_component_props`, `validate_component`, `theme_validate`,
`theme_export_css`, `accessibility_validate_colors`, `accessibility_validate_theme`,
`contract_load`, `contract_validate`, `contract_resolve_component`,
`contract_lock_component`, `contract_get_surface`

## Skills

`theming-system.md`, `dmc-components.md`, `accessibility-rules.md`,
`color-scheme-validation.md`, `mcp-tools-reference.md`, `pattern-enforcement.md`

## Design Patterns File

`.claude/design-patterns.json` — persists user-declared design rules across sessions.
Schema: `mcp-servers/dmc-design/schemas/design-patterns.schema.json`.

## Migration from viz-platform

Migrated from `viz-platform v10.0.0`. See `docs/MIGRATION-v11.md`.
