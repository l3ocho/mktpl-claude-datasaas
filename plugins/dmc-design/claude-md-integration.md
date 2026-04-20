# dmc-design CLAUDE.md Integration

Add this snippet to consumer project CLAUDE.md to enable dmc-design enforcement.

## Integration Snippet

```markdown
## DMC Design System (dmc-design)

### Design Patterns
Always read `.claude/design-patterns.json` before any UI edit. Locked patterns are
non-negotiable. Run `/design pattern check` before and after any CSS or layout change.

### Design Contract
Always read `.claude/design-contract.json` before any component creation. Contract
resolver enforces surface hierarchy and component locks. Contract wins over caller.

### Commands
- `/design setup` — Environment + contract builder
- `/design theme apply|create|export-css` — Theme management
- `/design pattern scan|lock|check|list|unlock` — Pattern enforcement
- `/design component <n>` — DMC validation
- `/design accessibility` — WCAG contrast check

### MCP Tools
- DMC: list_components, get_component_props, validate_component
- Theme: theme_validate, theme_export_css
- Accessibility: accessibility_validate_colors, accessibility_validate_theme
- Contract: contract_load, contract_validate, contract_resolve_component,
  contract_lock_component, contract_get_surface
```
