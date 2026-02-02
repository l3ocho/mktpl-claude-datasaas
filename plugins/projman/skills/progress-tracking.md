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

## Sprint Dispatch Log

A single structured comment on the sprint milestone that records all task dispatches and completions. This is the first place to look when resuming an interrupted sprint.

### Format

Post as a comment on the milestone (via `add_comment` on a pinned tracking issue, or as milestone description appendix):

```markdown
## Sprint Dispatch Log

| Time | Issue | Action | Agent | Branch | Notes |
|------|-------|--------|-------|--------|-------|
| 14:30 | #45 | Dispatched | Executor | feat/45-jwt | Parallel batch 1 |
| 14:30 | #46 | Dispatched | Executor | feat/46-login | Parallel batch 1 |
| 14:45 | #45 | Complete | Executor | feat/45-jwt | 47 tool calls, merged |
| 14:52 | #46 | Failed | Executor | feat/46-login | Auth test failure |
| 14:53 | #46 | Re-dispatched | Executor | feat/46-login | After fix |
| 15:10 | #46 | Complete | Executor | feat/46-login | 62 tool calls, merged |
| 15:10 | #47 | Dispatched | Executor | feat/47-tests | Batch 2 (depended on #45, #46) |
```

### When to Log

| Event | Action Column | Required Fields |
|-------|---------------|-----------------|
| Task dispatched to executor | `Dispatched` | Time, Issue, Branch, Batch info |
| Task completed | `Complete` | Time, Issue, Tool call count |
| Task failed | `Failed` | Time, Issue, Error summary |
| Task re-dispatched | `Re-dispatched` | Time, Issue, Reason |
| Domain gate checked | `Gate: PASS` or `Gate: FAIL` | Time, Issue, Domain |
| Sprint resumed | `Resumed` | Time, Notes (from checkpoint) |

### Implementation

The orchestrator appends rows to this log via `add_comment` on the first issue in the milestone (or a dedicated tracking issue). Each append is a single `add_comment` call updating the table.

**On sprint start:** Create the dispatch log header.
**On each event:** Append a row.
**On sprint resume:** Add a "Resumed" row with checkpoint context.

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
