---
name: pattern-enforcement
description: Read and enforce user-declared design patterns from .claude/design-patterns.json. Loaded by all /design commands and by design-reviewer agent. Makes locked patterns hard constraints during component generation, CSS edits, and layout changes.
---

# Pattern Enforcement

## Purpose

Load `.claude/design-patterns.json` at the start of any UI-related session. Surface
locked patterns as hard constraints. Prevent violations during code generation, CSS
edits, or layout changes.

## When to Load

Auto-loaded by:
- All `/design` commands
- `design-reviewer` agent
- Any skill or agent that reads or writes `assets/*.css` or Dash Python files

## File Location

`.claude/design-patterns.json` (consumer project root). If absent, no declared patterns —
behavior unchanged.

Schema: `mcp-servers/dmc-design/schemas/design-patterns.schema.json`.

## Enforcement Protocol

1. Read `.claude/design-patterns.json` at session start (cache in context)
2. For each locked pattern:
   - `severity: fail` → violation blocks the operation
   - `severity: warn` → warning, proceed
3. Report violations with pattern id, rule text, file/line reference
4. When generating code, verify output against applicable patterns before writing

## Pattern Categories

- `layout` — AppShell, flexbox, grid, Paper/Card dimensions
- `css` — custom properties, selector scoping, color scheme blocks
- `component` — DMC prop combinations, usage conventions
- `naming` — file, class, id, variable naming

## CSS Entry Point Discovery

For `css`-category patterns:
1. `.env` `CSS_ENTRY_POINT` variable
2. `assets/styles.css`
3. Glob `assets/*.css`
4. `static/css/*.css`
5. None found → skip css pattern enforcement

## Integration with color-scheme-validation

If `scheme_mode = "dual"` in `.claude/design-patterns.json`, also load
`color-scheme-validation.md` and apply Rules 1–5.
