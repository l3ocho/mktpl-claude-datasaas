---
description: Submit a Draft RFC for review, transitioning status to Review
agent: planner
---

# Submit RFC for Review

## Skills Required

- skills/mcp-tools-reference.md
- skills/rfc-workflow.md
- skills/rfc-templates.md

## Purpose

Transition an RFC from Draft to Review status, indicating it's ready for maintainer evaluation. Optionally assign a champion to shepherd the RFC through review.

## Invocation

Run `/rfc-review <number>` where number is the RFC number:
- `/rfc-review 0001`
- `/rfc-review 1` (leading zeros optional)

## Workflow

1. **Validate RFC Number**
   - Normalize input (add leading zeros if needed)
   - Fetch RFC page: `RFC-NNNN: *`

2. **Check Current Status**
   - Parse frontmatter to get current status
   - **STOP** if status is not "Draft"
   - Error: "RFC-NNNN is in [status] status. Only Draft RFCs can be submitted for review."

3. **Validate Minimum Content**
   - Check for Summary section (required)
   - Check for Motivation section (required)
   - Check for Detailed Design > Overview (required)
   - Warn if Alternatives Considered is empty

4. **Optional: Assign Champion**
   - Ask: "Would you like to assign a champion? (Enter username or skip)"
   - Champion is responsible for driving the RFC through review

5. **Update RFC Page**
   - Change status: Draft → Review
   - Update "Updated" date
   - Set Champion if provided
   - Add Review Notes section if not present

6. **Update RFC-Index**
   - Remove entry from "## Draft" section
   - Add entry to "## In Review" section

7. **Confirm Transition**
   - Display updated status
   - Note next steps (review discussion, then /rfc-approve or /rfc-reject)

## Visual Output

```
+----------------------------------------------------------------------+
|  PROJMAN - RFC Review Submission                                     |
+----------------------------------------------------------------------+

RFC-0005: Feature Idea submitted for review

Status: Draft → Review
Champion: @assigned_user (or: unassigned)
Updated: RFC-Index

Next steps:
- Discuss in RFC wiki page comments or meetings
- When decision reached: /rfc-approve 0005 or /rfc-reject 0005
```

## Validation Errors

- **RFC not found**: "RFC-NNNN not found. Check the number with /rfc-list"
- **Wrong status**: "RFC-NNNN is [status]. Only Draft RFCs can be reviewed."
- **Missing sections**: "RFC-NNNN is missing required sections: [list]. Please complete before review."
