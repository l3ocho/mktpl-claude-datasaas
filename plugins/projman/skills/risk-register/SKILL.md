---
description: Risk register template and management conventions for project planning
---

# Risk Register

## Wiki Page

Page name: `Risk-Register: {Name}` (e.g., `Risk-Register: Driving School SaaS`)

### Dependency Header

```
> **Project:** {Name}
> **Sprint:** N/A (project-level, reviewed per sprint)
> **Issues:** N/A
> **Parent:** Project: {Name}
> **Created:** YYYY-MM-DD
> **Status:** Active | Archived
```

## Risk Register Template

| ID | Risk | Probability | Impact | Score | Mitigation | Owner | Status |
|----|------|------------|--------|-------|------------|-------|--------|
| R1 | Example risk description | Medium | High | 6 | Mitigation strategy | Dev | Open |

## Scoring

| Probability | Value |
|-------------|-------|
| Low | 1 |
| Medium | 2 |
| High | 3 |

| Impact | Value |
|--------|-------|
| Low | 1 |
| Medium | 2 |
| High | 3 |

**Score** = Probability x Impact (1-9 range)

## Risk Lifecycle

| Status | Meaning |
|--------|---------|
| Open | Active risk, mitigation planned |
| Monitoring | Risk identified but not yet actionable |
| Mitigated | Mitigation applied, risk reduced |
| Occurred | Risk materialized — track resolution |
| Closed | No longer relevant |

## Integration

- `/project plan` creates initial risk register
- `/project status` summarizes open risk count and top-3 by score
- `/sprint close` updates risk statuses in lessons learned
