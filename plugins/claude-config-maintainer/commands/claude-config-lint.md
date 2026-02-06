---
name: claude-config lint
description: Lint CLAUDE.md for common anti-patterns and best practices
---

# /claude-config lint

Check CLAUDE.md against best practices and detect common anti-patterns.

## Skills to Load

- skills/visual-header.md
- skills/lint-rules.md

## Visual Output

Display: `CONFIG-MAINTAINER - CLAUDE.md Lint`

## Usage

```
/claude-config lint                         # Full lint
/claude-config lint --fix                   # Auto-fix issues
/claude-config lint --rules=security        # Check specific category
```

## Workflow

1. Parse markdown structure and hierarchy
2. Check for hardcoded paths, secrets, sensitive data
3. Identify content anti-patterns
4. Verify consistent formatting
5. Generate report with fix suggestions

## Options

| Option | Description |
|--------|-------------|
| `--fix` | Auto-fix issues |
| `--rules=LIST` | Check specific categories |
| `--ignore=LIST` | Skip specified rules |
| `--severity=LEVEL` | Filter by severity |
| `--strict` | Treat warnings as errors |

## When to Use

- Before committing CLAUDE.md changes
- During code review
- Periodically as maintenance
