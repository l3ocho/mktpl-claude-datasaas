---
description: Create a dashboard layout with the layout-builder agent
---

# Create Dashboard

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 VIZ-PLATFORM · Dashboard Builder                              │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the dashboard creation.

Create a dashboard layout structure with filters, grids, and sections.

## Usage

```
/dashboard {template}
```

## Arguments

- `template` (optional): Layout template - one of: basic, sidebar, tabs, split

## Examples

```
/dashboard              # Interactive layout builder
/dashboard basic        # Simple single-column layout
/dashboard sidebar      # Layout with sidebar navigation
/dashboard tabs         # Tabbed multi-page layout
/dashboard split        # Split-pane layout
```

## Agent Mapping

This command activates the **layout-builder** agent which orchestrates multiple tools:

1. `layout_create` - Create the base layout structure
2. `layout_add_filter` - Add filter components (dropdowns, date pickers)
3. `layout_set_grid` - Configure responsive grid settings
4. `layout_add_section` - Add content sections

## Workflow

1. **User invokes**: `/dashboard sidebar`
2. **Agent asks**: What is the dashboard purpose?
3. **Agent asks**: What filters are needed?
4. **Agent creates**: Base layout with `layout_create`
5. **Agent adds**: Filters with `layout_add_filter`
6. **Agent configures**: Grid with `layout_set_grid`
7. **Agent returns**: Complete layout structure

## Templates

### Basic
Single-column layout with header and content area.
```
┌─────────────────────────────┐
│          Header             │
├─────────────────────────────┤
│                             │
│          Content            │
│                             │
└─────────────────────────────┘
```

### Sidebar
Layout with collapsible sidebar navigation.
```
┌────────┬────────────────────┐
│        │       Header       │
│  Nav   ├────────────────────┤
│        │                    │
│        │      Content       │
│        │                    │
└────────┴────────────────────┘
```

### Tabs
Tabbed layout for multi-page dashboards.
```
┌─────────────────────────────┐
│          Header             │
├──────┬──────┬──────┬────────┤
│ Tab1 │ Tab2 │ Tab3 │        │
├──────┴──────┴──────┴────────┤
│                             │
│       Tab Content           │
│                             │
└─────────────────────────────┘
```

### Split
Split-pane layout for comparisons.
```
┌─────────────────────────────┐
│          Header             │
├──────────────┬──────────────┤
│              │              │
│    Left      │    Right     │
│    Pane      │    Pane      │
│              │              │
└──────────────┴──────────────┘
```

## Filter Types

Available filter components:
- `dropdown` - Single/multi-select dropdown
- `date_range` - Date range picker
- `slider` - Numeric range slider
- `checkbox` - Checkbox group
- `search` - Text search input

## Output

Returns a layout structure that can be:
- Used with page tools to create full app
- Rendered as a Dash layout
- Combined with chart components
