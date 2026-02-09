---
name: projman project close
description: Close a completed project — retrospective, archive, lessons learned
agent: orchestrator
---

# /project close

## Purpose

Run project-level retrospective, capture lessons learned, and archive project artifacts.

## Prerequisites

- All sprints in roadmap are closed
- Project status is `Executing`

## Skills Required

- skills/project-charter.md — to update status
- skills/wiki-conventions.md — page naming
- skills/visual-output.md — output formatting

## Workflow

### Step 1: Verify Completion
Check that all sprints in `Roadmap: {Name}` are marked complete.
Check that all epic-labeled issues are closed.

### Step 2: Project Retrospective
Create a retrospective section in the project charter:
- What went well
- What didn't go well
- Key learnings
- Metrics: total sprints, total issues, duration

### Step 3: Archive
Update `Project: {Name}` status → `Closed`
Update `Risk-Register: {Name}` status → `Archived`

### Step 4: Final Report
Display project summary with key metrics.
