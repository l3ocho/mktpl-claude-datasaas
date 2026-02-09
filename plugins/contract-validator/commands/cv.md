---
name: cv
description: Cross-plugin compatibility validation — type /cv <action> for commands
---

# /cv

Cross-plugin compatibility validation and agent verification.
When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `validate` | `/contract-validator:cv-validate` | Full marketplace compatibility validation |
| `check-agent` | `/contract-validator:cv-check-agent` | Validate single agent definition |
| `list-interfaces` | `/contract-validator:cv-list-interfaces` | Show all plugin interfaces |
| `dependency-graph` | `/contract-validator:cv-dependency-graph` | Mermaid visualization of plugin dependencies |
| `setup` | `/contract-validator:cv-setup` | Setup wizard for contract-validator MCP |
| `status` | `/contract-validator:cv-status` | Marketplace-wide health check |

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/cv validate`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/contract-validator:cv-validate`)
