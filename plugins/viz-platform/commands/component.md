---
description: Inspect Dash Mantine Component props and validation
---

# Inspect Component

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 VIZ-PLATFORM · Component Inspector                            │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the inspection.

Inspect a Dash Mantine Component's available props, types, and defaults.

## Usage

```
/component {name}
```

## Arguments

- `name` (required): DMC component name (e.g., Button, Card, TextInput)

## Examples

```
/component Button
/component TextInput
/component Select
/component Card
```

## Tool Mapping

This command uses the `get_component_props` MCP tool:

```python
get_component_props(component="Button")
```

## Output Example

```json
{
  "component": "Button",
  "category": "inputs",
  "props": {
    "children": {
      "type": "any",
      "required": false,
      "description": "Button content"
    },
    "variant": {
      "type": "string",
      "enum": ["filled", "outline", "light", "subtle", "default", "gradient"],
      "default": "filled",
      "description": "Button appearance variant"
    },
    "color": {
      "type": "string",
      "default": "blue",
      "description": "Button color from theme"
    },
    "size": {
      "type": "string",
      "enum": ["xs", "sm", "md", "lg", "xl"],
      "default": "sm",
      "description": "Button size"
    },
    "radius": {
      "type": "string",
      "enum": ["xs", "sm", "md", "lg", "xl"],
      "default": "sm",
      "description": "Border radius"
    },
    "disabled": {
      "type": "boolean",
      "default": false,
      "description": "Disable button"
    },
    "loading": {
      "type": "boolean",
      "default": false,
      "description": "Show loading indicator"
    },
    "fullWidth": {
      "type": "boolean",
      "default": false,
      "description": "Button takes full width"
    }
  }
}
```

## Listing All Components

To see all available components:

```python
list_components(category=None)  # All components
list_components(category="inputs")  # Just input components
```

### Component Categories

| Category | Components |
|----------|------------|
| `inputs` | Button, TextInput, Select, Checkbox, Radio, Switch, Slider, etc. |
| `navigation` | NavLink, Tabs, Breadcrumbs, Pagination, Stepper |
| `feedback` | Alert, Notification, Progress, Loader, Skeleton |
| `overlays` | Modal, Drawer, Tooltip, Popover, Menu |
| `typography` | Text, Title, Code, Blockquote, List |
| `layout` | Container, Grid, Stack, Group, Space, Divider |
| `data` | Table, Badge, Card, Paper, Timeline |

## Validating Component Usage

After inspecting props, validate your usage:

```python
validate_component(
    component="Button",
    props={
        "variant": "filled",
        "color": "blue",
        "size": "lg",
        "children": "Click me"
    }
)
```

Returns:
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

Or with errors:
```json
{
  "valid": false,
  "errors": [
    "Invalid prop 'colour' for Button. Did you mean 'color'?",
    "Prop 'size' expects one of ['xs', 'sm', 'md', 'lg', 'xl'], got 'huge'"
  ],
  "warnings": [
    "Prop 'fullwidth' should be 'fullWidth' (camelCase)"
  ]
}
```

## Why This Matters

DMC components have many props with specific type constraints. This tool:
- Prevents hallucinated prop names
- Validates enum values
- Catches typos before runtime
- Documents available options

## Related Commands

- `/chart {type}` - Create charts
- `/dashboard {template}` - Create layouts
