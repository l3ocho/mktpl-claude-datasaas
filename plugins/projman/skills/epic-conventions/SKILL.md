---
description: Epic decomposition and management conventions using Gitea labels and projects
---

# Epic Conventions

## What Is an Epic

An epic is a large body of work that spans multiple sprints. Epics are tracked as Gitea labels (`Epic/*`) and optionally as Gitea Project boards.

## Label Convention

Labels follow the pattern `Epic/{Name}`:
- `Epic/Database` — Schema design, migrations, seed data
- `Epic/API` — Backend endpoints, middleware, auth
- `Epic/Frontend` — UI components, routing, state management
- `Epic/Auth` — Authentication and authorization
- `Epic/Infrastructure` — CI/CD, deployment, monitoring

Epics are defined during `/project initiation` as part of the charter's Epic Decomposition table.

## Epic-to-Sprint Mapping

Each sprint focuses on one or more epics. The sprint milestone description references the active epics:

```
**Epics:** Epic/Database, Epic/API
**Project:** Driving School SaaS
```

## Wiki Cross-References

- Project Charter (`Project: {Name}`) contains the Epic Decomposition table
- Sprint Roadmap (`Roadmap: {Name}`) maps epics to sprint sequence
- WBS (`WBS: {Name}`) breaks epics into work packages
- Sprint Lessons (`Sprint-Lessons: Sprint-X`) reference which epics were active

## Issue-Epic Relationship

Every issue in an epic-aligned sprint gets the `Epic/*` label. This enables:
- Filtering all issues by epic across sprints
- Tracking epic completion percentage
- Epic velocity analysis in lessons learned

## DO NOT

- Create epics for single-sprint work — use regular labels
- Mix unrelated work under one epic label
- Skip epic labels during sprint planning — they're the traceability link
