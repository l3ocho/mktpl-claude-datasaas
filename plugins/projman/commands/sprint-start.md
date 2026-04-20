---
name: projman sprint start
description: [projman] Begin sprint execution with relevant lessons learned from previous sprints
agent: orchestrator
---

# Start Sprint Execution

## Skills Required

- skills/mcp-tools-reference/SKILL.md (frontmatter — auto-injected)
- skills/batch-execution/SKILL.md (frontmatter — auto-injected)
- skills/branch-security/SKILL.md
- skills/sprint-approval/SKILL.md
- skills/dependency-management/SKILL.md
- skills/lessons-learned/SKILL.md
- skills/git-workflow/SKILL.md
- skills/progress-tracking/SKILL.md
- skills/runaway-detection/SKILL.md
- skills/sprint-lifecycle/SKILL.md

## Purpose

Initiate sprint execution. The orchestrator agent verifies approval, analyzes dependencies for parallel execution, searches relevant lessons, and coordinates task dispatch.

## Invocation

Run `/sprint start` when ready to begin executing a planned sprint.

**Flags:**
- `--force` — Bypass approval gate (emergency only, logged to milestone)

## Workflow

Execute the sprint start workflow:

1. **Verify Sprint Approval & Lifecycle State** (required) - Check milestone for approval record. STOP if missing unless `--force` flag provided. Also verify lifecycle state is `Sprint/Planning` per `skills/sprint-lifecycle/SKILL.md`. Set `Sprint/Executing` after verification passes.
2. **Detect Checkpoints** - Check for resume points from interrupted sessions
3. **Fetch Sprint Issues** - Get open issues from milestone
4. **Analyze Dependencies** - Use `get_execution_order` for parallel batches
5. **Search Relevant Lessons** - Find applicable past experiences
6. **Dispatch Tasks** - Parallel when safe, sequential when file conflicts exist

**File Conflict Prevention:** Before parallel dispatch, check target files for overlap. Sequentialize tasks that modify the same files.

**Branch Isolation:** Each task runs on its own branch (`feat/<issue>-<desc>`).

**Sequential Merge:** After completion, merge branches sequentially to detect conflicts.

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  ⚡ EXECUTION                                                    ║
║  [Sprint Name]                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```
