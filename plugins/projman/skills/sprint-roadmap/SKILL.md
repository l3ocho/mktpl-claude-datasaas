---
description: Sprint roadmap template for sequencing epics across multiple sprints
---

# Sprint Roadmap

## Wiki Page

Page name: `Roadmap: {Name}` (e.g., `Roadmap: Driving School SaaS`)

### Dependency Header

```
> **Project:** {Name}
> **Sprint:** N/A (project-level)
> **Issues:** N/A
> **Parent:** Project: {Name}
> **Created:** YYYY-MM-DD
> **Status:** Draft | Active | Complete
```

## Roadmap Template

| Sprint | Epics | Focus | Dependencies | Status |
|--------|-------|-------|-------------|--------|
| Sprint 1 | Epic/Database | Schema design, initial migrations | None | Planned |
| Sprint 2 | Epic/Database, Epic/API | Seed data, API scaffolding | Sprint 1 | Planned |

## Milestones

| Milestone | Target Sprint | Criteria |
|-----------|--------------|----------|
| Backend MVP | Sprint 3 | All core API endpoints passing tests |
| Integration Complete | Sprint 6 | End-to-end flows working |

## Integration

- `/project plan` creates the initial roadmap from epic decomposition + dependency analysis
- `/sprint plan` references the roadmap to determine sprint scope
- `/sprint close` updates sprint status in roadmap
- `/project status` shows roadmap progress
