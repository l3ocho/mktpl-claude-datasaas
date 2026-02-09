---
name: sentinel
description: Security scanning and code refactoring — type /sentinel <action> for commands
---

# /sentinel

Security scanning and safe code refactoring tools.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/sentinel scan` | Full security audit (SQL injection, XSS, secrets, etc.) |
| `/sentinel refactor` | Apply refactoring patterns to improve code |
| `/sentinel refactor-dry` | Preview refactoring without applying changes |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
