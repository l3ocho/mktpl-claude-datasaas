# pr-review

Multi-agent pull request review with confidence scoring and actionable feedback.

## Overview

pr-review conducts comprehensive code reviews using specialized agents for security, performance, maintainability, and test coverage. Each finding includes a confidence score to reduce noise and focus on real issues.

## Commands

| Command | Description |
|---------|-------------|
| `/pr-review <pr#>` | Full multi-agent review |
| `/pr-summary <pr#>` | Quick summary without full review |
| `/pr-findings <pr#>` | Filter findings by category/confidence |
| `/pr-diff <pr#>` | View diff with inline comment annotations |
| `/initial-setup` | Full interactive setup wizard |
| `/project-init` | Quick project setup (system already configured) |
| `/project-sync` | Sync configuration with current git remote |

## Review Agents

| Agent | Focus |
|-------|-------|
| **Security Reviewer** | Injections, auth, data exposure, crypto |
| **Performance Analyst** | N+1 queries, complexity, memory, caching |
| **Maintainability Auditor** | Complexity, duplication, naming, coupling |
| **Test Validator** | Coverage, test quality, flaky tests |

## Confidence Scoring

Findings are scored 0.0 - 1.0:

| Range | Label | Action |
|-------|-------|--------|
| 0.9 - 1.0 | HIGH | Must address |
| 0.7 - 0.89 | MEDIUM | Should address |
| 0.5 - 0.69 | LOW | Consider addressing |
| < 0.5 | (suppressed) | Not reported |

## Installation

Add to your project's `.claude/settings.json`:

```json
{
  "plugins": ["pr-review"]
}
```

Requires Gitea MCP server configuration.

## Configuration

Environment variables can be set in your project's `.env` file or shell environment.

| Variable | Default | Description |
|----------|---------|-------------|
| `PR_REVIEW_CONFIDENCE_THRESHOLD` | `0.7` | Minimum confidence score (0.0-1.0) for reporting findings. Findings below this threshold are filtered out to reduce noise. |
| `PR_REVIEW_AUTO_SUBMIT` | `false` | Automatically submit review to Gitea without confirmation prompt |

### Example Configuration

```bash
# Project .env file

# Only show high-confidence findings (MEDIUM and HIGH)
PR_REVIEW_CONFIDENCE_THRESHOLD=0.7

# Auto-submit review to Gitea (default: false)
PR_REVIEW_AUTO_SUBMIT=false
```

### Confidence Threshold Details

The confidence threshold filters which findings appear in review output:

| Threshold | Effect |
|-----------|--------|
| `0.9` | Only definite issues (HIGH confidence) |
| `0.7` | Likely issues and above (MEDIUM+HIGH) - **recommended** |
| `0.5` | Include possible concerns (LOW+MEDIUM+HIGH) |
| `0.3` | Include speculative findings |

Lower thresholds show more findings but may include false positives. Higher thresholds reduce noise but may miss some valid concerns.

## Usage Examples

### Full Review

```
/pr-review 123

═══════════════════════════════════════════════════
PR Review Report: #123
═══════════════════════════════════════════════════

Summary:
  Files changed: 12
  Lines: +234 / -45

Findings: 8 total
  🔴 Critical: 1
  🟠 Major: 2
  🟡 Minor: 3
  💡 Suggestions: 2

[Detailed findings...]

VERDICT: REQUEST_CHANGES
═══════════════════════════════════════════════════
```

### Filter Findings

```
/pr-findings 123 --category security

# Shows only security-related findings
```

### Quick Summary

```
/pr-summary 123

# Shows change overview without full analysis
```

## Output

Review reports include:
- Summary statistics
- Findings grouped by severity
- Code snippets with context
- Suggested fixes
- Overall verdict (APPROVE/COMMENT/REQUEST_CHANGES)

## Verdict Logic

| Condition | Verdict |
|-----------|---------|
| Any critical finding | REQUEST_CHANGES |
| 2+ major findings | REQUEST_CHANGES |
| Only minor/suggestions | COMMENT |
| No significant findings | APPROVE |

## Integration

For CLAUDE.md integration instructions, see `claude-md-integration.md`.

## License

MIT
