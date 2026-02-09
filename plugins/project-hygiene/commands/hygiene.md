---
name: hygiene
description: Project hygiene checks — type /hygiene <action> for commands
---

# /hygiene

Manual project hygiene checks for file organization and cleanup.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `check` | `/project-hygiene:hygiene-check` | Run project hygiene checks (temp files, misplaced files, empty dirs) |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/hygiene check`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/project-hygiene:hygiene-check`)
