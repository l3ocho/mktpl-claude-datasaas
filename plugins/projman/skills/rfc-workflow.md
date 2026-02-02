---
name: rfc-workflow
description: RFC lifecycle management, state transitions, and wiki page conventions
---

# RFC Workflow

## Purpose

Defines the Request for Comments (RFC) system for capturing, reviewing, and tracking feature ideas through their lifecycle from initial proposal to implementation.

## When to Use

- **Planner agent**: When detecting approved RFCs for sprint planning
- **Commands**: `/rfc create`, `/rfc list`, `/rfc review`, `/rfc approve`, `/rfc reject`
- **Integration**: With `/sprint-plan` to select approved RFCs for implementation

---

## RFC Lifecycle States

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
                    ▼                                              │
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────────┐    │
│  Draft  │───▶│ Review  │───▶│ Approved │───▶│ Implementing │────┤
└─────────┘    └─────────┘    └──────────┘    └──────────────┘    │
     │              │                               │              │
     │              │                               ▼              │
     │              │                        ┌─────────────┐       │
     │              │                        │ Implemented │       │
     │              │                        └─────────────┘       │
     │              │                               │              │
     │              ▼                               ▼              │
     │         ┌──────────┐                  ┌────────────┐        │
     │         │ Rejected │                  │ Superseded │        │
     │         └──────────┘                  └────────────┘        │
     │                                                             │
     ▼                                                             │
┌─────────┐                                                        │
│  Stale  │────────────────────────────────────────────────────────┘
└─────────┘    (revived → Draft)
```

---

## State Definitions

| Status | Meaning | Valid Transitions |
|--------|---------|-------------------|
| `Draft` | Idea captured, needs refinement | → Review, → Stale |
| `Review` | Being evaluated by maintainers | → Approved, → Rejected, → Draft |
| `Approved` | Ready for sprint planning | → Implementing |
| `Rejected` | Declined with documented reason | (terminal) |
| `Implementing` | Active sprint work in progress | → Implemented, → Draft (if blocked) |
| `Implemented` | Completed, links to release | → Superseded |
| `Stale` | Draft with no activity >90 days | → Draft (if revived) |
| `Superseded` | Replaced by newer RFC | (terminal) |

---

## State Transition Rules

### Draft → Review
- **Who can transition**: RFC author or any maintainer
- **Requirements**: RFC has complete Summary, Motivation, and Detailed Design sections
- **Action**: Update status, optionally assign champion

### Review → Approved
- **Who can transition**: Maintainer or designated reviewer
- **Requirements**: Review discussion complete, no blocking concerns
- **Action**: Update status, add Decision section with approval reason

### Review → Rejected
- **Who can transition**: Maintainer or designated reviewer
- **Requirements**: Reason must be documented
- **Action**: Update status, add Decision section with rejection reason

### Approved → Implementing
- **Who can transition**: Planner agent via `/sprint-plan`
- **Requirements**: RFC selected for sprint
- **Action**: Update status, add Sprint reference, update RFC-Index

### Implementing → Implemented
- **Who can transition**: Orchestrator agent via `/sprint-close`
- **Requirements**: Sprint completed successfully
- **Action**: Update status, add completion date, link to lessons learned

### Implementing → Draft
- **Who can transition**: Any maintainer
- **Requirements**: Implementation blocked, needs rework
- **Action**: Update status, add Implementation Notes explaining why

### Draft → Stale
- **Automatic**: No activity for 90 days
- **Action**: Update status in RFC-Index

### Stale → Draft
- **Who can transition**: Anyone
- **Requirements**: Renewed interest, updated content
- **Action**: Update status, add Revival Notes

### Implemented → Superseded
- **Who can transition**: Any maintainer
- **Requirements**: New RFC replaces functionality
- **Action**: Update status, add Superseded-By reference

---

## Wiki Page Naming

| Page Type | Naming Convention | Example |
|-----------|-------------------|---------|
| RFC Page | `RFC-NNNN: Short Title` | `RFC-0001: RFC System Implementation` |
| Index Page | `RFC-Index` | `RFC-Index` |

**Number Format:**
- 4-digit zero-padded (0001, 0002, 0003, ...)
- Sequential, never reused
- Allocated via `allocate_rfc_number` MCP tool

---

## Number Allocation Logic

```python
# Pseudocode for allocate_rfc_number
async def allocate_rfc_number(repo):
    pages = await list_wiki_pages(repo)
    rfc_pages = [p for p in pages if p['title'].startswith('RFC-')]

    if not rfc_pages:
        return {'next_number': 1, 'formatted': 'RFC-0001'}

    numbers = []
    for page in rfc_pages:
        # Extract number from "RFC-NNNN: Title"
        match = re.match(r'RFC-(\d{4})', page['title'])
        if match:
            numbers.append(int(match.group(1)))

    next_num = max(numbers) + 1 if numbers else 1
    return {
        'next_number': next_num,
        'formatted': f'RFC-{next_num:04d}'
    }
