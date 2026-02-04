---
description: Start sprint planning with AI-guided architecture analysis and issue creation
agent: planner
---

# Sprint Planning

## Skills Required

- skills/mcp-tools-reference.md (frontmatter — auto-injected)
- skills/batch-execution.md (frontmatter — auto-injected)
- skills/branch-security.md
- skills/repo-validation.md
- skills/input-detection.md
- skills/lessons-learned.md
- skills/wiki-conventions.md
- skills/task-sizing.md
- skills/issue-conventions.md
- skills/sprint-approval.md
- skills/planning-workflow.md
- skills/label-taxonomy/labels-reference.md
- skills/sprint-lifecycle.md
- skills/token-budget-report.md

## Purpose

Initiate sprint planning session. The planner agent validates prerequisites, gathers requirements, searches lessons learned, creates wiki pages, and creates well-structured Gitea issues with proper dependencies and labels.

## Invocation

Provide sprint goals as natural language input, or prepare input via:
- `docs/changes/*.md` file with frontmatter
- Existing wiki proposal page
- Direct conversation

## Workflow

Execute the planning workflow as defined in `skills/planning-workflow.md`.

**Key steps:**
0. **Check Lifecycle State** - Execute `skills/sprint-lifecycle.md` check protocol. Expect idle state. Set `Sprint/Planning` after planning completes. Warn and stop if sprint is in another active state (unless `--force`).
1. Run pre-planning validations (branch, repo org, labels)
2. Detect input source (file, wiki, or conversation)
3. Search relevant lessons learned
4. Create/update wiki proposal and implementation pages
5. Perform architecture analysis
6. Create Gitea issues with wiki references (respecting task sizing rules)
7. Set up dependencies
8. Create or select milestone
9. Request explicit sprint approval

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🎯 PLANNING                                                     ║
║  [Sprint Name]                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

## Final Step: Token Budget Report

After displaying the planning summary and gaining sprint approval, generate a Token Budget Report per `skills/token-budget-report.md`.

- Phase: PLANNING
- List all skills that were loaded during this planning session
- Use the planner agent's model (sonnet) for agent overhead
- Display the formatted report
