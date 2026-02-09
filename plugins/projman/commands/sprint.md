---
name: sprint
description: Sprint lifecycle management — type /sprint <action> for commands
---

# /sprint

Sprint lifecycle management for projman.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/sprint plan` | Analyze requirements, create issues, request approval |
| `/sprint start` | Begin execution, load context, dispatch tasks |
| `/sprint status` | Check progress, blockers, completion percentage |
| `/sprint close` | Capture lessons learned, close milestone |
| `/sprint review` | Pre-close code quality review |
| `/sprint test` | Run/generate tests for sprint scope |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
