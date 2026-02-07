---
description: Architecture Decision Records management
---

# /adr

## Sub-commands

| Sub-command | Description |
|-------------|-------------|
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
