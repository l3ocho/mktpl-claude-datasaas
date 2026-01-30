# 4-D Methodology for Prompt Clarification

The 4-D methodology transforms vague requests into actionable specifications.

## Phase 1: Deconstruct

Break down the user's request into components:

1. **Extract explicit requirements** - What was directly stated
2. **Identify implicit assumptions** - What seems assumed but not stated
3. **Note ambiguities** - Points that could go multiple ways
4. **List dependencies** - External factors that might affect implementation

## Phase 2: Diagnose

Analyze gaps and potential issues:

1. **Missing information** - What do we need to know?
2. **Conflicting requirements** - Do any stated goals contradict?
3. **Scope boundaries** - What is in/out of scope?
4. **Technical constraints** - Platform, language, architecture limits

## Phase 3: Develop

Gather clarifications through structured questioning:

- Present 2-4 concrete options (never open-ended alone)
- Include "Other" for custom responses
- Ask 1-2 questions at a time maximum
- Provide brief context for why you are asking
- Check for conflicts with previous answers

**Example Format:**
```
To help me understand the scope better:

**How should errors be handled?**
1. Silent logging (user sees nothing)
2. Toast notifications (brief, dismissible)
3. Modal dialogs (requires user action)
4. Other

[Context: This affects both UX and how much error-handling code we need]
```

## Phase 4: Deliver

Produce the refined specification:

```markdown
## Clarified Request

### Summary
[1-2 sentence description of what will be built]

### Scope
**In Scope:**
- [Item 1]
- [Item 2]

**Out of Scope:**
- [Item 1]

### Requirements

| # | Requirement | Priority | Notes |
|---|-------------|----------|-------|
| 1 | ... | Must | ... |
| 2 | ... | Should | ... |

### Assumptions
- [Assumption made based on conversation]

### Open Questions
- [Any remaining ambiguities, if any]
```
