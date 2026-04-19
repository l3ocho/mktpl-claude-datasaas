---
name: sentinel
description: Code refactoring tools — type /sentinel <action> for commands
---

# /sentinel

Safe code refactoring tools. For full security audits (SQL injection, XSS, secrets, etc.), use the built-in `/security-review` command.

When invoked without a sub-command or with `$ARGUMENTS`, handle as follows:

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `refactor` | `/code-sentinel:sentinel-refactor` | Apply refactoring patterns to improve code |
| `refactor-dry` | `/code-sentinel:sentinel-refactor-dry` | Preview refactoring without applying changes |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/sentinel refactor`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** For security audits, use the built-in `/security-review` (covers SQL injection, XSS, auth flaws, secrets detection, and dependency vulnerabilities natively).
