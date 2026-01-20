# pr-review - CLAUDE.md Integration

Add the following section to your project's CLAUDE.md file to enable pr-review.

---

## Pull Request Review

This project uses the pr-review plugin for automated code review.

### Commands

| Command | Use Case |
|---------|----------|
| `/pr-review <pr#>` | Full multi-agent review |
| `/pr-summary <pr#>` | Quick change summary |
| `/pr-findings <pr#>` | Filter review findings |

### Review Categories

Reviews analyze:
- **Security**: Injections, auth issues, data exposure
- **Performance**: N+1 queries, complexity, memory
- **Maintainability**: Code quality, duplication, naming
- **Tests**: Coverage gaps, test quality

### Confidence Threshold

Findings below 0.5 confidence are suppressed.

- HIGH (0.9+): Definite issue
- MEDIUM (0.7-0.89): Likely issue
- LOW (0.5-0.69): Possible concern

### Verdict Rules

| Condition | Verdict |
|-----------|---------|
| Critical findings | REQUEST_CHANGES |
| 2+ Major findings | REQUEST_CHANGES |
| Minor only | COMMENT |
| No issues | APPROVE |

---

Copy the section between the horizontal rules into your CLAUDE.md.
