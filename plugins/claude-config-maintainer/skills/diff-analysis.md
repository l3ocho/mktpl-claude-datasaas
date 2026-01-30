# CLAUDE.md Diff Analysis

This skill defines how to analyze and present CLAUDE.md differences.

## Comparison Modes

| Mode | Command | Description |
|------|---------|-------------|
| Working vs HEAD | `/config-diff` | Uncommitted changes |
| Working vs Commit | `--commit=REF` | Changes since specific point |
| Commit to Commit | `--from=X --to=Y` | Historical comparison |
| Branch Comparison | `--branch=NAME` | Cross-branch differences |

## Change Indicators

| Symbol | Meaning |
|--------|---------|
| `+` | Line added |
| `-` | Line removed |
| `@@` | Location marker (line numbers) |
| `[MODIFIED]` | Section has changes |
| `[ADDED]` | New section created |
| `[REMOVED]` | Section deleted |
| `[UNCHANGED]` | No changes to section |

## Impact Categories

| Category | Meaning |
|----------|---------|
| NEW REQUIREMENT | Claude will need to do something new |
| REMOVED REQUIREMENT | Claude no longer needs to do something |
| MODIFIED | Existing behavior changed |
| NEW RULE | New constraint added |
| RELAXED RULE | Constraint removed or softened |

## Report Format

```
CLAUDE.md Diff Report
=====================

File: /path/to/project/CLAUDE.md
Comparing: [mode description]
Commit: [ref] "[message]" (time ago)

Summary:
- Lines added: N
- Lines removed: N
- Net change: +/-N lines
- Sections affected: N

Section Changes:
----------------

## Section Name [STATUS]
  +/- Change description

Detailed Diff:
--------------

--- CLAUDE.md (before)
+++ CLAUDE.md (after)

@@ -N,M +N,M @@
 context
-removed
+added
 context

Behavioral Impact:
------------------

These changes will affect Claude's behavior:

N. [CATEGORY] Description of impact
```

## Section-Focused View

When using `--section=NAME`:
- Filter diff to only that section
- Show section-specific statistics
- Highlight behavioral impact for that area

## Troubleshooting

### No changes detected
- File matches comparison target
- Verify comparing correct commits

### File not found in commit
- CLAUDE.md didn't exist at that point
- Use `git log -- CLAUDE.md` to find creation

### Not a git repository
- Command requires git history
- Initialize git or use file backup comparison
