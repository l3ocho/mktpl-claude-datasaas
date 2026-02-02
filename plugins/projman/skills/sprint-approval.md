---
name: sprint-approval
description: Approval gate logic for sprint execution
---

# Sprint Approval

## Purpose

Defines the approval workflow that gates sprint execution.

## When to Use

- **Planner agent**: After creating issues, request approval
- **Orchestrator agent**: Before execution, verify approval exists
- **Commands**: `/sprint-plan`, `/sprint-start`

---

## Core Principle

**Planning DOES NOT equal execution permission.**

Sprint approval is a mandatory checkpoint between planning and execution.

---

## Requesting Approval (Planner)

After creating issues, present approval request:

```
Sprint 17 Planning Complete
===========================

Created Issues:
- #45: [Sprint 17] feat: JWT token generation
- #46: [Sprint 17] feat: Login endpoint
- #47: [Sprint 17] test: Auth tests

Execution Scope:
- Branches: feat/45-*, feat/46-*, feat/47-*
- Files: auth/*, api/routes/auth.py, tests/test_auth*
- Dependencies: PyJWT, python-jose

⚠️ APPROVAL REQUIRED

Do you approve this sprint for execution?
This grants permission for agents to:
- Create and modify files in the listed scope
- Create branches with the listed prefixes
- Install listed dependencies

Type "approve sprint 17" to authorize execution.
```

---

## Recording Approval

On user approval, update milestone description:

```markdown
## Sprint Approval
**Approved:** 2026-01-28 14:30
**Approver:** User
**Scope:**
- Branches: feat/45-*, feat/46-*, feat/47-*
- Files: auth/*, api/routes/auth.py, tests/test_auth*
- Dependencies: PyJWT, python-jose
```

---

## Verifying Approval (Orchestrator)

Before execution, check milestone for approval:

```python
get_milestone(repo="org/repo", milestone_id=17)
# Check description for "## Sprint Approval" section
```

### If Approval Missing

```
🔴 SPRINT APPROVAL NOT FOUND — BLOCKED

Sprint 17 milestone does not contain an approval record.
Execution cannot proceed without approval.

Required: Run /sprint-plan first to:
1. Review the sprint scope
2. Get explicit approval for execution

To override (emergency only): /sprint-start --force
This bypasses the approval gate and logs a warning to the milestone.
```

### If Approval Found

```
✓ Sprint Approval Verified
  Approved: 2026-01-28 14:30
  Scope:
    Branches: feat/45-*, feat/46-*, feat/47-*
    Files: auth/*, api/routes/auth.py, tests/test_auth*

Proceeding with execution within approved scope...
```

---

## Scope Enforcement

When approval exists, agents SHOULD operate within approved scope:

```
Approved scope:
  Branches: feat/45-*, feat/46-*
  Files: auth/*, tests/test_auth*

Task #48 wants to create: feat/48-api-docs
→ NOT in approved scope!
→ STOP and ask user to approve expanded scope
```

**Operations outside scope should trigger re-approval via `/sprint-plan`.**

---

## Re-Approval Scenarios

Request re-approval when:
- New tasks discovered during execution
- Scope expansion needed (new files, new branches)
- Dependencies change significantly
- Timeline changes require scope adjustment

---

## Force Override

The `--force` flag bypasses the approval gate for emergency situations.

When `--force` is used:
1. Log a warning comment on the milestone: "⚠️ Sprint started without approval via --force on [date]"
2. Proceed with execution
3. The sprint close will flag this as an audit concern

**Do NOT use --force** as standard practice. If you find yourself using it regularly, the planning workflow needs adjustment.
