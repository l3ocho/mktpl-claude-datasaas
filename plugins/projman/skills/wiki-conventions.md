---
name: wiki-conventions
description: Proposal and implementation page format and naming conventions
---

# Wiki Conventions

## Purpose

Defines the naming and structure for wiki proposal and implementation pages.

## When to Use

- **Planner agent**: When creating wiki pages during planning
- **Orchestrator agent**: When updating status at sprint close
- **Commands**: `/sprint-plan`, `/sprint-close`, `/proposal-status`

---

## Page Naming

| Page Type | Naming Convention |
|-----------|-------------------|
| Proposal | `Change VXX.X.X: Proposal` |
| Implementation | `Change VXX.X.X: Proposal (Implementation N)` |

**Examples:**
- `Change V4.1.0: Proposal`
- `Change V4.1.0: Proposal (Implementation 1)`
- `Change V4.1.0: Proposal (Implementation 2)`

---

## Proposal Page Template

```markdown
> **Type:** Change Proposal
> **Version:** V04.1.0
> **Plugin:** projman
> **Status:** In Progress
> **Date:** 2026-01-26

# Feature Title

[Content migrated from input source or created from discussion]

## Implementations
- [Implementation 1](link) - Sprint 17 - In Progress
```

---

## Implementation Page Template

```markdown
> **Type:** Change Proposal Implementation
> **Version:** V04.1.0
> **Status:** In Progress
> **Date:** 2026-01-26
> **Origin:** [Proposal](wiki-link)
> **Sprint:** Sprint 17

# Implementation Details

[Technical details, scope, approach]

## Issues
- #45: JWT token generation
- #46: Login endpoint
- #47: Auth tests
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

On sprint close, update implementation page:

```markdown
> **Type:** Change Proposal Implementation
> **Version:** V04.1.0
> **Status:** Implemented ✅
> **Date:** 2026-01-26
> **Completed:** 2026-01-28
> **Origin:** [Proposal](wiki-link)
> **Sprint:** Sprint 17

# Implementation Details
[Original content...]

## Completion Summary
- All planned issues completed
- Lessons learned: [Link to lesson]
```

---

## Proposal Status Update

When all implementations complete, update proposal:

```markdown
> **Type:** Change Proposal
> **Version:** V04.1.0
> **Status:** Implemented ✅
> **Date:** 2026-01-26

# Feature Title
[Original content...]

## Implementations
- [Implementation 1](link) - Sprint 17 - ✅ Completed
```

---

## Creating Pages

**Create proposal:**
```python
create_wiki_page(
    repo="org/repo",
    title="Change V4.1.0: Proposal",
    content="[proposal template content]"
)
```

**Create implementation:**
```python
create_wiki_page(
    repo="org/repo",
    title="Change V4.1.0: Proposal (Implementation 1)",
    content="[implementation template content]"
)
```

**Update implementation on close:**
```python
update_wiki_page(
    repo="org/repo",
    page_name="Change-V4.1.0:-Proposal-(Implementation-1)",
    content="[updated content with completion status]"
)
```
