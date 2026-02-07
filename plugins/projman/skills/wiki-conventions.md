---
description: Wiki page naming conventions and dependency headers (Decision #30)
---

# Wiki Conventions

## Purpose

Defines naming conventions, dependency headers, and structure for all wiki pages in the project management workflow.

## When to Use

- **Planner agent**: When creating wiki pages during planning
- **Orchestrator agent**: When updating status at sprint close
- **Commands**: `/sprint plan`, `/sprint close`, `/project initiation`, `/project plan`, `/project status`, `/project close`, `/adr create`

---

## Page Naming Pattern

All wiki pages follow: `{Type}-{ID}: {Title}` or `{Type}: {Title}`

| Type | ID Format | Example |
|------|-----------|---------|
| RFC | NNNN (sequential) | `RFC-0001: OAuth2 Provider Support` |
| ADR | NNNN (sequential) | `ADR-0001: Use PostgreSQL with Alembic` |
| Project | Name | `Project: Driving School SaaS` |
| WBS | Name | `WBS: Driving School SaaS` |
| Risk-Register | Name | `Risk-Register: Driving School SaaS` |
| Roadmap | Name | `Roadmap: Driving School SaaS` |
| Sprint-Lessons | Sprint ID | `Sprint-Lessons: Sprint-3` |
| ADR-Index | — | `ADR-Index` |
| Change Proposal | Version | `Change VXX.X.X: Proposal` |
| Implementation | Version + N | `Change VXX.X.X: Proposal (Implementation N)` |

## Dependency Header

Every wiki page MUST include this header block:

```markdown
> **Project:** [project name or N/A]
> **Sprint:** [sprint milestone or N/A]
> **Issues:** #12, #15, #18 [or N/A]
> **Parent:** [parent wiki page or N/A]
> **Created:** YYYY-MM-DD
> **Status:** [lifecycle state]
```

## Hierarchy

- `Project: {Name}` is the root
  - `WBS: {Name}` (parent: Project)
  - `Risk-Register: {Name}` (parent: Project)
  - `Roadmap: {Name}` (parent: Project)
  - `ADR-NNNN: {Title}` (parent: Project)
  - `Sprint-Lessons: Sprint-X` (parent: Project)

---

## Change Proposal Pages (Legacy Format)

### Proposal Page Template

```markdown
> **Type:** Change Proposal
> **Version:** VXX.X.X
> **Plugin:** projman
> **Status:** In Progress
> **Date:** YYYY-MM-DD

# Feature Title

[Content migrated from input source or created from discussion]

## Implementations
- [Implementation 1](link) - Sprint N - In Progress
```

### Implementation Page Template

```markdown
> **Type:** Change Proposal Implementation
> **Version:** VXX.X.X
> **Status:** In Progress
> **Date:** YYYY-MM-DD
> **Origin:** [Proposal](wiki-link)
> **Sprint:** Sprint N

# Implementation Details

[Technical details, scope, approach]

## Issues
- #45: Issue description
- #46: Issue description
```

---

## Status Values

| Status | Meaning |
|--------|---------|
| `In Progress` | Active work |
| `Implemented` | Completed successfully |
| `Partial` | Partially completed, continued in next impl |
| `Failed` | Did not complete, abandoned |

---

## Completion Update (Sprint Close)

On sprint close, update implementation page status to `Implemented` and add a `## Completion Summary` section with lessons learned link.

On proposal page, update implementation entries with completion status.

---

## R&D Notes Section

Lessons learned pages include a `## R&D Notes` section at the bottom for capturing:

| Label | Description | Action |
|-------|-------------|--------|
| `RnD/Friction` | Workflow friction points | Consider improvements |
| `RnD/Gap` | Capability gaps discovered | Prioritize new tools |
| `RnD/Pattern` | Reusable patterns identified | Document for reuse |
| `RnD/Automation` | Automation opportunities | Add to backlog |

---

## Enforcement

- Commands creating wiki pages use these templates from their respective skills
- Malformed pages are flagged, not auto-corrected
