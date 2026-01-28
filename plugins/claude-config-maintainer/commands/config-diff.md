---
description: Show diff between current CLAUDE.md and last commit
---

# Compare CLAUDE.md Changes

This command shows differences between your current CLAUDE.md file and previous versions, helping track configuration drift and review changes before committing.

## What This Command Does

1. **Detect CLAUDE.md Location** - Finds the project's CLAUDE.md file
2. **Compare Versions** - Shows diff against last commit or specified revision
3. **Highlight Sections** - Groups changes by affected sections
4. **Summarize Impact** - Explains what the changes mean for Claude's behavior

## Usage

```
/config-diff
```

Compare against a specific commit:

```
/config-diff --commit=abc1234
/config-diff --commit=HEAD~3
```

Compare two specific commits:

```
/config-diff --from=abc1234 --to=def5678
```

Show only specific sections:

```
/config-diff --section="Critical Rules"
/config-diff --section="Quick Start"
```

## Comparison Modes

### Default: Working vs Last Commit
Shows uncommitted changes to CLAUDE.md:
```
/config-diff
```

### Working vs Specific Commit
Shows changes since a specific point:
```
/config-diff --commit=v1.0.0
```

### Commit to Commit
Shows changes between two historical versions:
```
/config-diff --from=v1.0.0 --to=v2.0.0
```

### Branch Comparison
Shows CLAUDE.md differences between branches:
```
/config-diff --branch=main
/config-diff --from=feature-branch --to=main
```

## Expected Output

```
CLAUDE.md Diff Report
=====================

File: /path/to/project/CLAUDE.md
Comparing: Working copy vs HEAD (last commit)
Commit: abc1234 "Update build commands" (2 days ago)

Summary:
- Lines added: 12
- Lines removed: 5
- Net change: +7 lines
- Sections affected: 3

Section Changes:
----------------

## Quick Start [MODIFIED]
  - Added new environment variable requirement
  - Updated test command with coverage flag

## Critical Rules [ADDED CONTENT]
  + New rule: "Never modify database migrations directly"

## Architecture [UNCHANGED]

## Common Operations [MODIFIED]
  - Removed deprecated deployment command
  - Added new Docker workflow

Detailed Diff:
--------------

--- CLAUDE.md (HEAD)
+++ CLAUDE.md (working)

@@ -15,7 +15,10 @@
 ## Quick Start

 ```bash
+export DATABASE_URL=postgres://...  # Required
 pip install -r requirements.txt
-pytest
+pytest --cov=src                    # Run with coverage
 uvicorn main:app --reload
 ```

@@ -45,6 +48,7 @@
 ## Critical Rules

 - Never modify `.env` files directly
+- Never modify database migrations directly
 - Always run tests before committing

Behavioral Impact:
------------------

These changes will affect Claude's behavior:

1. [NEW REQUIREMENT] Claude will now export DATABASE_URL before running
2. [MODIFIED] Test command now includes coverage reporting
3. [NEW RULE] Claude will avoid direct migration modifications

Review: Do these changes reflect your intended configuration?
```

## Section-Focused View

When using `--section`, output focuses on specific areas:

```
/config-diff --section="Critical Rules"

CLAUDE.md Section Diff: Critical Rules
======================================

--- HEAD
+++ Working

 ## Critical Rules

 - Never modify `.env` files directly
+- Never modify database migrations directly
+- Always use type hints in Python code
 - Always run tests before committing
-- Keep functions under 50 lines

Changes:
  + 2 rules added
  - 1 rule removed

Impact: Claude will follow 2 new constraints and no longer enforce
the 50-line function limit.
```

## Options

| Option | Description |
|--------|-------------|
| `--commit=REF` | Compare working copy against specific commit/tag |
| `--from=REF` | Starting point for comparison |
| `--to=REF` | Ending point for comparison (default: HEAD) |
| `--branch=NAME` | Compare against branch tip |
| `--section=NAME` | Show only changes to specific section |
| `--stat` | Show only statistics, no detailed diff |
| `--no-color` | Disable colored output |
| `--context=N` | Lines of context around changes (default: 3) |

## Understanding the Output

### Change Indicators

| Symbol | Meaning |
|--------|---------|
| `+` | Line added |
| `-` | Line removed |
| `@@` | Location marker showing line numbers |
| `[MODIFIED]` | Section has changes |
| `[ADDED]` | New section created |
| `[REMOVED]` | Section deleted |
| `[UNCHANGED]` | No changes to section |

### Impact Categories

- **NEW REQUIREMENT** - Claude will now need to do something new
- **REMOVED REQUIREMENT** - Claude no longer needs to do something
- **MODIFIED** - Existing behavior changed
- **NEW RULE** - New constraint added
- **RELAXED RULE** - Constraint removed or softened

## When to Use

Run `/config-diff` when:
- Before committing CLAUDE.md changes
- Reviewing what changed after pulling updates
- Debugging unexpected Claude behavior
- Auditing configuration changes over time
- Comparing configurations across branches

## Integration with Other Commands

| Workflow | Commands |
|----------|----------|
| Review before commit | `/config-diff` then `git commit` |
| After optimization | `/config-optimize` then `/config-diff` |
| Audit history | `/config-diff --from=v1.0.0 --to=HEAD` |
| Branch comparison | `/config-diff --branch=main` |

## Tips

1. **Review before committing** - Always check what changed
2. **Track behavioral changes** - Focus on rules and requirements sections
3. **Use section filtering** - Large files benefit from focused diffs
4. **Compare across releases** - Use tags to track major changes
5. **Check after merges** - Ensure CLAUDE.md didn't get conflict artifacts

## Troubleshooting

### "No changes detected"
- CLAUDE.md matches the comparison target
- Check if you're comparing the right commits

### "File not found in commit"
- CLAUDE.md didn't exist at that commit
- Use `git log -- CLAUDE.md` to find when it was created

### "Not a git repository"
- This command requires git history
- Initialize git or use file backup comparison instead
