---
description: Inspect Dash Mantine Component props and validation
---

# Inspect Component

## Skills to Load
- skills/mcp-tools-reference.md
- skills/dmc-components.md

## Visual Output

```
+------------------------------------------------------------------+
|  VIZ-PLATFORM - Component Inspector                              |
+------------------------------------------------------------------+
```

Inspect a DMC component's props, types, and defaults.

## Usage

```
/component {name}
```

## Arguments

- `name` (required): DMC component name (e.g., Button, Card, TextInput)

## Tool Mapping

```python
get_component_props(component="Button")
list_components(category="inputs")
validate_component(component="Button", props={"variant": "filled"})
```

## Related Commands

- `/chart {type}` - Create charts
- `/dashboard {template}` - Create layouts
