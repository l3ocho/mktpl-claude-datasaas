# Skill: dmc-domain-files

## When to Load

Load this skill when:
- Running `/drawio parse` — to determine which domain files to declare in `WIREFRAME.md`
- Running `/drawio generate` — to understand which component categories exist
- Answering questions about the DMC file loading strategy for viz-platform

---

## Overview

Leo's DMC reference documentation has been split into domain-specific files.
These files travel with `drawio-plugin` in `references/dmc/`.
viz-platform loads only the files relevant to the current project — reducing context size.

The `drawio parse` command detects which files are needed by scanning `component-class` attribute values.
This is declared in `WIREFRAME.md` under `## DMC Domain Files Required`.
viz-platform reads that declaration to know which files to load at session start.

---

## Domain Files Index

| File | Domain | Load When |
|---|---|---|
| `dmc-layout.txt` | Layout & shell components | **Always** — every DMC app uses AppShell, Grid, Stack, etc. |
| `dmc-ui.txt` | UI interaction components | **Always** — buttons, inputs, navigation, typography |
| `dmc-charts.txt` | Chart components | Only if chart components found in wireframe |
| `dmc-feedback.txt` | Feedback & overlay components | Only if feedback components found in wireframe |
| `dmc-theme.txt` | Theme configuration | Only if theme-related components found |

---

## Implementation Layer Order

Leo's app projects follow this implementation sequence. Each layer maps to specific DMC files:

| Layer | What Gets Built | DMC File(s) Needed |
|---|---|---|
| **1. Layout layer** | AppShell, AppShellNavbar, AppShellMain, Grid, Stack, Group, Container | `dmc-layout.txt` |
| **2. UI components layer** | NavLink, Button, Text, Title, Paper, Card, Badge, Anchor, ActionIcon, Select, TextInput, etc. | `dmc-ui.txt` |
| **3. Graph layer** | Plotly figures (AreaChart, BarChart, etc.) | Plotly — **no DMC file needed** (pure Plotly, not DMC) |
| **4. Callback layer** | Dash callbacks, Input/Output wiring | Pure Dash — **no DMC file needed** |

**Key insight:** Charts in Leo's projects are implemented with Plotly directly, not DMC chart components.
If a wireframe contains `AreaChart`, `BarChart`, etc., these refer to Plotly wrappers — `dmc-charts.txt`
covers only DMC-native chart components. When in doubt, check the `component` value:
- `dmc.AreaChart`, `AreaChart` (no prefix) in a DMC context → `dmc-charts.txt`
- `dcc.Graph` with Plotly figure → no DMC file needed

---

## Component → Domain File Mapping

### Always Load (dmc-layout.txt)

```
AppShell, AppShellNavbar, AppShellMain, AppShellHeader, AppShellFooter,
AppShellSection, AppShellAside,
Grid, GridCol,
Stack, Group, Center, Container, Flex,
SimpleGrid, Space, Divider,
ScrollArea, AspectRatio
```

### Always Load (dmc-ui.txt)

```
NavLink, Anchor, Breadcrumbs, Burger, Tabs, TabsList, TabsTab, TabsPanel,
Button, ActionIcon, CloseButton,
Text, Title, Code, Highlight, Mark, Blockquote,
Paper, Card, CardSection, Image, BackgroundImage, Avatar,
Badge, Indicator, ThemeIcon, ColorSwatch,
TextInput, PasswordInput, NumberInput, Textarea, Select, MultiSelect,
NativeSelect, Checkbox, Radio, RadioGroup, Switch, Slider, RangeSlider,
FileInput, Autocomplete, DateInput, DatePicker, DateTimePicker,
Table, TableThead, TableTbody, TableTr, TableTh, TableTd,
Tooltip, Popover, HoverCard, Menu, MenuItem,
List, ListItem, Timeline, TimelineItem,
Chip, ChipGroup, Kbd, Pill, PillGroup, PillsInput,
SegmentedControl, Rating, ColorInput, ColorPicker
```

### Conditional (dmc-charts.txt)

Load when any of these appear as `component-class` values:
```
AreaChart, BarChart, LineChart, DonutChart, PieChart,
RadarChart, SparklineChart, BubbleChart, ScatterChart,
CompositeChart
```

### Conditional (dmc-feedback.txt)

Load when any of these appear as `component-class` values:
```
Alert, Modal, ModalHeader, ModalBody, ModalFooter,
Drawer, DrawerHeader, DrawerBody, DrawerFooter,
Notification, NotificationProvider,
LoadingOverlay, Skeleton, Loader,
Progress, RingProgress, Progress,
Stepper, StepperStep
```

### Conditional (dmc-theme.txt)

Load when any of these appear as `component-class` values, or when theme configuration is mentioned
in `component-instructions` attributes:
```
MantineProvider, ColorSchemeScript,
theme, createTheme, mantineTheme
```

---

## How the Parser Uses This Skill

1. After extracting all `component-class` values from the `.drawio` XML
2. Run against each mapping above
3. Build the `## DMC Domain Files Required` section in `WIREFRAME.md`
4. Always include `dmc-layout.txt` and `dmc-ui.txt` — never omit them

## How viz-platform Uses This

When viz-platform receives a `WIREFRAME.md`, it reads `## DMC Domain Files Required`
and uses the Skill tool (or direct Read) to load only the listed files from
`plugins/drawio-plugin/references/dmc/` before scaffolding components.
