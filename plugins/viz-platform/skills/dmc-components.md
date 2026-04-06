# Dash Mantine Components Reference

## Registry Generation

The component registry backing the viz-platform MCP tools (`validate_component`,
`get_component_props`, `list_components`) is **AUTO-GENERATED**. Do not edit the
registry JSON files manually.

To regenerate for a consumer project:
```bash
python scripts/generate-dmc-refs.py --project /path/to/consumer-project
```

Consumer projects declare which components they use in `.claude/dmc-components.json`.
See `docs/CONFIGURATION.md` under "DMC Reference Generation" for the schema.

---

## Component Categories

| Category | Components |
|----------|------------|
| `inputs` | Button, TextInput, Select, Checkbox, Radio, Switch, Slider, etc. |
| `navigation` | NavLink, Tabs, Breadcrumbs, Pagination, Stepper |
| `feedback` | Alert, Notification, Progress, Loader, Skeleton |
| `overlays` | Modal, Drawer, Tooltip, Popover, Menu |
| `typography` | Text, Title, Code, Blockquote, List |
| `layout` | Container, Grid, Stack, Group, Space, Divider |
| `data` | Table, Badge, Card, Paper, Timeline |

## Common Props

Most components share these props:

| Prop | Type | Description |
|------|------|-------------|
| `size` | xs, sm, md, lg, xl | Component size |
| `radius` | xs, sm, md, lg, xl | Border radius |
| `color` | string | Theme color name |
| `variant` | string | Style variant |
| `disabled` | boolean | Disable interaction |

## Component Validation

Why validation matters:
- Prevents hallucinated prop names
- Validates enum values
- Catches typos before runtime
- Documents available options

### Validation Response

```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

With errors:
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

## Grid System

DMC Grid with responsive spans:

```python
dmc.Grid(
    children=[
        dmc.GridCol(
            children=[chart],
            span={"base": 12, "sm": 6, "lg": 4}
        )
    ],
    gutter="md"
)
```

## Button Example

```json
{
  "component": "Button",
  "props": {
    "variant": {
      "type": "string",
      "enum": ["filled", "outline", "light", "subtle", "default", "gradient"],
      "default": "filled"
    },
    "color": {
      "type": "string",
      "default": "blue"
    },
    "size": {
      "type": "string",
      "enum": ["xs", "sm", "md", "lg", "xl"],
      "default": "sm"
    }
  }
}
```
