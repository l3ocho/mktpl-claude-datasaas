# Layout Templates

## Available Templates

### Basic
Single-column layout with header and content area.
```
+-----------------------------+
|          Header             |
+-----------------------------+
|                             |
|          Content            |
|                             |
+-----------------------------+
```

### Sidebar
Layout with collapsible sidebar navigation.
```
+--------+--------------------+
|        |       Header       |
|  Nav   +--------------------+
|        |                    |
|        |      Content       |
|        |                    |
+--------+--------------------+
```

### Tabs
Tabbed layout for multi-page dashboards.
```
+-----------------------------+
|          Header             |
+------+------+------+--------+
| Tab1 | Tab2 | Tab3 |        |
+------+------+------+--------+
|                             |
|       Tab Content           |
|                             |
+-----------------------------+
```

### Split
Split-pane layout for comparisons.
```
+-----------------------------+
|          Header             |
+--------------+--------------+
|              |              |
|    Left      |    Right     |
|    Pane      |    Pane      |
|              |              |
+--------------+--------------+
```

## Filter Types

Available filter components:
- `dropdown` - Single/multi-select dropdown
- `date_range` - Date range picker
- `slider` - Numeric range slider
- `checkbox` - Checkbox group
- `search` - Text search input

## Output

Layout structures can be:
- Used with page tools to create full app
- Rendered as a Dash layout
- Combined with chart components
