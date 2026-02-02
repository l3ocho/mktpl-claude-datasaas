---
description: Begin sprint execution with relevant lessons learned from previous sprints
agent: orchestrator
---

# Start Sprint Execution

## Skills Required

- skills/mcp-tools-reference.md
- skills/branch-security.md
- skills/sprint-approval.md
- skills/dependency-management.md
- skills/lessons-learned.md
- skills/git-workflow.md
- skills/progress-tracking.md
- skills/runaway-detection.md

## Purpose

Initiate sprint execution. The orchestrator agent verifies approval, analyzes dependencies for parallel execution, searches relevant lessons, and coordinates task dispatch.

## Invocation

Run `/sprint-start` when ready to begin executing a planned sprint.

**Flags:**
- `--force` — Bypass approval gate (emergency only, logged to milestone)

## Workflow

Execute the sprint start workflow:

1. **Verify Sprint Approval** (required) - Check milestone for approval record. STOP if missing unless `--force` flag provided.
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
