---
name: pr diff
description: Formatted diff with inline review comments
agent: coordinator
---

# /pr diff - Annotated PR Diff Viewer

## Visual Output

Display header: `PR-REVIEW - Diff Viewer`

## Skills to Load

- skills/mcp-tools-reference.md
- skills/pr-analysis.md
- skills/output-formats.md

## Usage

```
/pr diff <pr-number> [--repo owner/repo] [--context <n>] [--no-comments] [--file <pattern>]
```

## Workflow

### Step 1: Fetch Data

Load MCP tools, then: `get_pr_diff`, `get_pr_comments`

### Step 2: Parse and Annotate

Execute `skills/pr-analysis.md` Annotated Diff Display:
- Overlay comments at file/line positions
- Show commenter, timestamp, replies
- Mark resolved vs open

### Step 3: Display

Use annotated diff format from `skills/output-formats.md`

## Use Cases

- Review preparation with existing feedback
- Followup work - see what was commented
- Progress tracking on resolved comments

## Related Commands

| Command | Purpose |
|---------|---------|
| `/pr summary` | Quick overview |
| `/pr review` | Full review |
| `/pr findings` | Filter findings |
