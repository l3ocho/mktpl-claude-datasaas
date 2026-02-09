---
name: viz
description: Visualization tools — type /viz <action> for commands
---

# /viz

Visualization tools with Dash Mantine Components validation, Plotly charts, and theming.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `theme` | `/viz-platform:viz-theme` | Apply existing theme to visualizations |
| `theme-new` | `/viz-platform:viz-theme-new` | Create new custom theme with design tokens |
| `theme-css` | `/viz-platform:viz-theme-css` | Export theme as CSS custom properties |
| `component` | `/viz-platform:viz-component` | Inspect DMC component props and validation |
| `dashboard` | `/viz-platform:viz-dashboard` | Create dashboard layouts with filters and grids |
| `chart` | `/viz-platform:viz-chart` | Create Plotly charts with theme integration |
| `chart-export` | `/viz-platform:viz-chart-export` | Export charts to PNG, SVG, PDF via kaleido |
| `breakpoints` | `/viz-platform:viz-breakpoints` | Configure responsive layout breakpoints |
| `accessibility-check` | `/viz-platform:viz-accessibility-check` | Color blind validation (WCAG contrast ratios) |
| `design-review` | `/viz-platform:viz-design-review` | Detailed design system audits |
| `design-gate` | `/viz-platform:viz-design-gate` | Binary pass/fail design system validation |
| `setup` | `/viz-platform:viz-setup` | Setup wizard for viz-platform MCP server |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/viz theme`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/viz-platform:viz-theme`)
