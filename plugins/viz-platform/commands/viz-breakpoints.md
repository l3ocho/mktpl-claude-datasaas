---
name: viz breakpoints
description: Configure responsive breakpoints for dashboard layouts
---

# /viz breakpoints

## Skills to Load
- skills/mcp-tools-reference.md
- skills/responsive-design.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Breakpoints                                      |
+------------------------------------------------------------------+
```

Configure responsive breakpoints for mobile-first design across screen sizes.

## Usage

```
/viz breakpoints {layout_ref}
```

## Arguments

- `layout_ref` (required): Layout name to configure breakpoints for

## Workflow

1. **User invokes**: `/viz breakpoints my-dashboard`
2. **Agent asks**: Which breakpoints to customize? (shows current settings)
3. **Agent asks**: Mobile column count? (xs, typically 1-2)
4. **Agent asks**: Tablet column count? (md, typically 4-6)
5. **Agent applies**: Breakpoint configuration via `layout_set_breakpoints`
6. **Agent returns**: Complete responsive configuration

## Related Commands

- `/viz dashboard {template}` - Create layout with default breakpoints
- `/viz theme {name}` - Theme includes default spacing values
