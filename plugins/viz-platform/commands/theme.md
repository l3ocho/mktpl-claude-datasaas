---
description: Apply an existing theme to the current context
---

# Apply Theme

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  🎨 VIZ-PLATFORM · Apply Theme                                    │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the theme activation.

Apply an existing theme to activate its design tokens.

## Usage

```
/theme {name}
```

## Arguments

- `name` (required): Theme name to activate

## Examples

```
/theme dark
/theme corporate-blue
/theme my-custom-theme
```

## Tool Mapping

This command uses the `theme_activate` MCP tool:

```python
theme_activate(theme_name="dark")
```

## Workflow

1. **User invokes**: `/theme dark`
2. **Tool activates**: Theme becomes active for subsequent operations
3. **Charts/layouts**: Automatically use active theme tokens

## Built-in Themes

| Theme | Description |
|-------|-------------|
| `light` | Mantine default light mode |
| `dark` | Mantine default dark mode |

## Listing Available Themes

To see all available themes:

```python
theme_list()
```

Returns both built-in and custom themes.

## Theme Effects

When a theme is activated:
- New charts inherit theme colors
- New layouts use theme spacing
- Components use theme typography
- Callbacks can read active theme tokens

## Related Commands

- `/theme-new {name}` - Create a new theme
- `/theme-css {name}` - Export theme as CSS
