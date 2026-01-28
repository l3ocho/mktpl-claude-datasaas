# /pr-review - Full Multi-Agent Review

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 PR-REVIEW · Full Review                                       │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the review.

## Purpose

Conduct a comprehensive pull request review using specialized agents for security, performance, maintainability, and test coverage.

## Usage

```
/pr-review <pr-number> [--repo owner/repo]
```

## Behavior

### Step 1: Fetch PR Data

Using Gitea MCP tools:
1. `get_pull_request` - PR metadata
2. `get_pr_diff` - Code changes
3. `get_pr_comments` - Existing discussion

### Step 2: Dispatch to Agents

The coordinator dispatches review tasks to specialized agents:

```
PR Review: #123 - Add user authentication
═══════════════════════════════════════════════════

Dispatching to review agents:
├─ Security Reviewer     → analyzing...
├─ Performance Analyst   → analyzing...
├─ Maintainability Auditor → analyzing...
└─ Test Validator        → analyzing...
```

### Step 3: Aggregate Findings

Collect findings from all agents, each with:
- Category (security, performance, maintainability, tests)
- Severity (critical, major, minor, suggestion)
- Confidence score (0.0 - 1.0)
- File and line reference
- Description
- Suggested fix (if applicable)

### Step 4: Filter by Confidence

Filter findings based on `PR_REVIEW_CONFIDENCE_THRESHOLD` (default: 0.7):

| Confidence | Label | Description |
|------------|-------|-------------|
| 0.9 - 1.0 | HIGH | Definite issue, must address |
| 0.7 - 0.89 | MEDIUM | Likely issue, should address |
| 0.5 - 0.69 | LOW | Possible concern, consider addressing |
| < threshold | (filtered) | Below configured threshold |

**Note:** With the default threshold of 0.7, only MEDIUM and HIGH confidence findings are shown. Adjust `PR_REVIEW_CONFIDENCE_THRESHOLD` to include more or fewer findings.

### Step 5: Generate Report

```
═══════════════════════════════════════════════════
PR Review Report: #123
═══════════════════════════════════════════════════

Summary:
  Files changed: 12
  Lines added: 234
  Lines removed: 45

Findings: 8 total
  🔴 Critical: 1
  🟠 Major: 2
  🟡 Minor: 3
  💡 Suggestions: 2

───────────────────────────────────────────────────
CRITICAL FINDINGS
───────────────────────────────────────────────────

[SEC-001] SQL Injection Vulnerability (Confidence: 0.95)
File: src/api/users.ts:45
Category: Security

The query uses string interpolation without parameterization:
```ts
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

Suggested fix:
```ts
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

───────────────────────────────────────────────────
MAJOR FINDINGS
───────────────────────────────────────────────────

[PERF-001] N+1 Query Pattern (Confidence: 0.82)
...

───────────────────────────────────────────────────
VERDICT
───────────────────────────────────────────────────

❌ REQUEST_CHANGES

This PR has 1 critical security issue that must be addressed
before merging. See SEC-001 above.

───────────────────────────────────────────────────
```

### Step 6: Submit Review (Optional)

```
Submit this review to Gitea?
1. Yes, with REQUEST_CHANGES
2. Yes, as COMMENT only
3. No, just show me the report
```

If yes, use `create_pr_review` MCP tool.

## Output

Full review report with:
- Summary statistics
- Findings grouped by severity
- Code snippets with context
- Suggested fixes
- Overall verdict

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PR_REVIEW_CONFIDENCE_THRESHOLD` | `0.7` | Minimum confidence to report (0.0-1.0) |
| `PR_REVIEW_AUTO_SUBMIT` | `false` | Auto-submit to Gitea |
