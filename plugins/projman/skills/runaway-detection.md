---
name: runaway-detection
description: Detecting and handling stuck agents
---

# Runaway Detection

## Purpose

Defines how to detect stuck agents and intervention protocols.

## When to Use

- **Orchestrator agent**: When monitoring dispatched agents
- **Executor agent**: Self-monitoring during execution

---

## Warning Signs

| Sign | Threshold | Action |
|------|-----------|--------|
| No progress comment | 30+ minutes | Investigate |
| Same phase repeated | 20+ tool calls | Consider stopping |
| Same error 3+ times | Immediately | Stop agent |
| Approaching budget | 80% of limit | Post checkpoint |

---

## Agent Timeout Guidelines

| Task Size | Expected Duration | Intervention Point |
|-----------|-------------------|-------------------|
| XS | ~5-10 min | 15 min no progress |
| S | ~10-20 min | 30 min no progress |
| M | ~20-40 min | 45 min no progress |

---

## Detection Protocol

1. **Read latest progress comment** - Check tool call count and phase
2. **Compare to previous** - Is progress happening?
3. **Check for error patterns** - Same error repeating?
4. **Evaluate time elapsed** - Beyond expected duration?

---

## Intervention Protocol

When you detect an agent may be stuck:

### Step 1: Assess

```
Agent Status Check for #45:
- Last progress: 25 minutes ago
- Phase: "Testing" (same as 20 tool calls ago)
- Errors: "ModuleNotFoundError" (3 times)
- Assessment: LIKELY STUCK
```

### Step 2: Stop Agent

```python
# If TaskStop available
TaskStop(task_id="agent-id")
```

### Step 3: Update Issue Status

```python
update_issue(
    repo="org/repo",
    issue_number=45,
    labels=["Status/Failed", ...other_labels]
)
```

### Step 4: Add Explanation Comment

```python
add_comment(
    repo="org/repo",
    number=45,
    body="""## Agent Intervention
**Reason:** No progress detected for 25 minutes / repeated errors
**Last Status:** Testing phase, ModuleNotFoundError x3
**Action:** Stopped agent, requires human review

### What Was Completed
- [x] Created auth/jwt_service.py
- [x] Implemented generate_token()

### What Remains
- [ ] Fix import issue
- [ ] Write tests
- [ ] Commit

### Recommendation
- Check for missing dependency in requirements.txt
- May need manual intervention to resolve import
"""
)
```

---

## Self-Monitoring (Executor)

Executors should self-monitor:

### Circuit Breakers

- **Same error 3 times**: Stop and report
- **80% of tool call budget**: Post checkpoint
- **File not found 3 times**: Stop and ask for help
- **Test failing same way 5 times**: Stop and report

### Self-Check Template

```
Self-check at tool call 45/100:
- Progress: 4/7 steps completed
- Current phase: Testing
- Errors encountered: 1 (resolved)
- Remaining budget: 55 calls
- Status: ON TRACK
```

---

## Recovery Actions

After stopping a stuck agent:

1. **Preserve work** - Branch and commits remain
2. **Document state** - Checkpoint in issue comment
3. **Identify cause** - What caused the loop?
4. **Plan recovery**:
   - Manual completion
   - Different approach
   - Break down further
   - Assign to human

---

## Common Stuck Patterns

| Pattern | Cause | Solution |
|---------|-------|----------|
| Import loop | Missing dependency | Add to requirements |
| Test loop | Non-deterministic test | Fix test isolation |
| Validation loop | Error message not changing | Improve error specificity |
| File not found | Wrong path | Verify path exists |
| Permission denied | File ownership | Check permissions |
