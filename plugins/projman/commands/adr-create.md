---
description: Create a new Architecture Decision Record wiki page
agent: planner
---

# /adr create

## Skills Required

- skills/adr-conventions.md — ADR template and naming
- skills/wiki-conventions.md — page naming and dependency headers
- skills/visual-output.md — output formatting

## Workflow

### Step 1: Allocate ADR Number
Search existing wiki pages for `ADR-NNNN` pattern. Allocate next sequential number.

### Step 2: Gather Context
Ask user for:
- Title (short, decision-focused)
- Context (what prompted this decision)
- Options considered (at least 2)
- Recommended option

### Step 3: Create Wiki Page
Create `ADR-NNNN: {Title}` per `skills/adr-conventions.md` template.
Set status to `Proposed`.

### Step 4: Update ADR Index
Update or create `ADR-Index` wiki page, adding the new ADR under "Proposed".

### Step 5: Confirm
Display the created ADR and its URL.
