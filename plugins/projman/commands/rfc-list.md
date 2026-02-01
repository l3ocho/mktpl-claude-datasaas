---
description: List all RFCs grouped by status from RFC-Index wiki page
agent: planner
---

# List RFCs

## Skills Required

- skills/mcp-tools-reference.md
- skills/rfc-workflow.md

## Purpose

Display all RFCs grouped by their lifecycle status. Highlights "Approved" RFCs that are ready for sprint planning.

## Invocation

Run `/rfc-list` to see all RFCs.

Optional filters:
- `/rfc-list approved` - Show only approved RFCs
- `/rfc-list draft` - Show only draft RFCs
- `/rfc-list review` - Show only RFCs in review

## Workflow

1. **Fetch RFC-Index**
   - Call `get_wiki_page` for "RFC-Index"
   - Handle missing index gracefully

2. **Parse Sections**
   - Extract tables from each status section
   - Parse RFC number, title, and metadata from each row

3. **Display Results**
   - Group by status
   - Highlight Approved section (ready for planning)
   - Show counts per status

## Visual Output

```
+----------------------------------------------------------------------+
|  PROJMAN - RFC Index                                                 |
+----------------------------------------------------------------------+

## Approved (Ready for Sprint Planning)

| RFC | Title | Champion | Created |
|-----|-------|----------|---------|
| RFC-0003 | Feature X | @user | 2026-01-15 |
| RFC-0007 | Enhancement Y | @user | 2026-01-28 |

## In Review (2)

| RFC | Title | Author | Created |
|-----|-------|--------|---------|
| RFC-0004 | Feature Y | @user | 2026-01-20 |
| RFC-0008 | Idea Z | @user | 2026-01-29 |

## Draft (3)

| RFC | Title | Author | Created |
|-----|-------|--------|---------|
| RFC-0005 | Concept A | @user | 2026-01-22 |
| RFC-0009 | Proposal B | @user | 2026-01-30 |
| RFC-0010 | Sketch C | @user | 2026-01-30 |

## Implementing (1)

| RFC | Title | Sprint | Started |
|-----|-------|--------|---------|
| RFC-0002 | Feature W | Sprint 18 | 2026-01-22 |

## Implemented (1)

| RFC | Title | Completed | Release |
|-----|-------|-----------|---------|
| RFC-0001 | Initial Feature | 2026-01-10 | v5.0.0 |

## Rejected (0)

(none)

## Stale (0)

(none)

---
Total: 10 RFCs | 2 Approved | 1 Implementing
```

## Edge Cases

- **No RFC-Index**: Display message "No RFCs yet. Create one with /rfc-create"
- **Empty sections**: Show "(none)" for empty status categories
- **Filter applied**: Only show matching section, still show total counts
