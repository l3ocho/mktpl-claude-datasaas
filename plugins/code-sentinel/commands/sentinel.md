---
name: sentinel
description: Security scanning and code refactoring — type /sentinel <action> for commands
---

# /sentinel

Security scanning and safe code refactoring tools.

When invoked without a sub-command or with `$ARGUMENTS`, handle as follows:

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `scan` | `/code-sentinel:sentinel-scan` | Full security audit (SQL injection, XSS, secrets, etc.) |
| `refactor` | `/code-sentinel:sentinel-refactor` | Apply refactoring patterns to improve code |
| `refactor-dry` | `/code-sentinel:sentinel-refactor-dry` | Preview refactoring without applying changes |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/sentinel scan`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/code-sentinel:sentinel-scan`)
