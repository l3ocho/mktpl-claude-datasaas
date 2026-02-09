---
name: projman sprint
description: Sprint lifecycle management — type /projman sprint <action> for commands
---

# /sprint

Sprint lifecycle management for projman.

When invoked without a sub-command or with `$ARGUMENTS`, handle as follows:

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `plan` | `/projman:sprint-plan` | Analyze requirements, create issues, request approval |
| `start` | `/projman:sprint-start` | Begin execution, load context, dispatch tasks |
| `status` | `/projman:sprint-status` | Check progress, blockers, completion percentage |
| `close` | `/projman:sprint-close` | Capture lessons learned, close milestone |
| `review` | `/projman:sprint-review` | Pre-close code quality review |
| `test` | `/projman:sprint-test` | Run/generate tests for sprint scope |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/sprint plan`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/projman:sprint-plan`)
