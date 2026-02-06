---
name: pr review
description: Full multi-agent PR review with confidence scoring
agent: coordinator
---

# /pr review - Full Multi-Agent Review

## Visual Output

Display header: `PR-REVIEW - Full Review`

## Skills to Load

- skills/mcp-tools-reference.md
- skills/review-workflow.md
- skills/review-patterns/confidence-scoring.md
- skills/output-formats.md

## Usage

```
/pr review <pr-number> [--repo owner/repo]
```

## Workflow

### Step 1: Fetch PR Data

Load MCP tools, then: `get_pull_request`, `get_pr_diff`, `get_pr_comments`

### Step 2: Dispatch to Agents

Execute `skills/review-workflow.md` - dispatch to Security, Performance, Maintainability, Test agents

### Step 3: Aggregate and Filter

Apply confidence threshold (default: 0.7). See `skills/review-patterns/confidence-scoring.md`

### Step 4: Generate Report

Use format from `skills/output-formats.md`. Group by severity: critical > major > minor > suggestion

### Step 5: Determine Verdict

- Any critical or 2+ major: REQUEST_CHANGES
- Only minor/suggestions: COMMENT
- No significant findings: APPROVE

### Step 6: Submit Review (Optional)

Ask user to submit as REQUEST_CHANGES, COMMENT, or skip. Use `create_pr_review` MCP tool.

## Configuration

| Variable | Default |
|----------|---------|
| `PR_REVIEW_CONFIDENCE_THRESHOLD` | `0.7` |
| `PR_REVIEW_AUTO_SUBMIT` | `false` |
