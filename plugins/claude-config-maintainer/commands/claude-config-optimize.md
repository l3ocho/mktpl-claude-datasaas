---
name: claude-config optimize
description: Optimize CLAUDE.md structure and content
---

# /claude-config optimize

Automatically optimize CLAUDE.md based on best practices.

## Skills to Load

- skills/visual-header.md
- skills/optimization-patterns.md
- skills/pre-change-protocol.md
- skills/claude-md-structure.md

## Visual Output

Display: `CONFIG-MAINTAINER - CLAUDE.md Optimization`

## Usage

```
/claude-config optimize                # Full optimization
/claude-config optimize --condense     # Reduce verbosity
/claude-config optimize --dry-run      # Preview only
```

## Workflow

1. Identify optimization opportunities
2. Plan restructure, condense, or add actions
3. Show before/after preview
4. Apply changes with approval
5. Verify improvements

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview without applying |
| `--no-backup` | Skip backup |
| `--aggressive` | Maximum condensation |
| `--section=NAME` | Optimize specific section |

**Priority:** Add Pre-Change Protocol if missing.

## Safety

- Auto backup to `.claude/backups/`
- Preview before applying
