---
name: design accessibility
description: Run WCAG accessibility validation on the current theme and color combinations
skills:
  - skills/accessibility-rules/SKILL.md
---

# /design accessibility

Check WCAG contrast compliance for the current DMC theme.

## Steps

1. Load current theme from design contract or ask user to specify
2. Use `accessibility_validate_colors` MCP tool to check color pairs
3. Use `accessibility_validate_theme` MCP tool for theme-level audit
4. Report violations with WCAG level (AA/AAA) and specific fixes
5. Suggest accessible alternatives for failing combinations
