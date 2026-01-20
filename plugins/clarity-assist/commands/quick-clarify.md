# /quick-clarify - Rapid Clarification Mode

## Purpose

Single-pass clarification for requests that are mostly clear but need minor disambiguation.

## When to Use

- Request is fairly clear, just one or two ambiguities
- User is in a hurry
- Follow-up to an already-clarified request
- Simple feature additions or bug fixes

## Process

### Step 1: Echo Understanding

Restate what you understood in a single sentence:

```
"I understand you want [X] that does [Y]."
```

### Step 2: Quick Disambiguation

If needed, ask ONE multiple-choice question:

```
**Just to confirm:** Should this [A] or [B]?
1. [Option A with brief description]
2. [Option B with brief description]
3. Both
4. Neither / Other approach
```

### Step 3: Proceed or Confirm

If confident (>90%), proceed with a brief confirmation:

```
"Got it. I'll implement [X with chosen option]. Starting now."
```

If less confident, offer a micro-summary:

```
"Quick summary before I start:
- [Key point 1]
- [Key point 2]
- [Assumption made]

Proceed? (Or clarify anything)"
```

## Example Interaction

**User:** Add a delete button to the user list

**Quick-Clarify Response:**

```
I'll add a delete button to each row in the user list.

**Should deletion require confirmation?**
1. Yes - show confirmation dialog (Recommended)
2. No - delete immediately
3. Soft delete - mark as deleted but keep data

[Asking because accidental deletions can be problematic]
```

## Escalation to Full /clarify

If quick-clarify reveals complexity:

```
"This is more involved than it first appeared - there are
several decisions to make. Want me to switch to a more
thorough clarification process? (Just say 'yes' or 'clarify')"
```

## Output Format

For quick-clarify, no formal specification document is needed. Just proceed with the task after brief confirmation, documenting assumptions inline with the work.
