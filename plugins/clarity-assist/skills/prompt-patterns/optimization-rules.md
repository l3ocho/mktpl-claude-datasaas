# Prompt Optimization Rules

## Core Rules

### Rule 1: Specificity Over Generality

| Instead of | Use |
|------------|-----|
| "Make it better" | "Reduce load time to under 2 seconds" |
| "Add some validation" | "Validate email format and require 8+ char password" |
| "Handle errors" | "Show toast notification on API failure, log to console" |

### Rule 2: Include Context

Every good prompt includes:
- **What**: The action/feature/fix needed
- **Where**: Location in codebase or UI
- **Why**: Purpose or problem being solved
- **Constraints**: Technical limits, compatibility, standards

### Rule 3: Define Success

Specify how to know when the task is done:
- Acceptance criteria
- Test cases to pass
- Behavior to verify

### Rule 4: Scope Boundaries

Explicitly state:
- What IS in scope
- What is NOT in scope
- What MIGHT be in scope (user's call)

## Anti-Patterns to Detect

### Vague Requests

Triggers: "improve", "fix", "update", "change", "better", "faster", "cleaner"

Response: Ask for specific metrics or outcomes

### Scope Creep Signals

Triggers: "while you're at it", "also", "might as well", "and another thing"

Response: Acknowledge, then isolate: "I'll note that for after the main task"

### Assumption Gaps

Triggers: References to "the" thing (which thing?), "it" (what's it?), "there" (where?)

Response: Echo back specific understanding

### Conflicting Requirements

Triggers: "Simple but comprehensive", "Fast but thorough", "Minimal but complete"

Response: Prioritize: "Which matters more: simplicity or completeness?"

## Question Templates

### For Unclear Purpose

```
**What problem does this solve?**
1. [Specific problem A]
2. [Specific problem B]
3. Combination
4. Different problem: ____
```

### For Missing Scope

```
**What should this include?**
- [ ] Feature A
- [ ] Feature B
- [ ] Feature C
- [ ] Other: ____
```

### For Ambiguous Behavior

```
**When [trigger event], what should happen?**
1. [Behavior option A]
2. [Behavior option B]
3. Nothing (ignore)
4. Depends on: ____
```

### For Technical Decisions

```
**Implementation approach:**
1. [Approach A] - pros: X, cons: Y
2. [Approach B] - pros: X, cons: Y
3. Let me decide based on codebase
4. Need more info about: ____
```

## Optimization Checklist

Before proceeding with any task, verify:

- [ ] **Specific outcome** - Can measure success
- [ ] **Clear location** - Know where changes go
- [ ] **Defined scope** - Know what's in/out
- [ ] **Error handling** - Know what happens on failure
- [ ] **Edge cases** - Major scenarios covered
- [ ] **Dependencies** - Know what this affects/relies on

## ND-Friendly Adaptations

### Reduce Cognitive Load
- Maximum 4 options per question
- Always include "Other" escape hatch
- Provide examples, not just descriptions

### Support Working Memory
- Summarize frequently
- Reference earlier decisions explicitly
- Don't assume user remembers context

### Allow Processing Time
- Don't rapid-fire questions
- Validate answers before moving on
- Offer to revisit/change earlier answers

### Manage Overwhelm
- Offer to break into smaller sessions
- Prioritize must-haves vs nice-to-haves
- Provide "good enough for now" options
