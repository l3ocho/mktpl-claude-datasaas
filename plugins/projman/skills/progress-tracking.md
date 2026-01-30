---
name: progress-tracking
description: Structured progress comments and status label management
---

# Progress Tracking

## Purpose

Defines structured progress comment format and status label management.

## When to Use

- **Orchestrator agent**: When tracking sprint execution
- **Executor agent**: When posting progress updates
- **Commands**: `/sprint-start`, `/sprint-status`

---

## Status Labels

| Label | Meaning | When to Apply |
|-------|---------|---------------|
| `Status/In-Progress` | Work actively happening | When dispatching task |
| `Status/Blocked` | Cannot proceed | When dependency or blocker found |
| `Status/Failed` | Task failed | When task cannot complete |
| `Status/Deferred` | Moved to future | When deprioritized |

### Rules

- Only ONE Status label at a time
- Remove Status labels when closing successfully
- Always add comment explaining status changes

---

## Applying Status Labels

**When dispatching:**
```python
update_issue(
    repo="org/repo",
    issue_number=45,
    labels=["Status/In-Progress", ...existing_labels]
)
```

**When blocked:**
```python
update_issue(
    repo="org/repo",
    issue_number=46,
    labels=["Status/Blocked", ...labels_without_in_progress]
)
add_comment(repo="org/repo", number=46, body="🚫 BLOCKED: Waiting for #45")
```

**When failed:**
```python
update_issue(
    repo="org/repo",
    issue_number=47,
    labels=["Status/Failed", ...labels_without_in_progress]
)
add_comment(repo="org/repo", number=47, body="❌ FAILED: [Error description]")
```

**On successful close:**
```python
update_issue(
    repo="org/repo",
    issue_number=45,
    state="closed",
    labels=[...labels_without_status]  # Remove all Status/* labels
)
```

---

## Structured Progress Comment Format

```markdown
## Progress Update
**Status:** In Progress | Blocked | Failed
**Phase:** [current phase name]
**Tool Calls:** X (budget: Y)

### Completed
- [x] Step 1
- [x] Step 2

### In Progress
- [ ] Current step (estimated: Z more calls)

### Blockers
- None | [blocker description]

### Next
- What happens after current step
```

---

## When to Post Progress Comments

- After completing each major phase (every 20-30 tool calls)
- When status changes (blocked, failed)
- When encountering unexpected issues
- Before approaching tool call budget limit

---

## Checkpoint Format (Resume Support)

For resume support, save checkpoints after major steps:

```markdown
## Checkpoint
**Branch:** feat/45-jwt-service
**Commit:** abc123
**Phase:** Testing
**Tool Calls:** 67

### Completed Steps
- [x] Created auth/jwt_service.py
- [x] Implemented generate_token()
- [x] Implemented verify_token()

### Pending Steps
- [ ] Write unit tests
- [ ] Add refresh logic
- [ ] Commit and push

### Files Modified
- auth/jwt_service.py (new)
- auth/__init__.py (modified)
```

---

## Sprint Progress Display

```
┌─ Sprint Progress ────────────────────────────────────────────────┐
│  Sprint 18 - User Authentication                                 │
│  ████████████░░░░░░░░░░░░░░░░░░ 40% complete                     │
│  ✅ Done: 4    ⏳ Active: 2    ⬚ Pending: 4                       │
│  Current:                                                        │
│    #45 ⏳ Implement JWT service                                  │
│    #46 ⏳ Build login endpoint                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Progress Bar Calculation

- Width: 30 characters
- Filled: `█` (completed percentage)
- Empty: `░` (remaining percentage)
- Formula: `(closed_issues / total_issues) * 30`

---

## Parallel Execution Status

```
Parallel Execution Status:

Batch 1:
  ✅ #45 - JWT service - COMPLETED (12:45)
  🔄 #48 - API docs - IN PROGRESS (75%)

Batch 2 (now unblocked):
  ⏳ #46 - Login endpoint - READY TO START
  ⏳ #49 - Auth tests - READY TO START

#45 completed! #46 and #49 are now unblocked.
```

---

## Auto-Check Subtasks on Close

When closing an issue, update unchecked subtasks in body:

```python
# Change - [ ] to - [x] for completed items
update_issue(
    repo="org/repo",
    issue_number=45,
    body="... - [x] Completed subtask ..."
)
```
