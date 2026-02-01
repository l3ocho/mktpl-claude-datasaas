---
description: Create a new RFC (Request for Comments) from conversation or clarified specification
agent: planner
---

# Create RFC

## Skills Required

- skills/mcp-tools-reference.md
- skills/rfc-workflow.md
- skills/rfc-templates.md

## Purpose

Create a new RFC wiki page to track a feature idea, proposal, or enhancement through the review lifecycle. RFCs provide a structured way to document, discuss, and approve changes before implementation.

## Invocation

Run `/rfc-create` with optional context:
- After `/clarify` to convert clarified spec to RFC
- With description of feature idea
- From conversation context

## Workflow

1. **Gather Input**
   - Check if conversation has clarified specification (from `/clarify`)
   - If no context: prompt for Summary, Motivation, and initial Design
   - Extract author from context or prompt

2. **Allocate RFC Number**
   - Call `allocate_rfc_number` MCP tool
   - Get next sequential 4-digit number

3. **Create RFC Page**
   - Use template from `skills/rfc-templates.md`
   - Fill in frontmatter (number, title, status=Draft, author, dates)
   - Populate Summary, Motivation, Detailed Design sections
   - Create wiki page: `RFC-NNNN: Title`

4. **Update RFC-Index**
   - Fetch RFC-Index (create if doesn't exist)
   - Add entry to "## Draft" section
   - Update wiki page

5. **Confirm Creation**
   - Display RFC number and wiki link
   - Remind about next steps (refine → `/rfc-review`)

## Visual Output

```
+----------------------------------------------------------------------+
|  PROJMAN - RFC Creation                                              |
+----------------------------------------------------------------------+

RFC-0001: [Title] created successfully!

Status: Draft
Wiki: [link to RFC page]

Next steps:
- Refine the RFC with additional details
- When ready: /rfc-review 0001 to submit for review
```

## Input Mapping

When converting from `/clarify` output:

| Clarify Section | RFC Section |
|-----------------|-------------|
| Problem/Context | Motivation > Problem Statement |
| Goals/Outcomes | Motivation > Goals |
| Scope/Requirements | Detailed Design > Overview |
| Constraints | Non-Goals or Detailed Design |
| Success Criteria | Testing Strategy |

## Edge Cases

- **No RFC-Index exists**: Create it with empty sections
- **User provides minimal input**: Create minimal RFC template, note sections to fill
- **Duplicate title**: Proceed (RFC numbers are unique, titles don't need to be)
