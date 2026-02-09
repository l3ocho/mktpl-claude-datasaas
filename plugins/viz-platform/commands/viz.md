---
name: viz
description: Visualization tools — type /viz <action> for commands
---

# /viz

Visualization tools with Dash Mantine Components validation, Plotly charts, and theming.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|-------------|-------------|
| `/viz theme` | Apply existing theme to visualizations |
| `/viz theme-new` | Create new custom theme with design tokens |
| `/viz theme-css` | Export theme as CSS custom properties |
| `/viz component` | Inspect DMC component props and validation |
| `/viz dashboard` | Create dashboard layouts with filters and grids |
| `/viz chart` | Create Plotly charts with theme integration |
| `/viz chart-export` | Export charts to PNG, SVG, PDF via kaleido |
| `/viz breakpoints` | Configure responsive layout breakpoints |
| `/viz accessibility-check` | Color blind validation (WCAG contrast ratios) |
| `/viz design-review` | Detailed design system audits |
| `/viz design-gate` | Binary pass/fail design system validation |
| `/viz setup` | Setup wizard for viz-platform MCP server |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
