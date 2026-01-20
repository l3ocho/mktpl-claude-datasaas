# /clarify - Full Prompt Optimization

## Purpose

Transform vague, incomplete, or ambiguous requests into clear, actionable specifications using the 4-D methodology with neurodivergent-friendly accommodations.

## When to Use

- Complex multi-step requests
- Requirements with multiple possible interpretations
- Tasks requiring significant context gathering
- When user seems uncertain about what they want

## 4-D Methodology

### Phase 1: Deconstruct

Break down the user's request into components:

1. **Extract explicit requirements** - What was directly stated
2. **Identify implicit assumptions** - What seems assumed but not stated
3. **Note ambiguities** - Points that could go multiple ways
4. **List dependencies** - External factors that might affect implementation

### Phase 2: Diagnose

Analyze gaps and potential issues:

1. **Missing information** - What do we need to know?
2. **Conflicting requirements** - Do any stated goals contradict?
3. **Scope boundaries** - What's in/out of scope?
4. **Technical constraints** - Platform, language, architecture limits

### Phase 3: Develop

Gather clarifications through structured questioning:

**ND-Friendly Question Rules:**
- Present 2-4 concrete options (never open-ended alone)
- Include "Other" for custom responses
- Ask 1-2 questions at a time maximum
- Provide brief context for why you're asking
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

### Phase 4: Deliver

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

## Conflict Detection

Before each question, review previous answers for conflicts:

```
[Internal check]
Previous: User said "keep it simple"
Current question about: Adding configuration options
Potential conflict: More options = more complexity
→ Acknowledge: "Earlier you mentioned keeping it simple. With that in mind..."
```

## Escalation Protocol

If the request is particularly messy or the user seems overwhelmed:

1. Acknowledge the complexity
2. Offer to start with just ONE aspect
3. Build incrementally

```
"This touches a lot of areas. Rather than tackle everything at once,
let's start with [most critical piece]. Once that's clear, we can
add the other parts. Sound good?"
```

## Example Interaction

**User:** Make the app faster

**Clarify Response:**

```
Let me help clarify what kind of performance improvements you're looking for.

**What type of slowness are you experiencing?**
1. Initial page load takes too long
2. Interactions feel sluggish (clicking, typing)
3. API calls are slow
4. All of the above
5. Other

[I'm asking because each has very different solutions]
```

## Output Format

After gathering all necessary information, use the Deliver phase format to present the clarified specification for user confirmation.
