# Clarification Techniques

Structured approaches for disambiguating user requests.

## Anti-Patterns to Detect

### Vague Requests
**Triggers:** "improve", "fix", "update", "change", "better", "faster", "cleaner"

**Response:** Ask for specific metrics or outcomes

### Scope Creep Signals
**Triggers:** "while you're at it", "also", "might as well", "and another thing"

**Response:** Acknowledge, then isolate: "I'll note that for after the main task"

### Assumption Gaps
**Triggers:** References to "the" thing (which thing?), "it" (what?), "there" (where?)

**Response:** Echo back specific understanding

### Conflicting Requirements
**Triggers:** "Simple but comprehensive", "Fast but thorough", "Minimal but complete"

**Response:** Prioritize: "Which matters more: simplicity or completeness?"

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

## Echo Understanding Technique

Before diving into questions, restate understanding:

```
"I understand you want [X] that does [Y]."
```

This validates comprehension and gives user a chance to correct early.

## Micro-Summary Technique

For quick confirmations before proceeding:

```
"Quick summary before I start:
- [Key point 1]
- [Key point 2]
- [Assumption made]

Proceed? (Or clarify anything)"
```
