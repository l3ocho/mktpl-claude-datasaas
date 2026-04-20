---
name: chart
description: [dmc-design] Plotly chart scaffolding — create, export
---

# /chart

Plotly chart scaffolding for Dash applications.

## Usage

```
/chart create <type>       — Scaffold a Plotly chart
/chart export <format>     — Export chart configuration
```

## Routing

Route based on first word of $ARGUMENTS:
- `create` → `/plotly-charts:chart-create`
- `export` → `/plotly-charts:chart-export`

If no arguments provided:
1. Display the Available Commands table above
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool
