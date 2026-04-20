---
name: projman sprint plan
description: [projman] Start sprint planning with AI-guided architecture analysis and issue creation
agent: planner
---

# Sprint Planning

## Skills Required

- skills/mcp-tools-reference/SKILL.md (frontmatter — auto-injected)
- skills/batch-execution/SKILL.md (frontmatter — auto-injected)
- skills/branch-security/SKILL.md
- skills/repo-validation/SKILL.md
- skills/input-detection/SKILL.md
- skills/lessons-learned/SKILL.md
- skills/wiki-conventions/SKILL.md
- skills/task-sizing/SKILL.md
- skills/issue-conventions/SKILL.md
- skills/sprint-approval/SKILL.md
- skills/planning-workflow/SKILL.md
- skills/label-taxonomy/SKILL.md
- skills/sprint-lifecycle/SKILL.md

## Purpose

Initiate sprint planning session. The planner agent validates prerequisites, gathers requirements, searches lessons learned, creates wiki pages, and creates well-structured Gitea issues with proper dependencies and labels.

## Invocation

Provide sprint goals as natural language input, or prepare input via:
- `docs/changes/*.md` file with frontmatter
- Existing wiki proposal page
- Direct conversation

## Workflow

Execute the planning workflow as defined in `skills/planning-workflow/SKILL.md`.

**Key steps:**
0. **Check Lifecycle State** - Execute `skills/sprint-lifecycle/SKILL.md` check protocol. Expect idle state. Set `Sprint/Planning` after planning completes. Warn and stop if sprint is in another active state (unless `--force`).
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

