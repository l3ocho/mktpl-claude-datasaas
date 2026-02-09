---
name: labels
description: Label management — type /labels <action> for commands
---

# /labels

Label management for projman.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `sync` | `/projman:labels-sync` | Sync label taxonomy to Gitea repository |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/labels sync`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/projman:labels-sync`)
