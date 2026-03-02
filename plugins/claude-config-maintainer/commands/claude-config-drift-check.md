---
name: claude-config drift-check
description: Detect permission drift between baseline and current settings
---

# /claude-config drift-check

Compare current `settings.local.json` against the saved baseline in `settings.json` to detect session-approval drift and permission degradation.

## Skills to Load

Before executing, load:
- `skills/visual-header.md`
- `skills/settings-optimization.md`

## Visual Output

```
+-----------------------------------------------------------------+
|  CONFIG-MAINTAINER - Permission Drift Check                      |
+-----------------------------------------------------------------+
```

## Usage

```
/claude-config drift-check                 # Check for drift, report findings
/claude-config drift-check --fix           # Check and offer to restore baseline
```

## Workflow

### Step 1: Load Both Files

Read `.claude/settings.json` (baseline) and `.claude/settings.local.json` (current).

If no baseline exists:
```
No baseline found in .claude/settings.json.

Run `/claude-config baseline save` first to establish a baseline,
then use drift-check to monitor changes over time.
```

### Step 2: Compute Drift Metrics

| Metric | Calculation |
|--------|------------|
| Redundant patterns | Patterns in local that duplicate baseline patterns |
| Session additions | Patterns in local not in baseline (accumulated approvals) |
| Baseline coverage | % of local patterns already covered by baseline |
| Drift score | 0 (no drift) to 100 (severe drift) |

### Step 3: Classify Session Additions

For each pattern in local but not in baseline:

| Classification | Detection | Action |
|---------------|-----------|--------|
| **Redundant** | Exact match or subset of baseline pattern | Safe to remove |
| **Machine-specific** | Contains absolute paths, user-specific dirs | Keep in local |
| **Session drift** | Generic patterns that should be in baseline | Suggest adding to baseline |
| **Compound command** | Contains `&&`, `\|\|`, `;`, `\|` | Flag as compound command gap |

### Step 4: Report

```
Permission Drift Report
========================

Baseline: .claude/settings.json (XX patterns, last modified YYYY-MM-DD)
Current:  .claude/settings.local.json (YY patterns)

Drift Score: 35/100 (moderate drift)

  Redundant patterns (safe to remove):      8
  Session-accumulated approvals:             12
  Machine-specific (keep):                   2
  Compound command gaps:                     3

Session Additions Breakdown:
  Bash(cd /home/leo/projects/portfolio && python app.py)  → compound command gap
  Bash(grep -r "foo" . | wc -l)                          → compound command gap
  Write(/home/leo/.local/share/*)                         → machine-specific
  Bash(pip install requests)                              → session drift
  ...

Recommendations:
  1. Run `/claude-config baseline restore` to remove 8 redundant patterns
  2. Consider adding 3 compound patterns to baseline (see Section 9 of settings-optimization skill)
  3. Review 12 session additions — promote useful ones to baseline with `/claude-config baseline save`
```

### Step 5: Auto-Fix (--fix flag)

If `--fix` is provided:
1. Remove redundant patterns from `settings.local.json`
2. Ask about session drift patterns: promote to baseline or discard?
3. Flag compound command gaps with recommended patterns
4. Leave machine-specific patterns untouched
5. Backup before any changes

## Drift Score Interpretation

| Score | Status | Meaning |
|-------|--------|---------|
| 0-10 | Clean | Minimal drift, baseline is effective |
| 11-30 | Low | Some session additions, periodic cleanup recommended |
| 31-60 | Moderate | Significant drift, approval prompts likely increasing |
| 61-100 | Severe | Baseline is ineffective, needs restore + re-optimization |

## DO NOT

- Modify settings.json during drift-check (that's baseline save's job)
- Remove machine-specific patterns without asking
- Skip the backup before --fix modifications
