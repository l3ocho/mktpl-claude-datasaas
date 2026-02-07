---
description: Work Breakdown Structure skill for decomposing projects and sprints into implementable work packages
---

# Work Breakdown Structure (WBS)

## Purpose

Bridges project-level epics and sprint-level issues. Used by `/project plan` to create the initial decomposition and by `/sprint plan` to refine sprint scope.

## Wiki Page

Page name: `WBS: {Name}` (e.g., `WBS: Driving School SaaS`)

### Dependency Header

```
> **Project:** {Name}
> **Sprint:** N/A (project-level, refined per sprint)
> **Issues:** N/A
> **Parent:** Project: {Name}
> **Created:** YYYY-MM-DD
> **Status:** Draft | Active | Complete
```

## Decomposition Rules

1. **Level 1:** Epics (from project charter)
2. **Level 2:** Work packages (groupings within an epic — typically 1 sprint each)
3. **Level 3:** Tasks (become Gitea issues — must be S or M size per task-sizing.md)

## Sprint Refinement

During `/sprint plan`, the planner:
1. Loads the WBS
2. Identifies the next unstarted work packages
3. Creates issues from Level 3 tasks
4. Marks consumed work packages as "Sprint-X" in the WBS

## Integration

- `/project plan` creates the initial WBS from epic decomposition
- `/sprint plan` consumes WBS work packages to create sprint issues
- `/sprint close` updates WBS with completion status
- `/project status` aggregates WBS progress for project-level view
