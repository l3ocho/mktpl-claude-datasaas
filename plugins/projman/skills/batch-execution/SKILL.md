---
name: batch-execution
description: Batch MCP API execution to eliminate redundant skill reloading between repetitive operations
---

# Batch Execution Pattern

## Purpose

Separate cognitive work (analysis, planning, decision-making) from mechanical API execution (issue creation, dependency setup, status updates). Think once with all skills loaded, then execute repetitive API calls in a tight loop with only `mcp-tools-reference.md` needed.

## When to Use

- **Planner agent**: After drafting all issues, before calling `create_issue`
- **Orchestrator agent**: When posting status updates, label changes, or comments across multiple issues
- **Any agent**: When making 3+ similar MCP API calls in sequence

## Protocol

### Phase 1: Cognitive Work (all skills loaded)

During analysis, architecture, and planning — use every skill you need. Read files, think deeply, ask questions, resolve ambiguity. This is where the full skill set pays for itself.

**Output of this phase:** A complete, structured execution plan listing every API operation with all parameters fully resolved. No ambiguity, no placeholders that require re-analysis.

### Phase 2: Execution Manifest

Before entering batch mode, produce a structured manifest. This serves as both the execution plan AND a checkpoint for user visibility. Format:

```
## Execution Manifest

### Issue Creation (N items)
1. `create_issue` — title: "[Sprint XX] feat: ..." | labels: [...] | milestone: N
2. `create_issue` — title: "[Sprint XX] fix: ..." | labels: [...] | milestone: N
...

### Dependency Setup (N items)
1. `create_issue_dependency` — issue: $1 depends_on: $2
...

### Milestone Assignment (N items)
1. `update_issue` — issue: $1 milestone: N
...

### Status/Label Updates (N items)
1. `update_issue` — issue: #N labels: [add "Status/In-Progress"]
...
```

Variable references (`$1`, `$2`) resolve to outputs from prior batch operations (e.g., `$1` = issue number returned by first `create_issue`).

### Phase 3: Batch Execute

Execute the manifest items in order, grouped by operation type:

1. **All `create_issue` calls** — collect returned issue numbers
2. **Resolve variable references** — map `$1` → actual issue #45, `$2` → #46, etc.
3. **All `create_issue_dependency` calls** — using resolved numbers
4. **All milestone assignments** — if not done during creation
5. **All status/label updates** — using resolved numbers

**Rules during batch execution:**
- Do NOT re-read any skill files between calls
- Do NOT re-analyze or second-guess the plan — it was finalized in Phase 1
- Do NOT add commentary between individual API calls — batch them silently
- DO track success/failure per operation
- DO continue on individual failures (log and report at end)
- DO post a progress summary after each batch group completes

### Phase 4: Batch Report

After all operations complete, report results:

```
## Batch Execution Complete

### Issue Creation: 6/6 ✓
- #45: [Sprint 19] feat: JWT generation
- #46: [Sprint 19] feat: Login endpoint
- #47: [Sprint 19] feat: Token refresh
- #48: [Sprint 19] test: Auth unit tests
- #49: [Sprint 19] docs: API documentation
- #50: [Sprint 19] chore: CI pipeline

### Dependencies: 4/4 ✓
- #46 depends on #45
- #47 depends on #45
- #48 depends on #46, #47
- #49 depends on #46

### Milestone Assignment: 6/6 ✓
- All issues assigned to Sprint 19

### Failures: 0
```

## Error Handling

| Error | Action |
|-------|--------|
| Single API call fails | Log error, continue with next item |
| Dependency target missing (prior create failed) | Skip dependency, log as blocked |
| All creates fail | STOP batch, report connection/auth issue |
| Partial milestone assignment | Report which issues weren't assigned |

After batch completes, if any failures: present failure summary and ask user whether to retry failed operations or continue.

## Anti-Patterns

| Wrong | Why | Right |
|-------|-----|-------|
| Re-reading `mcp-tools-reference.md` before each API call | Wastes tokens; you already know the tool signatures | Read once, execute many |
| Interleaving analysis with API calls | Forces full context per call | Finish ALL analysis first, THEN batch execute |
| Calling create_issue one at a time with commentary between | Token overhead per turn | Queue all creates, execute in tight loop |
| Stopping the batch to ask user about individual items | Defeats batching purpose | Complete batch, report results, ask about failures |
