---
description: Manual project hygiene check — validates file organization and cleanup
---

# /hygiene check

## Purpose

Manually run project hygiene checks that were previously automatic (PostToolUse hook removed per Decision #29).

## Checks Performed

1. **Temp file detection** — find files in project root that look temporary (*.tmp, *.bak, *.swp, *~)
2. **Misplaced files** — files outside their expected directories per project conventions
3. **Empty directories** — directories with no files
4. **Large files** — files exceeding reasonable size thresholds
5. **Debug artifacts** — leftover debug logs, console.log statements, print statements

## Usage

```
/hygiene check              # Run all checks
/hygiene check --fix        # Auto-fix safe issues (delete temp files, remove empty dirs)
```

## Output

```
Temp files: 0 found
Misplaced files: 0 found
Empty directories: 2 found
Large files: 0 found
Debug artifacts: 1 found

Fixable: 2 issues (run with --fix)
```
