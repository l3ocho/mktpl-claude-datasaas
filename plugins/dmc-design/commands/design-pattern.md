---
name: design pattern
description: [dmc-design] Design pattern enforcement — scan, lock, check, list, unlock
skills:
  - skills/pattern-enforcement/SKILL.md
---

# /design pattern

Manage user-declared design patterns stored in `.claude/design-patterns.json`.

## Usage

```
/design pattern scan              — Extract current patterns from code + CSS
/design pattern lock "<rule>"     — Declare a new pattern
/design pattern check             — Verify all locked patterns hold
/design pattern list              — Show all locked patterns
/design pattern unlock <id>       — Remove a pattern
```

## Routing

Route based on first word of $ARGUMENTS:
- `scan` → execute pattern scan workflow
- `lock` → execute pattern lock workflow
- `check` → execute pattern check workflow
- `list` → execute pattern list workflow
- `unlock` → execute pattern unlock workflow

If no action given, display usage above.

## scan

Read `assets/*.css` and Python files. Extract:
- CSS custom properties (grouped by color scheme if dual mode)
- Repeated DMC prop combinations on Paper, Card, Stack components
Write results to `.claude/design-patterns.json` as source: "scan" entries.

## lock

Parse the user's natural language rule from $ARGUMENTS.
Determine category (layout/css/component/naming).
Generate a pattern entry with:
- id: next available p{NNN} (e.g. p001, p002)
- declared_by: "user"
- declared_at: current ISO timestamp
- rule: the user's declaration
- category: inferred
- enforcement.file_globs: based on category
- enforcement.detect: description of what to detect
- enforcement.severity: "fail"
- source: "manual"
Append to patterns array in `.claude/design-patterns.json`. Create file if absent.

## check

Read `.claude/design-patterns.json`.
For each locked pattern, check current codebase files matching file_globs.
Report violations grouped by severity.

## list

Read `.claude/design-patterns.json`.
Display patterns grouped by category (layout, css, component, naming).
Show id, rule, severity, source for each.

## unlock

Read pattern id from $ARGUMENTS.
Confirm with user.
Remove the matching pattern from the file.
