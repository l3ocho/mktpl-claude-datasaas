# drawio-plugin

**Version:** 1.2.0 | **Domain:** data | **License:** MIT

Wireframe design tools for draw.io — bridges the design phase (`.drawio` wireframes) and the
build phase (DMC component scaffolding via dmc-design). Parses draw.io XML into structured
`WIREFRAME.md` specs and generates draw.io XML from natural language UI descriptions.

## Purpose

dmc-design's DMC scaffolding commands have always needed an upstream input: a structured
description of what to build. `drawio-plugin` fills that gap. Design in draw.io → parse to
`WIREFRAME.md` → hand to dmc-design for scaffolding. The plugin also supports the reverse
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
| `wireframe-schema.md` | WIREFRAME.md output format — the contract between this plugin and dmc-design |
| `dmc-domain-files.md` | DMC file loading strategy — dynamic discovery of which reference files to declare |

## WIREFRAME.md Contract

`WIREFRAME.md` is the file produced by `/drawio parse` and consumed by `dmc-design`.

It captures:
- Which DMC domain reference files the session needs (discovered dynamically from `references/dmc/dmc-*.txt`)
- The shared layout component tree (AppShell, navbar and other regions) — written once
- Per-page component hierarchies with `component-instructions`, callback wiring, and data bindings

**Convention:** Wireframes live in `docs/design/{project-name}.drawio` and `WIREFRAME.md`
lands in the same directory. This folder syncs via Nextcloud across all environments.

**Consumer:** dmc-design reads `## DMC Domain Files Required` from `WIREFRAME.md` to decide
which reference files from `references/dmc/` to load before scaffolding DMC components.

## Related Plugins

| Plugin | Relationship |
|---|---|
| `dmc-design` | Downstream consumer — uses WIREFRAME.md as upstream input for DMC scaffolding |

## DMC Reference Files

Domain-specific DMC documentation is stored in `references/dmc/`.
Files follow the naming convention `dmc-*.txt` and are **AUTO-GENERATED** by
`scripts/generate-dmc-refs.py`. The set of files is not fixed — new domains
can be added by updating `DOMAIN_CATEGORY_MAP` in that script.

Current files (as of last generation):

| File | Contents |
|---|---|
| `dmc-layout.txt` | AppShell, Grid, Stack, Group, Container and related layout components |
| `dmc-ui.txt` | NavLink, Button, Text, Title, Paper, Card, Table, inputs and all UI components |
| `dmc-charts.txt` | DMC-native chart components (AreaChart, BarChart, etc.) |
| `dmc-feedback.txt` | Alert, Modal, Drawer, Notification, LoadingOverlay, Skeleton and feedback components |
| `dmc-theme.txt` | MantineProvider, theme configuration, createTheme |

These files are Leo's curated DMC reference documentation, split by domain to minimize
context size. dmc-design loads only the files relevant to the current project.

## Changelog

### v1.2.0
- Dynamic DMC domain file discovery: parser now lists `references/dmc/dmc-*.txt` instead
  of assuming a fixed file list. New domain files added by `generate-dmc-refs.py` are
  automatically picked up without plugin code changes.
- `skills/dmc-domain-files.md` — added "Domain Files Discovery" section with glob pattern
  and updated "How the Parser Uses This Skill" to reflect dynamic listing step.
- `skills/wireframe-schema.md` — "DMC Domain File Detection" section now documents the
  dynamic discovery step before applying component-to-file mapping rules.
- README updated to describe dynamic file set.

### v1.1.0
- `references/dmc/*.txt` files are now AUTO-GENERATED artifacts (was: hand-maintained stubs)
- `skills/dmc-domain-files.md` — added "Reference File Generation" section at top
- `references/dmc/README.md` — new file documenting generation process

### v1.0.0
- Initial release: `/drawio parse` and `/drawio generate` commands
- Three skills: drawio-conventions, wireframe-schema, dmc-domain-files
