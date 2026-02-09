---
name: projman sprint review
description: Pre-sprint-close code quality review
agent: code-reviewer
---

# Sprint Review - Code Review for Sprint Close

## Skills Required

- skills/review-checklist.md
- skills/sprint-lifecycle.md

## Purpose

Review recent code changes for quality issues before closing the sprint.

## Invocation

Run `/sprint review` before `/sprint close` to catch issues.

## Workflow

0. **Check Lifecycle State** - Execute `skills/sprint-lifecycle.md` check protocol. Expect `Sprint/Executing`. Set `Sprint/Reviewing` after review begins. Warn if in wrong state (allow with `--force`).
1. **Determine Scope** - Sprint files or recent commits (`git diff --name-only HEAD~5`)
2. **Read Files** - Use Read tool for each file in scope
3. **Scan for Patterns** - Check each category from review checklist
4. **Compile Findings** - Group by severity (Critical, Warning, Recommendation)
5. **Report Verdict** - READY / NEEDS ATTENTION / BLOCK

## Review Categories

See `skills/review-checklist.md` for complete patterns:
- Debug artifacts (TODO, console.log, commented code)
- Code quality (long functions, deep nesting, duplication)
- Security (hardcoded secrets, SQL injection, disabled SSL)
- Error handling (bare except, swallowed exceptions)

## DO NOT

- Rewrite or refactor code automatically
- Make changes without explicit approval
- Review files outside sprint/change scope
- Spend excessive time on style issues

## Visual Output

See `skills/visual-output.md`. This command invokes the **Code Reviewer** agent:
- Phase Emoji: 🔍
- Phase Name: REVIEW
- Context: Sprint Name