```

---

## RFC-Index Page Format

The RFC-Index page organizes RFCs by status:

```markdown
# RFC Index

## Approved

RFCs ready for implementation in upcoming sprints.

| RFC | Title | Champion | Created |
|-----|-------|----------|---------|
| [RFC-0003](RFC-0003:-Feature-X) | Feature X | @user | 2026-01-15 |

## In Review

RFCs currently being evaluated.

| RFC | Title | Author | Created |
|-----|-------|--------|---------|
| [RFC-0004](RFC-0004:-Feature-Y) | Feature Y | @user | 2026-01-20 |

## Draft

RFCs in early development.

| RFC | Title | Author | Created |
|-----|-------|--------|---------|
| [RFC-0005](RFC-0005:-Idea-Z) | Idea Z | @user | 2026-01-25 |

## Implementing

RFCs currently being implemented.

| RFC | Title | Sprint | Started |
|-----|-------|--------|---------|
| [RFC-0002](RFC-0002:-Feature-W) | Feature W | Sprint 18 | 2026-01-22 |

## Implemented

Completed RFCs.

| RFC | Title | Completed | Release |
|-----|-------|-----------|---------|
| [RFC-0001](RFC-0001:-Initial-Feature) | Initial Feature | 2026-01-10 | v5.0.0 |

## Rejected

RFCs that were declined.

| RFC | Title | Reason | Date |
|-----|-------|--------|------|
| [RFC-0006](RFC-0006:-Rejected-Idea) | Rejected Idea | Out of scope | 2026-01-18 |

## Stale

Inactive RFCs (no updates >90 days).

| RFC | Title | Last Updated |
|-----|-------|--------------|
```

---

## Creating RFC-Index

If RFC-Index doesn't exist when creating first RFC:

```python
create_wiki_page(
    repo="org/repo",
    title="RFC-Index",
    content="""# RFC Index

## Approved

RFCs ready for implementation in upcoming sprints.

| RFC | Title | Champion | Created |
|-----|-------|----------|---------|

## In Review

RFCs currently being evaluated.

| RFC | Title | Author | Created |
|-----|-------|--------|---------|

## Draft

RFCs in early development.

| RFC | Title | Author | Created |
|-----|-------|--------|---------|

## Implementing

RFCs currently being implemented.

| RFC | Title | Sprint | Started |
|-----|-------|--------|---------|

## Implemented

Completed RFCs.

| RFC | Title | Completed | Release |
|-----|-------|-----------|---------|

## Rejected

RFCs that were declined.

| RFC | Title | Reason | Date |
|-----|-------|--------|------|

## Stale

Inactive RFCs (no updates >90 days).

| RFC | Title | Last Updated |
|-----|-------|--------------|
"""
)
```

---

## Updating RFC-Index

When RFC status changes:

1. Fetch current RFC-Index content
2. Parse sections by status header
3. Remove RFC entry from old section (if present)
4. Add RFC entry to new section
5. Update wiki page

**Example status change (Draft → Review):**
1. Remove from "## Draft" section
2. Add to "## In Review" section

---

## Integration Points

| Component | How It Uses RFC System |
|-----------|------------------------|
| `/rfc create` | Creates RFC page + updates RFC-Index |
| `/rfc list` | Reads and displays RFC-Index |
| `/rfc review` | Transitions Draft -> Review |
| `/rfc approve` | Transitions Review -> Approved |
| `/rfc reject` | Transitions Review/Draft -> Rejected |
| `/sprint-plan` | Detects Approved RFCs, transitions to Implementing |
| `/sprint-close` | Transitions Implementing -> Implemented |
| `clarity-assist` | Suggests `/rfc create` for feature ideas |
