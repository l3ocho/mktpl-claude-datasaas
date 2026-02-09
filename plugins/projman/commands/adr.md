---
name: adr
description: Architecture Decision Records management — type /adr <action> for commands
---

# /adr

Architecture Decision Records management for projman.

When invoked without a sub-command, display available actions and ask which to run.

## Available Commands

| Command | Description |
|---------|-------------|
| `/adr create` | Create a new ADR wiki page |
| `/adr list` | List all ADRs by status |
| `/adr update` | Update an existing ADR |
| `/adr supersede` | Mark an ADR as superseded by a new one |

## Usage

```
/adr create "<title>"
/adr list [--status proposed|accepted|superseded|deprecated]
/adr update <ADR-NNNN> [--status accepted|deprecated]
/adr supersede <ADR-NNNN> --by <ADR-MMMM>
```

## Workflow

1. Display the table above
2. Ask: "Which command would you like to run?"
3. Route to the selected sub-command
