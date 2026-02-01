---
description: Approve an RFC in Review status, making it ready for sprint planning
agent: planner
---

# Approve RFC

## Skills Required

- skills/mcp-tools-reference.md
- skills/rfc-workflow.md
- skills/rfc-templates.md

## Purpose

Transition an RFC from Review to Approved status, indicating the proposal has been accepted and is ready for implementation in an upcoming sprint.

## Invocation

Run `/rfc-approve <number>` where number is the RFC number:
- `/rfc-approve 0003`
- `/rfc-approve 3` (leading zeros optional)

## Workflow

1. **Validate RFC Number**
   - Normalize input (add leading zeros if needed)
   - Fetch RFC page: `RFC-NNNN: *`

2. **Check Current Status**
   - Parse frontmatter to get current status
   - **STOP** if status is not "Review"
   - Error: "RFC-NNNN is in [status] status. Only RFCs in Review can be approved."

3. **Gather Decision Details**
   - Prompt: "Please provide the approval rationale (why is this RFC being approved?):"
   - This becomes the Decision section content

4. **Update RFC Page**
   - Change status: Review → Approved
   - Update "Updated" date
   - Add/update Decision section:
     ```markdown
     ## Decision

     **Decision:** Approved
     **Date:** YYYY-MM-DD
     **Decided By:** @[current user or maintainer]

     **Rationale:**

     [User-provided rationale]
     ```

5. **Update RFC-Index**
   - Remove entry from "## In Review" section
   - Add entry to "## Approved" section

6. **Confirm Approval**
   - Display updated status
   - Note that RFC is now available for `/sprint-plan`

## Visual Output

```
+----------------------------------------------------------------------+
|  PROJMAN - RFC Approval                                              |
+----------------------------------------------------------------------+

RFC-0003: Feature X has been approved!

Status: Review → Approved
Decision recorded in RFC page.

This RFC is now available for sprint planning.
Use /sprint-plan and select this RFC when prompted.
```

## Validation Errors

- **RFC not found**: "RFC-NNNN not found. Check the number with /rfc-list"
- **Wrong status**: "RFC-NNNN is [status]. Only RFCs in Review can be approved."
- **No rationale provided**: "Approval rationale is required. Please explain why this RFC is being approved."
