---
name: dash
description: Dash application scaffolding — dashboard, page, breakpoints
---

# /dash

Dash application scaffolding and layout management.

## Usage

```
/dash dashboard [template]  — Create a Dash dashboard layout
/dash page <n>              — Create a new Dash page
/dash breakpoints           — Configure responsive breakpoints
```

## Routing

Route based on first word of $ARGUMENTS:
- `dashboard` → `/dash-scaffold:dash-dashboard`
- `page` → `/dash-scaffold:dash-page`
- `breakpoints` → `/dash-scaffold:dash-breakpoints`

If no arguments provided:
1. Display the Available Commands table above
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool
