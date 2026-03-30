# drawio-plugin CLAUDE.md Integration

Add this snippet to your project's CLAUDE.md to enable drawio-plugin capabilities.

## When to Use This Plugin

Use `drawio-plugin` during the **design phase**, before running viz-platform scaffolding commands.

Typical workflow:
1. Create or receive a `.drawio` wireframe file
2. Run `/drawio parse` → produces `WIREFRAME.md`
3. Hand `WIREFRAME.md` to viz-platform → run `/viz component` or `/viz dashboard` to scaffold

## Integration Snippet

```markdown
## Wireframe Design (drawio-plugin)

This project uses drawio-plugin to parse draw.io wireframes into DMC component specs.

### Wireframe Location
Source: docs/design/{project-name}.drawio
Spec:   docs/design/WIREFRAME.md

### Available Commands
- `/drawio parse docs/design/{project-name}.drawio` — parse wireframe → WIREFRAME.md
- `/drawio generate "{description}"` — generate .drawio XML from UI description

### WIREFRAME.md Contract
WIREFRAME.md is the upstream input for viz-platform DMC scaffolding.
When scaffolding components, always read WIREFRAME.md first for:
- Component hierarchy and parent chain
- DMC domain files to load
- Implementation notes from the `instructions` attributes
```

## Commands Reference

| Command | Usage | Description |
|---|---|---|
| `/drawio parse` | `/drawio parse {file.drawio}` | Parse .drawio XML → WIREFRAME.md spec with DMC domain file declarations |
| `/drawio generate` | `/drawio generate "{description}" [--pages ...] [--output ...]` | Generate .drawio XML from UI description following layer conventions |

## Skills Loaded Per Command

| Command | Skills Loaded |
|---|---|
| `/drawio parse` | `drawio-conventions.md`, `wireframe-schema.md`, `dmc-domain-files.md` |
| `/drawio generate` | `drawio-conventions.md` |

## WIREFRAME.md Contract

`WIREFRAME.md` is produced by `/drawio parse` and consumed by `viz-platform`.

By convention, app project wireframes are stored in `docs/design/{project-name}.drawio`
and the generated `WIREFRAME.md` lands in the same directory (`docs/design/WIREFRAME.md`).
This folder is synced via Nextcloud and shared across all development environments.

The file contains:
- **DMC domain files required** — which reference files viz-platform should load
- **Shared layout** — AppShell, navbar component tree (written once, applies to all pages)
- **Per-page content** — component hierarchy for each route, with implementation notes

## Related Plugins

| Plugin | Relationship |
|---|---|
| `viz-platform` | Downstream consumer of WIREFRAME.md. Use viz-platform to scaffold DMC components after parsing. |
| `data-platform` | Unrelated — handles ETL and database operations, not UI design |
