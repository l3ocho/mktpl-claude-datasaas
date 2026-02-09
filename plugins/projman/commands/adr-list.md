---
name: projman adr list
description: List all ADRs grouped by status
agent: planner
---

# /adr list

## Skills Required

- skills/adr-conventions.md — ADR lifecycle states
- skills/visual-output.md — output formatting

## Workflow

### Step 1: Read ADR Index
Load `ADR-Index` wiki page.

### Step 2: Display
Group ADRs by status (Accepted, Proposed, Superseded, Deprecated).
Show table with ID, Title, Date, Status.

### Optional Filter
`/adr list --status proposed` — show only proposed ADRs.
