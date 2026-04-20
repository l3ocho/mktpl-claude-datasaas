---
description: Template and conventions for project charter wiki pages
---

# Project Charter Conventions

## Wiki Page Naming

Page name: `Project: {Name}` (e.g., `Project: Driving School SaaS`)

## Dependency Header

```
> **Project:** {Name}
> **Sprint:** N/A (project-level)
> **Issues:** N/A (created during planning)
> **Parent:** N/A (top-level artifact)
> **Created:** YYYY-MM-DD
> **Status:** Initiating | Planning | Executing | Closing | Closed
```

## Charter Structure

The wiki page follows this structure:

1. **Vision** — One paragraph describing what this project achieves and why
2. **Scope** — In Scope (explicit list) and Out of Scope (prevents scope creep)
3. **Source Analysis Summary** — Key findings from `/project initiation` (if applicable)
4. **Architecture Decisions** — Links to ADR wiki pages
5. **Epic Decomposition** — Table of epics with description, priority, estimated sprints
6. **Sprint Roadmap** — Link to `Roadmap: {Name}` wiki page
7. **Risk Register** — Link to `Risk-Register: {Name}` wiki page
8. **Stakeholders** — Table of roles, persons, responsibilities
9. **Success Criteria** — Measurable outcomes that define "done"

## Lifecycle States

| State | Meaning | Transition |
|-------|---------|------------|
| Initiating | Discovery and chartering in progress | Planning (charter approved) |
| Planning | WBS, risk, roadmap being created | Executing (first sprint starts) |
| Executing | Sprints are running | Closing (all epics complete) |
| Closing | Retrospective and archival | Closed |
| Closed | Archived | Terminal |

State is tracked in the charter's `Status` field.
