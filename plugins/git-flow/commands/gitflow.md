---
name: gitflow
description: Git workflow automation with safety enforcement — type /gitflow <action> for commands
---

# /gitflow

Git workflow automation with smart commits, branch management, and safety enforcement.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/gitflow setup` | Configure git-flow for the current project |
| `/gitflow commit` | Smart commit with optional --push, --merge, --sync |
| `/gitflow branch-start` | Create a properly-named feature branch |
| `/gitflow branch-cleanup` | Clean up merged/stale branches |
| `/gitflow status` | Enhanced git status with recommendations |
| `/gitflow config` | Configure git-flow settings |

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
