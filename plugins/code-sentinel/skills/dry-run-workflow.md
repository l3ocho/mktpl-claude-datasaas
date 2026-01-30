---
description: Workflow for previewing changes safely before applying them
---

# Dry Run Workflow Skill

## Overview

Dry run mode analyzes code and shows proposed changes without modifying files. Essential for reviewing impact before committing to changes.

## Opportunity Scoring

Rate each refactoring opportunity on three dimensions:

### Impact Score (1-5)
| Score | Meaning | Example |
|-------|---------|---------|
| 5 | Major improvement | Cyclomatic complexity 15 -> 3 |
| 4 | Significant improvement | Function 50 lines -> 15 lines |
| 3 | Moderate improvement | Better naming, clearer structure |
| 2 | Minor improvement | Code style modernization |
| 1 | Cosmetic only | Formatting changes |

### Risk Score (1-5)
| Score | Meaning | Example |
|-------|---------|---------|
| 5 | Very high risk | Changes to core business logic |
| 4 | High risk | Modifies shared utilities |
| 3 | Moderate risk | Changes function signatures |
| 2 | Low risk | Internal implementation only |
| 1 | Minimal risk | Pure functions, no side effects |

### Effort Score (1-5)
| Score | Meaning | Example |
|-------|---------|---------|
| 5 | Major effort | Requires architecture changes |
| 4 | Significant effort | Many files affected |
| 3 | Moderate effort | Multiple related changes |
| 2 | Low effort | Single file, clear scope |
| 1 | Trivial | Automated transformation |

## Priority Calculation

```
Priority = (Impact * 2) - Risk - (Effort * 0.5)
```

| Priority Range | Recommendation |
|---------------|----------------|
| > 5 | Recommended - do it |
| 3-5 | Optional - consider it |
| < 3 | Skip - not worth it |

## Output Format

### Recommended Section
High impact, low risk opportunities:
```
1. **pattern-name** at file:lines
   - Description of the change
   - Impact: High/Medium/Low (specific metric improvement)
   - Risk: Low/Medium/High (why)
   - Run: `/refactor <target> --pattern=<pattern>`
```

### Optional Section
Lower priority opportunities grouped by type.

### Summary
- Count of recommended vs optional
- Estimated overall improvement percentage
- Any blockers or dependencies

## Dependency Detection

Before recommending changes, check for:

1. **Test Coverage** - Does this code have tests?
2. **Usage Scope** - Is it used elsewhere?
3. **Side Effects** - Does it modify external state?
4. **Breaking Changes** - Will it change public API?

Flag dependencies in output:
```
Note: This refactoring requires updating 3 callers:
  - src/api/handlers.py:45
  - src/cli/commands.py:78
  - tests/test_handlers.py:23
```

## Safety Checklist

Before recommending any change:

- [ ] All affected code locations identified
- [ ] No breaking API changes without flag
- [ ] Test coverage assessed
- [ ] Side effects documented
- [ ] Rollback path clear (git)
