---
description: Reject an RFC with documented reason, marking it as declined
agent: planner
---

# Reject RFC

## Skills Required

- skills/mcp-tools-reference.md
- skills/rfc-workflow.md
- skills/rfc-templates.md

## Purpose

Transition an RFC to Rejected status with a documented reason. Rejected RFCs remain in the wiki for historical reference but are marked as declined.

## Invocation

Run `/rfc-reject <number>` where number is the RFC number:
- `/rfc-reject 0006`
- `/rfc-reject 6` (leading zeros optional)

## Workflow

1. **Validate RFC Number**
   - Normalize input (add leading zeros if needed)
   - Fetch RFC page: `RFC-NNNN: *`

2. **Check Current Status**
   - Parse frontmatter to get current status
   - **STOP** if status is not "Draft" or "Review"
   - Error: "RFC-NNNN is in [status] status. Only Draft or Review RFCs can be rejected."

3. **Require Rejection Reason**
   - Prompt: "Please provide the rejection reason (required):"
   - **STOP** if no reason provided
   - Error: "Rejection reason is required to document why this RFC was declined."

4. **Update RFC Page**
   - Change status: [current] → Rejected
   - Update "Updated" date
   - Add/update Decision section:
     ```markdown
     ## Decision

     **Decision:** Rejected
     **Date:** YYYY-MM-DD
     **Decided By:** @[current user or maintainer]

     **Reason:**

     [User-provided rejection reason]
     ```

5. **Update RFC-Index**
   - Remove entry from current section ("## Draft" or "## In Review")
   - Add entry to "## Rejected" section with reason summary

6. **Confirm Rejection**
   - Display updated status
   - Note that RFC remains in wiki for reference

## Visual Output

```
+----------------------------------------------------------------------+
|  PROJMAN - RFC Rejection                                             |
+----------------------------------------------------------------------+

RFC-0006: Proposed Feature has been rejected.

Status: Review → Rejected
Reason: Out of scope for current project direction

The RFC remains in the wiki for historical reference.
If circumstances change, a new RFC can be created.
```

## Validation Errors

- **RFC not found**: "RFC-NNNN not found. Check the number with /rfc-list"
- **Wrong status**: "RFC-NNNN is [status]. Only Draft or Review RFCs can be rejected."
- **No reason provided**: "Rejection reason is required. Please document why this RFC is being declined."

## Notes

- Rejected is a terminal state
- To reconsider, create a new RFC that references the rejected one
- Rejection reasons help future contributors understand project direction
