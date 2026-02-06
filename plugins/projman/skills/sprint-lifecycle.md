---
name: sprint-lifecycle
description: Sprint lifecycle state machine using milestone labels
---

# Sprint Lifecycle

## Purpose

Defines the valid sprint lifecycle states and transitions, enforced via labels on the sprint milestone. Each projman command checks the current state before executing and updates it on completion.

## When to Use

- **All sprint commands**: Check state on entry, update on exit
- **Sprint status**: Display current lifecycle state

---

## State Machine

```
idle -> Sprint/Planning -> Sprint/Executing -> Sprint/Reviewing -> idle
         (sprint plan)    (sprint start)       (sprint review)    (sprint close)
```

## State Labels

| Label | Set By | Meaning |
|-------|--------|---------|
| *(no Sprint/* label)* | `/sprint close` or initial state | Idle - no active sprint phase |
| `Sprint/Planning` | `/sprint plan` | Planning in progress |
| `Sprint/Executing` | `/sprint start` | Execution in progress |
| `Sprint/Reviewing` | `/sprint review` | Code review in progress |

**Rule:** Only ONE `Sprint/*` label may exist on a milestone at a time. Setting a new one removes the previous one.

---

## State Transition Rules

| Command | Expected State | Sets State | On Wrong State |
|---------|---------------|------------|----------------|
| `/sprint plan` | idle (no Sprint/* label) | `Sprint/Planning` | Warn: "Sprint is in [state]. Run `/sprint close` first or use `--force` to re-plan." Allow with `--force`. |
| `/sprint start` | `Sprint/Planning` | `Sprint/Executing` | Warn: "Expected Sprint/Planning state but found [state]. Run `/sprint plan` first or use `--force`." Allow with `--force`. |
| `/sprint review` | `Sprint/Executing` | `Sprint/Reviewing` | Warn: "Expected Sprint/Executing state but found [state]." Allow with `--force`. |
| `/sprint close` | `Sprint/Reviewing` | Remove all Sprint/* labels (idle) | Warn: "Expected Sprint/Reviewing state but found [state]. Run `/sprint review` first or use `--force`." Allow with `--force`. |
| `/sprint status` | Any | No change (read-only) | Display current state in output. |

---

## Checking State (Protocol)

At command entry, before any other work:

1. Fetch the active milestone using `get_milestone`
2. Check milestone description for `**Sprint State:**` line
3. Compare against expected state for this command
4. If mismatch: display warning with guidance, STOP unless `--force` provided
5. If match: proceed and update state after command completes its primary work

**Implementation:** Use milestone description metadata. Add/update a line:
```
**Sprint State:** Sprint/Executing
```

This avoids needing actual Gitea labels on milestones (which may not be supported). Parse this line to check state, update it to set state.

---

## Setting State

After command completes successfully:

1. Fetch current milestone description
2. If `**Sprint State:**` line exists, replace it
3. If not, append it to the end of the description
4. Update milestone via `update_milestone`

**Format:** `**Sprint State:** <state>` where state is one of:
- `Sprint/Planning`
- `Sprint/Executing`
- `Sprint/Reviewing`
- (empty/removed for idle)

---

## Displaying State

In `/sprint status` output, include:

```
Sprint Phase: Executing (since 2026-02-01)
```

Parse the milestone description for the `**Sprint State:**` line and display it prominently.

---

## Edge Cases

- **No active milestone**: State is implicitly `idle`
- **Multiple milestones**: Use the open/active milestone. If multiple open, use the most recent.
- **Milestone has no state line**: Treat as `idle`
- **`--force` used**: Log to milestone: "Warning: Lifecycle state override: [command] forced from [actual] state on [date]"
