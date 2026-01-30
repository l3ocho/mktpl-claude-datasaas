---
description: Show diff between current CLAUDE.md and last commit
---

# Compare CLAUDE.md Changes

Show differences between CLAUDE.md versions to track configuration drift.

## Skills to Load

- skills/visual-header.md
- skills/diff-analysis.md

## Visual Output

Display: `CONFIG-MAINTAINER - CLAUDE.md Diff`

## Usage

```
/config-diff                           # Working vs last commit
/config-diff --commit=abc1234          # Working vs specific commit
/config-diff --from=v1.0 --to=v2.0     # Compare two commits
/config-diff --section="Critical Rules"  # Specific section only
```

## Workflow

1. Find project's CLAUDE.md file
2. Show diff against target revision
3. Group changes by affected sections
4. Explain behavioral implications

## Options

| Option | Description |
|--------|-------------|
| `--commit=REF` | Compare against specific commit |
| `--from=REF` | Starting point |
| `--to=REF` | Ending point (default: HEAD) |
| `--section=NAME` | Show only specific section |
| `--stat` | Statistics only |

## When to Use

- Before committing CLAUDE.md changes
- Reviewing changes after pull
- Debugging unexpected behavior
