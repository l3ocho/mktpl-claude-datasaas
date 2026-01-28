# clarity-assist

Prompt optimization and requirement clarification plugin with neurodivergent-friendly accommodations.

## Overview

clarity-assist helps transform vague, incomplete, or ambiguous requests into clear, actionable specifications. It uses a structured 4-D methodology (Deconstruct, Diagnose, Develop, Deliver) and ND-friendly communication patterns.

## Commands

| Command | Description |
|---------|-------------|
| `/clarify` | Full 4-D prompt optimization for complex requests |
| `/quick-clarify` | Rapid single-pass clarification for simple requests |

## Features

### 4-D Methodology

1. **Deconstruct** - Break down the request into components
2. **Diagnose** - Analyze gaps and potential issues
3. **Develop** - Gather clarifications through structured questions
4. **Deliver** - Produce refined specification

### ND-Friendly Design

- **Option-based questioning** - Always provide 2-4 concrete choices
- **Chunked questions** - Ask 1-2 questions at a time
- **Context for questions** - Explain why you're asking
- **Conflict detection** - Check previous answers before new questions
- **Progress acknowledgment** - Summarize frequently

### Escalation Protocol

When requests are complex or users seem overwhelmed:
- Acknowledge complexity
- Offer to focus on one aspect at a time
- Build incrementally

## Installation

Add to your project's `.claude/settings.json`:

```json
{
  "plugins": ["clarity-assist"]
}
```

## Usage

### Full Clarification

```
/clarify

[Your vague or complex request here]
```

### Quick Clarification

```
/quick-clarify

[Your mostly-clear request here]
```

## Configuration

No configuration required. The plugin uses sensible defaults.

## Output Format

After clarification, you receive a structured specification:

```markdown
## Clarified Request

### Summary
[Description of what will be built]

### Scope
**In Scope:** [items]
**Out of Scope:** [items]

### Requirements
[Prioritized table]

### Assumptions
[List of assumptions]
```

## Documentation

- [Neurodivergent Support Guide](docs/ND-SUPPORT.md) - How clarity-assist supports ND users with executive function challenges and cognitive differences

## Integration

For CLAUDE.md integration instructions, see `claude-md-integration.md`.

## License

MIT
