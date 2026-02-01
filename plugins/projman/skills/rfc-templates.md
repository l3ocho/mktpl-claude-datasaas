---
name: rfc-templates
description: RFC page templates and frontmatter format specifications
---

# RFC Templates

## Purpose

Provides templates for RFC wiki pages and defines the required/optional sections for complete RFC documentation.

## When to Use

- **Commands**: `/rfc-create` when generating new RFC pages
- **Integration**: Referenced by `rfc-workflow.md` for page structure

---

## RFC Page Frontmatter

Every RFC page starts with a metadata block using blockquote format:

```markdown
> **RFC:** 0001
> **Title:** Short Descriptive Title
> **Status:** Draft
> **Author:** @username
> **Created:** 2026-01-25
> **Updated:** 2026-01-25
> **Champion:** (unassigned)
> **Sprint:** (none)
> **Superseded-By:** (none)
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `RFC` | Yes | 4-digit RFC number (e.g., 0001) |
| `Title` | Yes | Short descriptive title |
| `Status` | Yes | Current lifecycle status |
| `Author` | Yes | Original RFC author |
| `Created` | Yes | Creation date (YYYY-MM-DD) |
| `Updated` | Yes | Last update date (YYYY-MM-DD) |
| `Champion` | No | Assigned reviewer/sponsor |
| `Sprint` | No | Sprint reference when implementing |
| `Superseded-By` | No | RFC number if superseded |

---

## Full RFC Page Template

```markdown
> **RFC:** NNNN
> **Title:** [Short Title]
> **Status:** Draft
> **Author:** @[username]
> **Created:** YYYY-MM-DD
> **Updated:** YYYY-MM-DD
> **Champion:** (unassigned)
> **Sprint:** (none)
> **Superseded-By:** (none)

# RFC-NNNN: [Full Title]

## Summary

A brief (2-3 paragraph) explanation of the proposed change. This should be understandable by someone unfamiliar with the codebase.

**What:** What is being proposed?
**Why:** Why is this change needed?
**Impact:** What will be different after this is implemented?

## Motivation

### Problem Statement

Describe the problem this RFC addresses. Include:
- Current pain points or limitations
- User stories or use cases
- Why existing solutions are insufficient

### Goals

- [ ] Goal 1: Specific, measurable outcome
- [ ] Goal 2: Another specific outcome
- [ ] Goal 3: Third outcome

### Non-Goals

What is explicitly out of scope for this RFC:
- Non-goal 1
- Non-goal 2

## Detailed Design

### Overview

High-level description of the solution approach.

### Architecture

Describe the technical architecture:
- Components involved
- Data flow
- Integration points

### Implementation Details

#### Component 1

Detailed implementation for component 1.

#### Component 2

Detailed implementation for component 2.

### API/Interface Changes

If applicable, describe any API or interface changes:

```python
# Example new API
def new_function(param1: str, param2: int) -> dict:
    """Description of new function."""
    pass
```

### Database/Storage Changes

If applicable, describe any data model changes.

### Configuration Changes

If applicable, describe any new configuration options.

## Alternatives Considered

### Alternative 1: [Name]

**Description:** Brief description of this alternative.

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Why not chosen:** Explanation.

### Alternative 2: [Name]

**Description:** Brief description of this alternative.

**Pros:**
- Pro 1

**Cons:**
- Con 1

**Why not chosen:** Explanation.

## Unresolved Questions

Questions that need to be answered before or during implementation:

1. **Question 1:** Description of open question
   - Possible answer A
   - Possible answer B

2. **Question 2:** Description of another open question

## Dependencies

- Dependency 1: Description and status
- Dependency 2: Description and status

## Security Considerations

Describe any security implications:
- Authentication/authorization impacts
- Data privacy considerations
- Potential attack vectors and mitigations

## Testing Strategy

How will this be tested:
- Unit tests
- Integration tests
- Manual testing checklist

## Rollout Plan

How will this be deployed:
- Feature flags
- Phased rollout
- Rollback strategy

---

## Review Notes

*(Added during Review phase)*

### Review Discussion

Summary of review feedback and discussions.

### Changes Made

List of changes made in response to review feedback.

---

## Decision

*(Added when Approved or Rejected)*

**Decision:** [Approved/Rejected]
**Date:** YYYY-MM-DD
**Decided By:** @[username]

**Rationale:**

Explanation of the decision.

---

## Implementation

*(Added during Implementing phase)*

**Sprint:** [Sprint reference]
**Started:** YYYY-MM-DD
**Issues:**
- #123: Issue title
- #124: Another issue

### Progress Notes

Updates during implementation.

---

## Completion

*(Added when Implemented)*

**Completed:** YYYY-MM-DD
**Release:** vX.Y.Z
**Lessons Learned:** [Link to lessons wiki page]

### Final Notes

Summary of what was implemented and any deviations from the original design.
```

---

## Section Requirements by Status

### Draft (Minimum)
- Summary (complete)
- Motivation (at least Problem Statement)
- Detailed Design (at least Overview)

### Review (Required)
All Draft sections plus:
- Alternatives Considered (at least 1)
- Unresolved Questions (can be empty if none)

### Approved (Required)
All Review sections plus:
- Decision section with approval

### Implementing (Required)
All Approved sections plus:
- Implementation section with Sprint and Issues

### Implemented (Required)
All Implementing sections plus:
- Completion section

---

## RFC-Index Entry Format

### Draft Section Entry
```markdown
| [RFC-0005](RFC-0005:-Idea-Z) | Idea Z | @user | 2026-01-25 |
```

### Review Section Entry
```markdown
| [RFC-0004](RFC-0004:-Feature-Y) | Feature Y | @user | 2026-01-20 |
```

### Approved Section Entry
```markdown
| [RFC-0003](RFC-0003:-Feature-X) | Feature X | @champion | 2026-01-15 |
```

### Implementing Section Entry
```markdown
| [RFC-0002](RFC-0002:-Feature-W) | Feature W | Sprint 18 | 2026-01-22 |
```

### Implemented Section Entry
```markdown
| [RFC-0001](RFC-0001:-Initial-Feature) | Initial Feature | 2026-01-10 | v5.0.0 |
```

### Rejected Section Entry
```markdown
| [RFC-0006](RFC-0006:-Rejected-Idea) | Rejected Idea | Out of scope | 2026-01-18 |
```

---

## Minimal RFC Template (Quick Start)

For rapid RFC creation from conversation:

```markdown
> **RFC:** NNNN
> **Title:** [Title]
> **Status:** Draft
> **Author:** @[username]
> **Created:** YYYY-MM-DD
> **Updated:** YYYY-MM-DD
> **Champion:** (unassigned)
> **Sprint:** (none)
> **Superseded-By:** (none)

# RFC-NNNN: [Title]

## Summary

[Brief description of the proposal]

## Motivation

### Problem Statement

[What problem does this solve?]

### Goals

- [ ] [Primary goal]

## Detailed Design

### Overview

[High-level approach]

## Alternatives Considered

*(To be added during review)*

## Unresolved Questions

- [Any open questions?]
```

---

## Creating RFC from Clarified Spec

When `/clarify` provides a clarified specification, map sections:

| Clarify Output | RFC Section |
|----------------|-------------|
| Problem/Context | Motivation > Problem Statement |
| Goals/Outcomes | Motivation > Goals |
| Scope/Requirements | Detailed Design > Overview |
| Constraints | Detailed Design or Non-Goals |
| Success Criteria | Testing Strategy |
