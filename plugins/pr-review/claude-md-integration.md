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
| `/pr-diff <pr#>` | View diff with inline comments |

### Review Categories

Reviews analyze:
- **Security**: Injections, auth issues, data exposure
- **Performance**: N+1 queries, complexity, memory
- **Maintainability**: Code quality, duplication, naming
- **Tests**: Coverage gaps, test quality

### Confidence Threshold

Configure via `PR_REVIEW_CONFIDENCE_THRESHOLD` (default: 0.7).

| Range | Label | Action |
|-------|-------|--------|
| 0.9 - 1.0 | HIGH | Must address |
| 0.7 - 0.89 | MEDIUM | Should address |
| 0.5 - 0.69 | LOW | Consider addressing |
| < threshold | (filtered) | Not reported |

With default threshold of 0.7, only MEDIUM and HIGH findings are shown.

### Verdict Rules

| Condition | Verdict |
|-----------|---------|
| Critical findings | REQUEST_CHANGES |
| 2+ Major findings | REQUEST_CHANGES |
| Minor only | COMMENT |
| No issues | APPROVE |

---

Copy the section between the horizontal rules into your CLAUDE.md.
