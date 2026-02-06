---
name: pr findings
description: List and filter review findings by category/severity
agent: coordinator
---

# /pr findings - Filter Review Findings

## Visual Output

Display header: `PR-REVIEW - Findings`

## Skills to Load

- skills/mcp-tools-reference.md
- skills/review-patterns/confidence-scoring.md
- skills/output-formats.md

## Usage

```
/pr findings <pr-number> [--category <cat>] [--severity <sev>] [--confidence <min>] [--file <pattern>] [--compact] [--json]
```

## Workflow

### Without Previous Review

Prompt: "No review found. Run `/pr review`, `/pr summary`, or cancel?"

### With Previous Review

1. Load findings from previous review
2. Apply filters (category, severity, confidence, file)
3. Display using format from `skills/output-formats.md`

## Output Formats

Reference `skills/output-formats.md`:
- **Detailed** (default) - Full finding
- **Compact** (`--compact`) - Single line
- **JSON** (`--json`) - Structured data

## Examples

```bash
/pr findings 123 --category security
/pr findings 123 --severity critical,major
/pr findings 123 --confidence 0.8
/pr findings 123 --file src/api/*
```
