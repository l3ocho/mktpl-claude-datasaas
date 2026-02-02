---
description: Design system compliance gate (pass/fail) for sprint execution
arguments:
  - name: path
    description: File or directory to validate
    required: true
---

# /design-gate

Binary pass/fail validation for design system compliance. Used by projman orchestrator during sprint execution to gate issue completion.

## Usage

```
/design-gate <path>
```

**Examples:**
```
/design-gate ./app/pages/dashboard.py
/design-gate ./app/components/
```

## What It Does

1. **Activates** the `design-reviewer` agent in gate mode
2. **Loads** the `skills/design-system-audit.md` skill
3. **Scans** target path for DMC usage
4. **Checks only for FAIL-level violations:**
   - Invalid component props
   - Non-existent components
   - Missing required props
   - Deprecated components
5. **Returns binary result:**
   - `PASS` - No blocking violations found
   - `FAIL` - One or more blocking violations

## Output

### On PASS
```
DESIGN GATE: PASS
No blocking design system violations found.
```

### On FAIL
```
DESIGN GATE: FAIL

Blocking Issues (2):
1. app/pages/home.py:45 - Invalid prop 'onclick' on dmc.Button
   Fix: Use 'n_clicks' for click handling

2. app/components/nav.py:12 - Component 'dmc.Navbar' not found
   Fix: Use 'dmc.AppShell.Navbar' (DMC v0.14+)

Run /design-review for full audit report.
```

## Integration with projman

This command is automatically invoked by the projman orchestrator when:

1. An issue has the `Domain/Viz` label
2. The orchestrator is about to mark the issue as complete
3. The orchestrator passes the path of changed files

**Gate behavior:**
- PASS → Issue can be marked complete
- FAIL → Issue stays open, blocker comment added

## Differences from /design-review

| Aspect | /design-gate | /design-review |
|--------|--------------|----------------|
| Output | Binary PASS/FAIL | Detailed report |
| Severity | FAIL only | FAIL + WARN + INFO |
| Purpose | Automation gate | Human review |
| Verbosity | Minimal | Comprehensive |

## When to Use

- **Automated pipelines**: CI/CD design system checks
- **Sprint execution**: Automatic quality gates
- **Quick validation**: Fast pass/fail without full report

For detailed findings, use `/design-review` instead.

## Requirements

- viz-platform MCP server must be running
- Target path must exist
