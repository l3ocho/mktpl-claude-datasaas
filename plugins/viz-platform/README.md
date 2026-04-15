# viz-platform

Visualization tools for Dash Mantine Components (DMC) dashboards — component validation, Plotly charts, theming, and layout scaffolding.

**Version:** 9.4.0

---

## Commands

| Command | Description |
|---------|-------------|
| `/viz component {name}` | Inspect DMC component props |
| `/viz chart {type}` | Create Plotly charts |
| `/viz dashboard {template}` | Scaffold a layout (basic, sidebar, tabs, split) |
| `/viz theme {name}` | Apply a named theme |
| `/viz theme-new {name}` | Create a custom theme |
| `/viz theme-css {name}` | Export theme as CSS custom properties |
| `/viz design-review <path>` | Full design system audit with FAIL/WARN/INFO findings |
| `/viz design-gate <path>` | Binary PASS/FAIL design gate for CI/sprint automation |
| `/viz accessibility-check` | WCAG color contrast and accessibility audit |
| `/viz breakpoints` | Configure responsive breakpoints |

---

## Agents

### component-check
DMC component validation specialist. Validates props before rendering — catches typos, invalid enum values, wrong case, and React-vs-Dash prop patterns.

**Dual-scheme behavior:** Automatically detects dual-scheme CSS support. When detected, applies color scheme integrity checks (Rules 1, 2, 3, 4) alongside standard component validation.

### design-reviewer
Design system compliance auditor. Reviews code for proper DMC usage, theme tokens, and accessibility standards.

**Dual-scheme behavior:** Automatically detects dual-scheme CSS support. When detected, includes a "Color Scheme Integrity" subsection in all reports. In gate mode, Rule 1 and Rule 2 violations block the gate.

### theme-setup
Theme creation specialist for brand-aligned Dash Mantine Components themes.

**Dual-scheme behavior:** Automatically detects dual-scheme CSS support. When detected, enforces that every color token has values for both `light` and `dark` schemes during `theme_create` and `theme_export_css`. Prompts user to verify both modes visually after export.

### layout-builder
Dashboard layout scaffolding for filtering, grid systems, and responsive design.

---

## Skills

| Skill | Description |
|-------|-------------|
| `design-system-audit.md` | Audit rules, violation patterns, and severity classification for DMC compliance |
| `theming-system.md` | Theme model, design tokens, CSS custom properties, and color palette reference |
| `mcp-tools-reference.md` | MCP tool signatures and call patterns for all viz-platform tools |
| `accessibility-rules.md` | WCAG contrast requirements and accessibility validation patterns |
| `chart-types.md` | Supported Plotly chart types and configuration options |
| `layout-templates.md` | Available layout templates and configuration |
| `responsive-design.md` | Breakpoint patterns and mobile-first design rules |
| `dmc-components.md` | DMC component registry and dynamic discovery |
| `color-scheme-validation.md` | **Conditional.** Five auditable rules for dual-scheme CSS integrity (see below) |

---

## Color Scheme Validation (v9.4.0)

### Purpose

Prevents the fix-one-break-the-other loop in dual-scheme Mantine apps — where a CSS change for one color mode silently breaks the other.

### How It Works

At the start of any color-related session, agents run a two-grep detection against the CSS entry point:

```bash
grep -c 'data-mantine-color-scheme="dark"'  <entry_point>
grep -c 'data-mantine-color-scheme="light"' <entry_point>
```

- Both counts > 0 → `scheme_mode = "dual"` → `color-scheme-validation.md` is loaded and all five rules apply
- Otherwise → `scheme_mode = "single"` → zero behavioral change

Single-scheme projects are completely unaffected.

### Five Rules

| Rule | Name | Severity |
|------|------|----------|
| 1 | Dual-Scope Rule | FAIL |
| 2 | No Unscoped Color Values | FAIL |
| 3 | Anti-Loop Detection | WARN |
| 4 | Two-Mode Verification Protocol | Required advisory |
| 5 | Token Pair Convention | WARN (existing) / FAIL (new tokens) |

See `skills/color-scheme-validation.md` for full rule definitions and detection logic.

### /viz design-gate Enhancement

`/viz design-gate` now includes Color Scheme Integrity as a **blocking check** when `scheme_mode = "dual"`:
- Unscoped color custom properties: must be 0
- Single-scheme-only color custom properties: must be 0

Gate output includes: `Color Scheme Integrity: PASS/FAIL (N defects)`

---

## Consumer Project Requirements

### CSS Entry Point Convention

Agents discover the CSS entry point using this fallback chain:

1. `CSS_ENTRY_POINT` variable in project `.env`
2. `assets/styles.css`
3. `assets/*.css` (glob all)
4. `static/css/*.css`
5. No CSS found → `scheme_mode = "single"` (color scheme checks skipped)

### Recommended Setup

For dual-scheme projects, set an explicit entry point in `.env`:

```
CSS_ENTRY_POINT=assets/styles.css
```

This avoids ambiguity when multiple CSS files exist.

---

## MCP Server

The `mcp-servers/viz-platform/` server provides all DMC validation, chart, layout, theme, and accessibility tools. Requires Python 3.11+ with the viz-platform venv set up via `./scripts/setup.sh`.

---

## Integration

See `claude-md-integration.md` for the CLAUDE.md snippet to add to consumer projects.
