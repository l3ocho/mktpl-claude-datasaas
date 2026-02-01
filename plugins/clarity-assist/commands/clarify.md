# /clarify - Full Prompt Optimization

## Visual Output

```
+----------------------------------------------------------------------+
|  CLARITY-ASSIST - Prompt Optimization                                |
+----------------------------------------------------------------------+
```

## Purpose

Transform vague, incomplete, or ambiguous requests into clear, actionable specifications using the 4-D methodology with neurodivergent-friendly accommodations.

## When to Use

- Complex multi-step requests
- Requirements with multiple possible interpretations
- Tasks requiring significant context gathering
- When user seems uncertain about what they want

## Skills to Load

Load these skills before proceeding:

- `skills/4d-methodology.md` - Core 4-phase process
- `skills/nd-accommodations.md` - ND-friendly question patterns
- `skills/clarification-techniques.md` - Anti-patterns and templates
- `skills/escalation-patterns.md` - When to adjust approach

## Workflow

1. **Deconstruct** - Break down request into components
2. **Diagnose** - Identify gaps and conflicts
3. **Develop** - Gather clarifications via structured questions
4. **Deliver** - Present refined specification
5. **Offer RFC Creation** - For feature work, offer to save as RFC

## Output Format

Use the Deliver phase template from `skills/4d-methodology.md` to present the clarified specification for user confirmation.

## RFC Creation Offer (Step 5)

After presenting the clarified specification, if the request appears to be a feature or enhancement:

```
---

Would you like to save this as an RFC for formal tracking?

An RFC (Request for Comments) provides:
- Structured documentation of the proposal
- Review workflow before implementation
- Integration with sprint planning

[1] Yes, create RFC from this specification
[2] No, proceed with implementation directly
```

If user selects [1]:
- Pass clarified specification to `/rfc-create`
- The Summary, Motivation, and Design sections will be populated from the clarified spec
- User can then refine the RFC and submit for review
