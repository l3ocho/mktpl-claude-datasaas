---
description: Architecture Decision Record conventions and wiki page template
---

# ADR Conventions

## Wiki Page Naming

Page name: `ADR-NNNN: {Title}` (e.g., `ADR-0001: Use PostgreSQL with Alembic`)

Sequential numbering. Allocate next available number.

## Dependency Header

```
> **Project:** {Name}
> **Sprint:** N/A or sprint where ADR was created
> **Issues:** Related issue numbers or N/A
> **Parent:** Project: {Name}
> **Created:** YYYY-MM-DD
> **Status:** Proposed | Accepted | Superseded | Deprecated
```

## ADR Template

1. **Context** — What is the issue motivating this decision?
2. **Decision** — What is the change being proposed/made?
3. **Consequences** — Positive, Negative, Neutral outcomes
4. **Alternatives Considered** — Table of options with pros, cons, verdict
5. **References** — Related ADRs, RFCs, external links

## Lifecycle

| State | Meaning |
|-------|---------|
| Proposed | Under discussion, not yet approved |
| Accepted | Approved and in effect |
| Superseded | Replaced by a newer ADR (link to replacement) |
| Deprecated | No longer relevant |

## ADR Index Page

Maintain an `ADR-Index` wiki page listing all ADRs grouped by status.

## Integration with Sprint Workflow

- ADRs created via `/adr create` during project initiation or planning
- ADR status checked during `/project status`
- Sprint planning can reference ADRs in issue descriptions
