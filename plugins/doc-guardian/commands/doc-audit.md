---
description: Full documentation audit - scans entire project for doc drift without making changes
---

# Documentation Audit

Perform a comprehensive documentation drift analysis.

## Process

1. **Inventory Documentation Files**
   - README.md (root and subdirectories)
   - CLAUDE.md
   - API documentation
   - Docstrings in code files
   - Configuration references

2. **Cross-Reference Analysis**
   For each documentation file:
   - Extract referenced functions, classes, endpoints, configs
   - Verify each reference exists in codebase
   - Check signatures/types match documentation
   - Flag deprecated or renamed items still in docs

3. **Completeness Check**
   - Public functions without docstrings
   - Exported modules without README coverage
   - Environment variables used but not documented
   - CLI commands not in help text

4. **Output Format**
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

5. **Do NOT make changes** - audit only, report findings
