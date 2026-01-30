---
name: task-sizing
description: Task sizing rules and mandatory breakdown requirements
---

# Task Sizing Rules

## Purpose

Defines effort estimation rules and enforces task breakdown requirements.

## When to Use

- **Planner agent**: When creating issues during sprint planning
- **Orchestrator agent**: When reviewing task scope during sprint start
- **Code Reviewer agent**: When flagging oversized tasks

---

## Sizing Matrix

| Effort | Files | Checklist Items | Max Tool Calls | Agent Scope |
|--------|-------|-----------------|----------------|-------------|
| **XS** | 1 file | 0-2 items | ~30 | Single function/fix |
| **S** | 1 file | 2-4 items | ~50 | Single file feature |
| **M** | 2-3 files | 4-6 items | ~80 | Multi-file feature |
| **L** | MUST BREAK DOWN | - | - | Too large |
| **XL** | MUST BREAK DOWN | - | - | Way too large |

---

## CRITICAL: L/XL Tasks MUST Be Broken Down

**Why:**
- Agents running 400+ tool calls take 1+ hour with no visibility
- Large tasks lack clear completion criteria
- Debugging failures is extremely difficult
- Small tasks enable parallel execution

---

## Scoping Checklist

1. Can this be completed in one file? → XS or S
2. Does it touch 2-3 files? → M (maximum for single task)
3. Does it touch 4+ files? → MUST break down
4. Would you estimate 50+ tool calls? → MUST break down
5. Does it require complex decision-making mid-task? → MUST break down

---

## Breakdown Example

### BAD (L - too broad)
```
[Sprint 3] feat: Implement schema diff detection hook
Labels: Efforts/L
- Hook skeleton
- Pattern detection
- Warning output
- Integration
```

### GOOD (broken into S tasks)
```
[Sprint 3] feat: Create hook skeleton
Labels: Efforts/S
- [ ] Create hook file with standard header
- [ ] Add file type detection for SQL
- [ ] Exit 0 (non-blocking)

[Sprint 3] feat: Add DROP/ALTER pattern detection
Labels: Efforts/S
- [ ] Detect DROP COLUMN/TABLE/INDEX
- [ ] Detect ALTER TYPE changes
- [ ] Detect RENAME operations

[Sprint 3] feat: Add warning output formatting
Labels: Efforts/S
- [ ] Format breaking change warnings
- [ ] Add hook prefix to output

[Sprint 3] chore: Register hook in hooks.json
Labels: Efforts/XS
- [ ] Add PostToolUse:Edit hook entry
```

---

## Enforcement

**The planner MUST refuse to create L/XL tasks without breakdown.**

If user requests a large task:
```
This task appears to be L/XL sized (touches 4+ files, estimated 100+ tool calls).

L/XL tasks MUST be broken down into S/M subtasks because:
- Agents need clear, completable units of work
- Parallel execution requires smaller tasks
- Progress visibility requires frequent checkpoints

Let me break this down into smaller tasks...
```
