---
name: drift-detection
description: Core drift detection rules, cross-reference analysis, and priority levels
---

# Drift Detection

## Purpose

Defines how to detect documentation drift through cross-reference analysis.

## When to Use

- **doc-audit**: Full cross-reference analysis
- **stale-docs**: Commit-based staleness detection
- **SessionStart hook**: Real-time drift detection

---

## Cross-Reference Analysis

For each documentation file:
1. Extract referenced functions, classes, endpoints, configs
2. Verify each reference exists in codebase
3. Check signatures/types match documentation
4. Flag deprecated or renamed items still in docs

---

## Drift Detection Rules

| Rule | Check | Priority |
|------|-------|----------|
| Version Mismatch | Hardcoded versions must match package.json, pyproject.toml, requirements.txt | P0 |
| Function References | Function names must exist with matching signatures | P0 |
| Path References | File paths must exist in directory structure | P0 |
| Config Keys | Env vars and config keys must be used in code | P1 |
| Command Examples | CLI examples must be valid commands | P1 |

---

## Priority Levels

| Level | Description | Action |
|-------|-------------|--------|
| **P0 (Critical)** | Broken references causing user errors | Immediate fix |
| **P1 (High)** | Outdated information misleading users | Fix in current session |
| **P2 (Medium)** | Missing documentation for public interfaces | Add to backlog |
| **P3 (Low)** | Style inconsistencies, minor wording | Optional |

---

## Drift Categories

### Critical (Broken References)
- Function/class renamed but docs not updated
- File moved/deleted but docs still reference old path
- API endpoint changed but docs show old URL

### Stale (Outdated Info)
- Version numbers not matching actual
- Configuration examples using deprecated keys
- Screenshots of old UI

### Missing (Undocumented)
- Public functions without docstrings
- New features not in README
- Environment variables used but not documented

---

## Documentation File Mapping

| Doc File | Related Code |
|----------|--------------|
| README.md | All files in same directory |
| API.md | src/api/**/* |
| CLAUDE.md | Configuration files, scripts |
| docs/module.md | src/module/**/* |
| Component.md | Component.tsx, Component.css |

---

## Output Format

```
## Documentation Drift Report

### Critical (Broken References)
- [ ] README.md:45 references `calculate_total()` - function renamed to `compute_total()`

### Stale (Outdated Info)
- [ ] CLAUDE.md:23 lists Python 3.9 - project uses 3.11

### Missing (Undocumented)
- [ ] api/handlers.py:`create_order()` - no docstring

### Summary
- Critical: X items
- Stale: X items
- Missing: X items
```
