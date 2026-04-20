---
name: design
description: DMC Design System commands — setup, theme, pattern, component, accessibility
---

# /design

Dash Mantine Components design system management.

## Usage

```
/design setup               — Environment + contract builder
/design theme [action]      — Theme management (apply|create|export-css)
/design pattern [action]    — Pattern enforcement (scan|lock|check|list|unlock)
/design component <n>       — DMC component validation
/design accessibility       — WCAG contrast check
```

## Routing

Route to the appropriate sub-command based on the first word of $ARGUMENTS:
- `setup` → `/dmc-design:design-setup`
- `theme` → `/dmc-design:design-theme`
- `pattern` → `/dmc-design:design-pattern`
- `component` → `/dmc-design:design-component`
- `accessibility` → `/dmc-design:design-accessibility`

If no arguments provided:
1. Display the Available Commands table above
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool
