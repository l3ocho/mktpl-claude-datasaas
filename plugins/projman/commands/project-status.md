---
description: Full project hierarchy status view (absorbs /proposal-status)
agent: planner
---

# /project status

## Purpose

Display comprehensive project status including charter state, epic progress, risk summary, and sprint roadmap status. Absorbs the former `/proposal-status` functionality.

## Skills Required

- skills/project-charter.md — charter structure
- skills/visual-output.md — output formatting

## Workflow

### Step 1: Load Project Artifacts
Read wiki pages:
- `Project: {Name}` — charter and status
- `Roadmap: {Name}` — sprint sequence and completion
- `Risk-Register: {Name}` — open risks
- `WBS: {Name}` — work package completion

### Step 2: Aggregate Sprint Progress
For each sprint in the roadmap:
- Check milestone status (open/closed)
- Count issues by state (open/closed)
- Calculate completion percentage

### Step 3: Display Status

```
Project: {Name}
Status: Executing
Epics: 3/6 complete
Sprints: 4/8 closed
Open Risks: 2 (highest: R1 score 6)
Next Sprint: Sprint 5
```

### Step 4: Detail Sections
- Epic progress bars
- Top risks by score
- Upcoming sprint scope from roadmap
- ADR summary (accepted/proposed counts)
