---
description: Update an existing ADR's content or status
agent: planner
---

# /adr update

## Skills Required

- skills/adr-conventions.md — ADR template
- skills/wiki-conventions.md — page naming

## Workflow

### Step 1: Load ADR
Read `ADR-NNNN: {Title}` wiki page.

### Step 2: Apply Updates
Update content or status as specified. Valid status transitions:
- Proposed → Accepted
- Proposed → Deprecated
- Accepted → Deprecated

### Step 3: Update ADR Index
Move ADR to correct status section in `ADR-Index`.
