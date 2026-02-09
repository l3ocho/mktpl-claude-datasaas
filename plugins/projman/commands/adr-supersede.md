---
name: projman adr supersede
description: Mark an ADR as superseded by a newer ADR
agent: planner
---

# /adr supersede

## Skills Required

- skills/adr-conventions.md — ADR lifecycle
- skills/wiki-conventions.md — page naming

## Workflow

### Step 1: Validate
Verify both ADRs exist. The superseding ADR should be in `Accepted` or `Proposed` state.

### Step 2: Update Old ADR
Set status to `Superseded`. Add note: "Superseded by ADR-MMMM: {Title}".

### Step 3: Update New ADR
Add note: "Supersedes ADR-NNNN: {Title}".

### Step 4: Update ADR Index
Move old ADR to "Superseded" section.
