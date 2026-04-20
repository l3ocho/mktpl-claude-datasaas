---
name: doc audit
description: [doc-guardian] Full documentation audit - scans entire project for doc drift without making changes
---

# /doc audit

Perform a comprehensive documentation drift analysis.

## Skills to Load

- skills/drift-detection/SKILL.md
- skills/doc-patterns/SKILL.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Documentation Audit                              |
+------------------------------------------------------------------+
```

## Process

1. **Inventory Documentation Files**
   Execute `skills/doc-patterns/SKILL.md` - identify all doc files

2. **Cross-Reference Analysis**
   Execute `skills/drift-detection/SKILL.md` - verify all references

3. **Completeness Check**
   - Public functions without docstrings
   - Exported modules without README coverage
   - Environment variables used but not documented
   - CLI commands not in help text

4. **Output**
   Use format from `skills/drift-detection/SKILL.md`

5. **Do NOT make changes** - audit only, report findings
