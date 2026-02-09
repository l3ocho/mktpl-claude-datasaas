---
name: projman adr
description: Architecture Decision Records management — type /projman adr <action> for commands
---

# /adr

Architecture Decision Records management for projman.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Action | Command to Invoke | Description |
|--------|-------------------|-------------|
| `create` | `/projman:adr-create` | Create a new ADR wiki page |
| `list` | `/projman:adr-list` | List all ADRs by status |
| `update` | `/projman:adr-update` | Update an existing ADR |
| `supersede` | `/projman:adr-supersede` | Mark an ADR as superseded by a new one |

## Usage

```
/adr create "<title>"
/adr list [--status proposed|accepted|superseded|deprecated]
/adr update <ADR-NNNN> [--status accepted|deprecated]
/adr supersede <ADR-NNNN> --by <ADR-MMMM>
```

## Routing

If `$ARGUMENTS` is provided (e.g., user typed `/adr create`):
1. Match the first word of `$ARGUMENTS` against the **Action** column above
2. **Invoke the corresponding command** from the "Command to Invoke" column using the Skill tool
3. Pass any remaining arguments to the invoked command

If no arguments provided:
1. Display the Available Commands table
2. Ask: "Which action would you like to run?"
3. When the user responds, invoke the matching command using the Skill tool

**Note:** Commands can also be invoked directly using their plugin-prefixed names (e.g., `/projman:adr-create`)
