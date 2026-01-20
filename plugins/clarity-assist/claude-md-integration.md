# clarity-assist - CLAUDE.md Integration

Add the following section to your project's CLAUDE.md file to enable clarity-assist.

---

## Prompt Clarification

This project uses the clarity-assist plugin for requirement gathering.

### When to Use

- Complex or vague requests
- Multi-step implementations
- When requirements seem incomplete

### Commands

| Command | Use Case |
|---------|----------|
| `/clarify` | Full 4-D methodology for complex requests |
| `/quick-clarify` | Rapid mode for simple disambiguation |

### Communication Style

When gathering requirements:
- Present 2-4 concrete options (never open-ended alone)
- Ask 1-2 questions at a time
- Explain why you're asking each question
- Check for conflicts with previous answers
- Summarize progress frequently

### Output Format

After clarification, produce a structured specification:

```markdown
## Clarified Request

### Summary
[1-2 sentence description]

### Scope
**In Scope:** [items]
**Out of Scope:** [items]

### Requirements
| # | Requirement | Priority | Notes |
|---|-------------|----------|-------|
| 1 | ... | Must | ... |

### Assumptions
[List made during conversation]
```

---

Copy the section between the horizontal rules into your CLAUDE.md.
