---
name: gitflow
description: Git workflow automation with safety enforcement — type /gitflow <action> for commands
---

# /gitflow

Git workflow automation with smart commits, branch management, and safety enforcement.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `setup` | `/git-flow:gitflow-setup` | Configure git-flow for the current project |
| `commit` | `/git-flow:gitflow-commit` | Smart commit with optional --push, --merge, --sync |
| `branch-start` | `/git-flow:gitflow-branch-start` | Create a properly-named feature branch |
| `branch-cleanup` | `/git-flow:gitflow-branch-cleanup` | Clean up merged/stale branches |
| `status` | `/git-flow:gitflow-status` | Enhanced git status with recommendations |
| `config` | `/git-flow:gitflow-config` | Configure git-flow settings |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/gitflow commit`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/git-flow:gitflow-commit`)
