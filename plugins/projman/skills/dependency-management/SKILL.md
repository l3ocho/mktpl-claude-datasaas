---
name: dependency-management
description: Parallel execution planning, dependency graphs, and file conflict prevention
---

# Dependency Management

## Purpose

Defines how to analyze dependencies, plan parallel execution, and prevent file conflicts.

## When to Use

- **Orchestrator agent**: When starting sprint execution
- **Commands**: `/sprint start`, `/sprint-diagram`

---

## Get Execution Order

```python
get_execution_order(repo="org/repo", issue_numbers=[45, 46, 47, 48, 49])
```

Returns batches that can run in parallel:
```json
{
  "batches": [
    [45, 48],   // Batch 1: No dependencies
    [46, 49],   // Batch 2: Depends on batch 1
    [47]        // Batch 3: Depends on batch 2
  ]
}
```

**Independent tasks in the same batch can run in parallel.**

---

## Parallel Execution Display

```
Parallel Execution Batches:
┌─────────────────────────────────────────────────────────────┐
│ Batch 1 (can start immediately):                            │
│   • #45 [Sprint 18] feat: Implement JWT service             │
│   • #48 [Sprint 18] docs: Update API documentation          │
├─────────────────────────────────────────────────────────────┤
│ Batch 2 (after batch 1):                                    │
│   • #46 [Sprint 18] feat: Build login endpoint (needs #45)  │
│   • #49 [Sprint 18] test: Add auth tests (needs #45)        │
├─────────────────────────────────────────────────────────────┤
│ Batch 3 (after batch 2):                                    │
│   • #47 [Sprint 18] feat: Create login form (needs #46)     │
└─────────────────────────────────────────────────────────────┘
```

---

## File Conflict Prevention (MANDATORY)

**CRITICAL: Before dispatching parallel agents, check for file overlap.**

### Pre-Dispatch Conflict Check

1. **Identify target files** for each task in the batch
2. **Check for overlap** - Do any tasks modify the same file?
3. **If overlap detected** - Sequentialize those specific tasks

### Example Analysis

```
Batch 1 Analysis:
  #45 - Implement JWT service
        Files: auth/jwt_service.py, auth/__init__.py
  #48 - Update API documentation
        Files: docs/api.md, README.md
  Overlap: NONE → Safe to parallelize ✅

Batch 2 Analysis:
  #46 - Build login endpoint
        Files: api/routes/auth.py, auth/__init__.py
  #49 - Add auth tests
        Files: tests/test_auth.py, auth/__init__.py
  Overlap: auth/__init__.py → CONFLICT! ⚠️
  Action: Sequentialize #46 and #49 (run #46 first)
```

### Conflict Resolution Rules

| Conflict Type | Action |
|---------------|--------|
| Same file in checklist | Sequentialize tasks |
| Same directory | Review if safe, usually OK |
| Shared test file | Sequentialize or assign different test files |
| Shared config | Sequentialize |

---

## Branch Isolation Protocol

Each task MUST have its own branch:
```
Task #45 → feat/45-jwt-service (isolated)
Task #48 → feat/48-api-docs (isolated)
```

Never have two agents work on the same branch.

---

## Sequential Merge After Completion

```
1. Task #45 completes → merge feat/45-jwt-service to development
2. Task #48 completes → merge feat/48-api-docs to development
3. Never merge simultaneously - always sequential to detect conflicts
```

**If Merge Conflict Occurs:**
1. Stop second task
2. Resolve conflict manually or assign to human
3. Resume/restart second task with updated base

---

## Creating Dependencies

```python
# Issue 46 depends on issue 45
create_issue_dependency(
    repo="org/repo",
    issue_number=46,
    depends_on=45
)
```

This ensures #46 won't be scheduled until #45 completes.
