---
description: RFC lifecycle management - create, list, review, approve, reject
agent: planner
---

# RFC Management

## Skills Required

- skills/mcp-tools-reference.md
- skills/rfc-workflow.md
- skills/rfc-templates.md

## Purpose

Manage the full RFC lifecycle through sub-commands. RFCs provide a structured way to document, discuss, and approve changes before implementation.

## Invocation

```
/rfc <sub-command> [arguments]
```

### Sub-Commands

| Sub-Command | Usage | Description |
|-------------|-------|-------------|
| `create` | `/rfc create` | Create new RFC from conversation or clarified spec |
| `list` | `/rfc list [filter]` | List all RFCs grouped by status |
| `review` | `/rfc review <number>` | Submit Draft RFC for review |
| `approve` | `/rfc approve <number>` | Approve RFC in Review status |
| `reject` | `/rfc reject <number>` | Reject RFC with documented reason |

---

## Sub-Command: create

Create a new RFC wiki page to track a feature idea through the review lifecycle.

**Workflow:**
1. Check if conversation has clarified specification (from `/clarify`)
2. If no context: prompt for Summary, Motivation, and initial Design
3. Call `allocate_rfc_number` MCP tool for next sequential number
4. Create RFC page using template from `skills/rfc-templates.md`
5. Update RFC-Index wiki page (create if doesn't exist)
6. Display RFC number, wiki link, and next steps

**Input Mapping (from /clarify):**

| Clarify Section | RFC Section |
|-----------------|-------------|
| Problem/Context | Motivation > Problem Statement |
| Goals/Outcomes | Motivation > Goals |
| Scope/Requirements | Detailed Design > Overview |
| Constraints | Non-Goals or Detailed Design |
| Success Criteria | Testing Strategy |

**Edge cases:**
- No RFC-Index exists: Create it with empty sections
- User provides minimal input: Create minimal RFC template, note sections to fill
- Duplicate title: Proceed (RFC numbers are unique, titles don't need to be)

---

## Sub-Command: list

Display all RFCs grouped by lifecycle status.

**Filters:** `/rfc list approved`, `/rfc list draft`, `/rfc list review`

**Workflow:**
1. Fetch RFC-Index wiki page via `get_wiki_page`
2. Parse tables from each status section
3. Display grouped by status, highlight Approved section
4. Show counts per status

**Edge cases:**
- No RFC-Index: "No RFCs yet. Create one with `/rfc create`"
- Empty sections: Show "(none)"

---

## Sub-Command: review

Submit a Draft RFC for review, transitioning status to Review.

**Usage:** `/rfc review <number>` (leading zeros optional)

**Workflow:**
1. Validate RFC number, fetch page
2. Check status is Draft - STOP if not
3. Validate minimum content (Summary, Motivation, Detailed Design > Overview required)
4. Optionally assign champion
5. Update RFC page: status Draft -> Review, update date
6. Update RFC-Index: move from Draft to In Review section

---

## Sub-Command: approve

Approve an RFC in Review status for sprint planning.

**Usage:** `/rfc approve <number>` (leading zeros optional)

**Workflow:**
1. Validate RFC number, fetch page
2. Check status is Review - STOP if not
3. Gather approval rationale (required)
4. Update RFC page: status Review -> Approved, add Decision section
5. Update RFC-Index: move from In Review to Approved section

---

## Sub-Command: reject

Reject an RFC with documented reason.

**Usage:** `/rfc reject <number>` (leading zeros optional)

**Workflow:**
1. Validate RFC number, fetch page
2. Check status is Draft or Review - STOP if not
3. Require rejection reason (mandatory)
4. Update RFC page: status -> Rejected, add Decision section
5. Update RFC-Index: move to Rejected section

---

## Visual Output

```
+----------------------------------------------------------------------+
|  PROJMAN - RFC [Sub-Command]                                         |
+----------------------------------------------------------------------+
```

---

## Validation Errors (All Sub-Commands)

- **RFC not found**: "RFC-NNNN not found. Check the number with `/rfc list`"
- **Wrong status**: "RFC-NNNN is in [status] status. [Specific allowed statuses for this action]."
- **Missing required input**: Specific message per sub-command
- **No sub-command provided**: Display sub-command reference table
