# drawio-plugin

**Version:** 1.0.0 | **Domain:** data | **License:** MIT

Wireframe design tools for draw.io — bridges the design phase (`.drawio` wireframes) and the
build phase (DMC component scaffolding via viz-platform). Parses draw.io XML into structured
`WIREFRAME.md` specs and generates draw.io XML from natural language UI descriptions.

## Purpose

viz-platform's DMC scaffolding commands have always needed an upstream input: a structured
description of what to build. `drawio-plugin` fills that gap. Design in draw.io → parse to
`WIREFRAME.md` → hand to viz-platform for scaffolding. The plugin also supports the reverse
direction: generate a `.drawio` wireframe from a description when no design file exists yet.

## Commands

| Command | Usage | Description |
|---|---|---|
| `/drawio parse` | `/drawio parse {file.drawio}` | Parse .drawio XML → WIREFRAME.md spec + DMC domain file declarations |
| `/drawio generate` | `/drawio generate "{description}"` | Generate .drawio XML from UI description following DMC layer conventions |

## Skills

| Skill | Purpose |
|---|---|
| `drawio-conventions.md` | Core XML structure spec — layer naming, object attributes, parent chain rules, worked example |
| `wireframe-schema.md` | WIREFRAME.md output format — the contract between this plugin and viz-platform |
| `dmc-domain-files.md` | DMC file loading strategy — which reference files to declare per implementation layer |

## WIREFRAME.md Contract

`WIREFRAME.md` is the file produced by `/drawio parse` and consumed by `viz-platform`.

It captures:
- Which DMC domain reference files the session needs
- The shared layout component tree (AppShell, navbar and other regions) — written once
- Per-page component hierarchies with `component-instructions`, callback wiring, and data bindings

**Convention:** Wireframes live in `docs/design/{project-name}.drawio` and `WIREFRAME.md`
lands in the same directory. This folder syncs via Nextcloud across all environments.

**Consumer:** viz-platform reads `## DMC Domain Files Required` from `WIREFRAME.md` to decide
which reference files from `references/dmc/` to load before scaffolding DMC components.

## Related Plugins

| Plugin | Relationship |
|---|---|
| `viz-platform` | Downstream consumer — uses WIREFRAME.md as upstream input for DMC scaffolding |

## DMC Reference Files

Domain-specific DMC documentation is stored in `references/dmc/`:

| File | Contents |
|---|---|
| `dmc-layout.txt` | AppShell, Grid, Stack, Group, Container and related layout components |
| `dmc-ui.txt` | NavLink, Button, Text, Title, Paper, Card, Table, inputs and all UI components |
| `dmc-charts.txt` | DMC-native chart components (AreaChart, BarChart, etc.) |
| `dmc-feedback.txt` | Alert, Modal, Drawer, Notification, LoadingOverlay, Skeleton and feedback components |
| `dmc-theme.txt` | MantineProvider, theme configuration, createTheme |

These files are Leo's curated DMC reference documentation, split by domain to minimize
context size. viz-platform loads only the files relevant to the current project.
