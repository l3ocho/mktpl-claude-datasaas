---
name: dash dashboard
description: Create a dashboard layout with the layout-builder agent
---

# /dash dashboard

Create a dashboard layout with filters, grids, and sections.

## Usage

```
/dash dashboard {template}
```

## Arguments

- `template` (optional): basic, sidebar, tabs, split

## Agent Mapping

Activates **layout-builder** agent which orchestrates:
- `layout_create` - Create base layout structure
- `layout_add_filter` - Add filter components
- `layout_set_grid` - Configure responsive grid

## Related Commands

- `/viz breakpoints {layout}` - Configure responsive breakpoints
- `/viz chart {type}` - Add charts to layout
