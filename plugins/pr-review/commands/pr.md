---
name: pr
description: Pull request review and management — type /pr <action> for commands
---

# /pr

Multi-agent pull request review with confidence scoring.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/pr review` | Full multi-agent PR review with confidence scoring |
| `/pr summary` | Quick summary of PR changes |
| `/pr findings` | List and filter review findings by category/severity |
| `/pr diff` | Formatted diff with inline review comments |
| `/pr init` | Quick project setup for PR reviews |
| `/pr sync` | Sync config with git remote after repo move/rename |
| `/pr setup` | Setup wizard for pr-review |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
