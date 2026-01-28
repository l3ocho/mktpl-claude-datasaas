---
name: review
description: Pre-sprint-close code quality review
---

# Code Review for Sprint Close

Review the recent code changes for quality issues before closing the sprint.

## Review Checklist

Analyze the changes and report on:

### 1. Debug Artifacts
- [ ] TODO/FIXME comments that should be resolved or converted to issues
- [ ] Console.log, print(), debug statements left in code
- [ ] Commented-out code blocks

### 2. Code Quality
- [ ] Functions exceeding 50 lines (complexity smell)
- [ ] Deeply nested conditionals (>3 levels)
- [ ] Duplicate code patterns
- [ ] Missing docstrings/comments on public functions

### 3. Security Scan (Lightweight)
- [ ] Hardcoded strings that look like secrets (API keys, passwords, tokens)
- [ ] SQL strings with concatenation (injection risk)
- [ ] Disabled SSL verification
- [ ] Overly permissive file permissions in code

### 4. Error Handling
- [ ] Bare except/catch blocks
- [ ] Swallowed exceptions (catch with pass/empty block)
- [ ] Missing null/undefined checks on external data

## Output Format

Provide a structured report:

```
## Sprint Review Summary

### Critical Issues (Block Sprint Close)
- [file:line] Description

### Warnings (Should Address)
- [file:line] Description

### Recommendations (Nice to Have)
- [file:line] Description

### Clean Files
- List of files with no issues found
```

## Scope

If sprint context is available from projman, limit review to files touched in current sprint.
Otherwise, review staged changes or changes in the last 5 commits.

## How to Determine Scope

1. **Check for sprint context**: Look for `.projman/current-sprint.json` or similar
2. **Fall back to git changes**: Use `git diff --name-only HEAD~5` or staged files
3. **Filter by file type**: Focus on code files (.py, .js, .ts, .go, .rs, etc.)

## Execution Steps

1. Determine scope (sprint files or recent commits)
2. For each file in scope:
   - Read the file content
   - Scan for patterns in each category
   - Record findings with file:line references
3. Compile findings into the structured report
4. Provide recommendation: READY / NEEDS ATTENTION / BLOCK

## Visual Output

When executing this command, display the plugin header:

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🏁 CLOSING                                                      ║
║  Code Review                                                     ║
╚══════════════════════════════════════════════════════════════════╝
```

Then proceed with the review workflow.

## Do NOT

- Rewrite or refactor code automatically
- Make changes without explicit approval
- Review files outside the sprint/change scope
- Spend excessive time on style issues (assume formatters handle this)
