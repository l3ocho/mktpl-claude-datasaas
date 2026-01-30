# Multi-Agent Review Workflow

## Overview

PR reviews use specialized agents that analyze different aspects of code changes. The coordinator dispatches to relevant agents and aggregates findings.

## Agent Roles

| Agent | Focus Area | File Patterns |
|-------|------------|---------------|
| **Security Reviewer** | Vulnerabilities, auth, injection | `*.ts`, `*.js`, `*.sql`, `*.py` |
| **Performance Analyst** | N+1, inefficient algorithms, memory | `*.ts`, `*.js`, `*.py`, `*.go` |
| **Maintainability Auditor** | Complexity, readability, DRY | All code files |
| **Test Validator** | Coverage, edge cases, assertions | `*.test.*`, `*_test.*`, `*_spec.*` |

## Dispatch Logic

1. **Analyze changed files** - Identify file types and patterns
2. **Select agents** - Match files to relevant agents
3. **Parallel dispatch** - Send review tasks to agents
4. **Collect findings** - Aggregate results from all agents
5. **Filter by confidence** - Apply threshold (default: 0.7)
6. **Generate report** - Structure findings by severity

### Skip Patterns

Don't dispatch agents for:
- `*.md`, `*.txt` - Documentation only
- `*.json` (config) - Unless security-sensitive
- Generated files - `*.min.js`, `*.d.ts`, etc.

## Finding Structure

Each finding includes:

```
{
  id: "SEC-001",
  category: "security" | "performance" | "maintainability" | "tests",
  severity: "critical" | "major" | "minor" | "suggestion",
  confidence: 0.0 - 1.0,
  file: "src/api/users.ts",
  line: 45,
  title: "SQL Injection Vulnerability",
  description: "Detailed explanation...",
  fix: "Suggested code fix..." (optional)
}
```

## Verdict Logic

| Condition | Verdict |
|-----------|---------|
| Any critical finding | REQUEST_CHANGES |
| 2+ major findings | REQUEST_CHANGES |
| Only minor/suggestions | COMMENT |
| No significant findings | APPROVE |

## Confidence Thresholds

Reference: `skills/review-patterns/confidence-scoring.md`

| Range | Label | Action |
|-------|-------|--------|
| 0.9 - 1.0 | HIGH | Must address |
| 0.7 - 0.89 | MEDIUM | Should address |
| 0.5 - 0.69 | LOW | Consider addressing |
| < threshold | Filtered | Not shown |

Default threshold: 0.7 (MEDIUM and above)

## Aggregation Rules

When multiple agents find the same issue:
1. Keep highest confidence score
2. Merge descriptions
3. Use most severe category
4. Deduplicate fixes
