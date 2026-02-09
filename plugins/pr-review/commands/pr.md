---
name: pr
description: Pull request review and management — type /pr <action> for commands
---

# /pr

Multi-agent pull request review with confidence scoring.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `review` | `/pr-review:pr-review` | Full multi-agent PR review with confidence scoring |
| `summary` | `/pr-review:pr-summary` | Quick summary of PR changes |
| `findings` | `/pr-review:pr-findings` | List and filter review findings by category/severity |
| `diff` | `/pr-review:pr-diff` | Formatted diff with inline review comments |
| `init` | `/pr-review:pr-init` | Quick project setup for PR reviews |
| `sync` | `/pr-review:pr-sync` | Sync config with git remote after repo move/rename |
| `setup` | `/pr-review:pr-setup` | Setup wizard for pr-review |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/pr review`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/pr-review:pr-review`)
