# Neurodivergent-Friendly Accommodations

Guidelines for making clarification interactions accessible and comfortable for neurodivergent users.

## Core Principles

### Reduce Cognitive Load
- Maximum 4 options per question
- Always include "Other" escape hatch
- Provide examples, not just descriptions
- Use numbered lists for easy reference

### Support Working Memory
- Summarize frequently
- Reference earlier decisions explicitly
- Do not assume user remembers context from many turns ago
- Echo back understanding before proceeding

### Allow Processing Time
- Do not rapid-fire questions
- Validate answers before moving on
- Offer to revisit or change earlier answers
- One question block at a time

### Manage Overwhelm
- Offer to break into smaller sessions
- Prioritize must-haves vs nice-to-haves
- Provide "good enough for now" options
- Acknowledge complexity openly

## Question Formatting Rules

**Always do:**
```
**How should errors be handled?**
1. Silent logging (user sees nothing)
2. Toast notifications (brief, dismissible)
3. Modal dialogs (requires user action)
4. Other

[Context: This affects both UX and error-handling complexity]
```

**Never do:**
```
How do you want to handle errors? There are many approaches...
```

## Conflict Acknowledgment

Before asking about something that might conflict with a previous answer:

```
[Internal check]
Previous: User said "keep it simple"
Current question about: Adding configuration options
Potential conflict: More options = more complexity
```

Then acknowledge: "Earlier you mentioned keeping it simple. With that in mind..."

## Escalation for Overwhelm

If the request is particularly complex or user seems overwhelmed:

1. Acknowledge the complexity openly
2. Offer to start with just ONE aspect
3. Build incrementally

```
"This touches a lot of areas. Rather than tackle everything at once,
let's start with [most critical piece]. Once that's clear, we can
add the other parts. Sound good?"
```
