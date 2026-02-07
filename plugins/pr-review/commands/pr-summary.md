---
name: pr summary
description: Quick summary of PR changes
agent: coordinator
---

# /pr summary - Quick PR Summary

## Visual Output

Display header: `PR-REVIEW - Quick Summary`

## Skills to Load

- skills/mcp-tools-reference.md
- skills/pr-analysis.md
- skills/output-formats.md

## Usage

```
/pr summary <pr-number> [--repo owner/repo]
```

## Workflow

### Step 1: Fetch PR Data

Load MCP tools, then: `get_pull_request`, `get_pr_diff`

### Step 2: Analyze Changes

Execute `skills/pr-analysis.md`:
- Categorize changes (feature, fix, refactor)
- Calculate statistics
- Identify key files
- Assess scope and risk

### Step 3: Generate Summary

Use summary format from `skills/output-formats.md`

## When to Use

- Quick overview before full review
- Triage multiple PRs
- Decide if `/pr review` is needed
