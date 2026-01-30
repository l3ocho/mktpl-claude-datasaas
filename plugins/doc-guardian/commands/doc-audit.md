---
description: Full documentation audit - scans entire project for doc drift without making changes
---

# Documentation Audit

Perform a comprehensive documentation drift analysis.

## Skills to Load

- skills/drift-detection.md
- skills/doc-patterns.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Documentation Audit                              |
+------------------------------------------------------------------+
```

## Process

1. **Inventory Documentation Files**
   Execute `skills/doc-patterns.md` - identify all doc files

2. **Cross-Reference Analysis**
   Execute `skills/drift-detection.md` - verify all references

3. **Completeness Check**
   - Public functions without docstrings
   - Exported modules without README coverage
   - Environment variables used but not documented
   - CLI commands not in help text

4. **Output**
   Use format from `skills/drift-detection.md`

5. **Do NOT make changes** - audit only, report findings
