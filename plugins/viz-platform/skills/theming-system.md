# Surface Contract Specification

## Purpose

The design contract (``.claude/design-contract.json``) defines a per-project surface hierarchy
that the viz-platform resolver enforces automatically. Every component rendered in a
consumer project resolves its background, border, and variant tokens through this contract
rather than from ad-hoc per-component decisions.

---

## Surface Hierarchy Model

Four surface levels, ordered from back to front:

| Level | Semantic meaning | Typical DMC components | Default (light) | Default (dark) |
|-------|-----------------|------------------------|-----------------|----------------|
| `base` | App shell, main page background | `AppShellMain`, `Container`, `Stack`, `Group` | `white` | `dark.8` |
| `raised` | Cards, panels elevated above base | `Card`, `Paper` | `white` + border | `dark.7` + border |
| `overlay` | Floating elements above the page | `Modal`, `Drawer`, `Popover` | `gray.0` | `dark.6` |
| `nested_in_overlay` | Content inside overlays | `Card` inside `Modal` | `white` | `dark.7` |

### Inference Rules

The resolver infers surface level from component name and parent context:

1. If `parent_context == "overlay"` → level is `nested_in_overlay` (always)
2. Otherwise, look up `COMPONENT_SURFACE_DEFAULTS` map
3. Unknown components default to `base`

Pass `surface_context` explicitly to `contract_resolve_component` to override inference.

---

## Resolver Merge Rules

Resolution order (highest priority wins):

```
component_lock.spec  >  surface tokens  >  requested_props
```

1. Start with `requested_props` as the base
2. Apply surface tokens: `bg`, `withBorder` + `borderColor` (if border defined), `variant`
3. Apply lock `spec` on top — lock entries always win

**Contract wins over caller.** If the contract says `bg: "white"` for raised surfaces,
callers cannot override it by passing `bg: "blue"` to `validate_component`.

---

## Component Lock Protocol

Use `contract_lock_component` to freeze specific prop values for a component:

```python
contract_lock_component(
    component="Modal",
    spec={"padding": "md", "radius": "md", "withCloseButton": True},
    reference_file="app/pages/settings.py",
    reference_line=42
)
```

### When to lock

- The component has a canonical usage that must not drift (e.g., the primary Modal style)
- A design decision was made in a PR and needs to be preserved
- Surface-derived tokens are insufficient (lock adds non-surface props like `radius`)

### Cascade behavior

Locks are per-component-name, not per-instance. All `Modal` components in the project
receive the locked spec. Use with intent — locks affect every usage site.

---

## Light / Dark as Separate Contracts

Light and dark are independent surface maps within the same contract file. The resolver
picks the correct map based on the `scheme` parameter:

```json
{
  "schemes": {
    "light": { "surfaces": { "base": { "bg": "white" }, ... } },
    "dark":  { "surfaces": { "base": { "bg": "dark.8" }, ... } }
  }
}
```

Pass `scheme="dark"` to `contract_resolve_component` when rendering in dark mode.
Component locks apply regardless of scheme (the lock `spec` is scheme-agnostic).

---

## Density Protocol

The `density` field controls DMC spacing props project-wide:

| Density | DMC spacing props | Use case |
|---------|-------------------|----------|
| `compact` | `p="xs"`, `gap="xs"`, `spacing="xs"` | Data-dense dashboards |
| `comfortable` | `p="md"`, `gap="md"`, `spacing="md"` | Content-forward apps |

The resolver does not automatically inject spacing props — density is a convention
for commands and agents to read from the contract and apply consistently:

```python
contract = contract_load()
density = contract["density"]  # "compact" or "comfortable"
spacing = "xs" if density == "compact" else "md"
```

---

## Interaction Tokens

The `interaction` block defines project-wide behavioral tokens:

| Token | Default | Meaning |
|-------|---------|---------|
| `hover_delta` | `-1` | Shade shift on hover (e.g., shade 5 → shade 4) |
| `focus_ring.size` | `2` | Focus ring width in px |
| `focus_ring.color_token` | `primary.5` | Focus ring color |
| `disabled_opacity` | `0.55` | Opacity for disabled state |
| `error_token` | `red.6` | Color token for error states |

Read these from `contract_load()` output when generating interactive components.

---

## Extending the Contract

To add a new surface level or override defaults, edit `.claude/design-contract.json`
directly or re-run `/viz setup` Phase 3.

To add a new color scheme (e.g., high-contrast):

1. Add a new key under `schemes` (note: schema only permits `light` and `dark` by default)
2. Or extend the schema at `mcp-servers/viz-platform/schemas/design-contract.schema.json`

To remove a lock: delete the component key from `component_locks` in the contract file.

---

## Mantine Color Token Reference

Each Mantine color has 10 shades (0–9). Shade 5 is the primary shade.

| Use | Token pattern | Example |
|-----|---------------|---------|
| Backgrounds | `{color}.{0-2}` | `gray.0`, `dark.8` |
| Borders | `{color}.{2-4}` | `gray.2`, `dark.5` |
| Interactive | `{color}.{5-7}` | `primary.5`, `blue.6` |
| Error | `red.6` | Standard error |

Available colors: blue, cyan, teal, green, lime, yellow, orange, red, pink,
grape, violet, indigo, gray, dark.
