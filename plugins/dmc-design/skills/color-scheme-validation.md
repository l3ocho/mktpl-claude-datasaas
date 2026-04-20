---
name: color-scheme-validation
description: Auditable rules for CSS color scheme integrity in dual-scheme Mantine applications. Loaded conditionally when both light and dark scheme selectors are detected.
---

# Color Scheme Validation

## Purpose

Defines five auditable rules for maintaining CSS color scheme integrity in dual-scheme Mantine applications. Prevents the fix-one-break-the-other loop where CSS changes in one color mode silently break the other.

This skill is **loaded conditionally** — only when `scheme_mode = "dual"` is detected (see detection logic below).

---

## CSS Entry Point Discovery

Agents use this fallback chain to locate the CSS entry point before running any rule:

1. Check project `.env` for `CSS_ENTRY_POINT` variable — if set, use that path directly
2. If not set, check `assets/styles.css`
3. If not found, glob `assets/*.css` and scan all matched files
4. If `assets/` does not exist, check `static/css/*.css`
5. If no CSS files found anywhere → default to `scheme_mode = "single"` (this skill is not loaded)

---

## Scheme Detection

Run once at the start of any session involving CSS changes. Result determines whether this skill is loaded.

```
1. Resolve CSS entry point (discovery chain above)
2. dark_count  = grep -c 'data-mantine-color-scheme="dark"'  <entry_point>
3. light_count = grep -c 'data-mantine-color-scheme="light"' <entry_point>
4. If dark_count > 0 AND light_count > 0 → scheme_mode = "dual"  → load this skill
5. Otherwise                              → scheme_mode = "single" → skip this skill
```

Single-scheme apps: zero behavioral change. This skill is a no-op.

---

## Rule 1 — Dual-Scope Rule

**Severity: FAIL**

Every CSS custom property holding a color value (`background`, `foreground`, `border`, `shadow`, `accent`) must be defined under **both** `[data-mantine-color-scheme="dark"]` and `[data-mantine-color-scheme="light"]` selector blocks.

### Detection

Parse the CSS entry point. For each custom property with a color value:
- Check that the property appears inside a `[data-mantine-color-scheme="dark"]` block
- Check that the same property appears inside a `[data-mantine-color-scheme="light"]` block

### Defect

- Custom property defined in one scheme block but not the other
- Custom property defined outside any scheme block (at `:root` level with a color value)

### Example — Defect

```css
[data-mantine-color-scheme="dark"] {
  --app-surface-bg: #1a1a2e;   /* only in dark → FAIL */
}
/* missing light block for --app-surface-bg */
```

### Example — Correct

```css
[data-mantine-color-scheme="dark"] {
  --app-surface-bg: #1a1a2e;
}
[data-mantine-color-scheme="light"] {
  --app-surface-bg: #ffffff;
}
```

---

## Rule 2 — No Unscoped Color Values Rule

**Severity: FAIL**

Raw color values (`#hex`, `rgb()`, `rgba()`, `hsl()`, named CSS colors) in CSS rules targeting application components must appear inside a `[data-mantine-color-scheme]` ancestor selector.

### Exceptions

- CSS reset rules (e.g., `*, *::before, *::after`)
- Third-party library overrides
- Mantine internal variables (prefixed `--mantine-`)

### Detection

Find color value declarations where no `[data-mantine-color-scheme]` ancestor selector is present in the rule's selector chain.

Patterns to detect:
```
/#[0-9a-fA-F]{3,8}/
/rgb\(/ /rgba\(/
/hsl\(/ /hsla\(/
/:\s*(black|white|red|blue|green|gray|grey|transparent)/
```

### Example — Defect

```css
.my-card {
  background-color: #f5f5f5;  /* unscoped → FAIL */
}
```

### Example — Correct

```css
[data-mantine-color-scheme="light"] .my-card {
  background-color: #f5f5f5;
}
[data-mantine-color-scheme="dark"] .my-card {
  background-color: #2c2c2c;
}
```

---

## Rule 3 — Anti-Loop Detection Rule

**Severity: WARN** (advisory — blocks further color changes until scoping is verified)

If the same CSS custom property appears more than once in the branch diff output, flag as a potential scheme-scoping loop before allowing another modification.

### Diff Baseline

```bash
git diff $(git merge-base HEAD development)
```

This captures **all feature-branch changes** (committed and uncommitted) relative to the development merge-base. Works regardless of staging/commit state mid-session.

### Detection

Parse the diff output for repeated `--[prefix]-` custom property token names.

```
token_names = extract all "--[word]-[word...]" from diff +/- lines
for each token_name where count > 1:
  agent MUST verify scheme scoping before proceeding with further color changes
```

### When triggered

Display this advisory before allowing the next color-related edit:

```
⚠️ Anti-Loop Advisory: --[token-name] appears N times in branch diff.
   This may indicate a scheme-scoping loop. Please verify:
   1. Is this token defined under BOTH [data-mantine-color-scheme="dark"] and [data-mantine-color-scheme="light"]?
   2. Did a change in one scheme accidentally remove it from the other?
   Confirm scoping is correct before proceeding.
```

---

## Rule 4 — Two-Mode Verification Protocol

**Severity: Required (advisory)**

After any color-related change passes automated checks, the agent must instruct the user to verify both color modes visually. Automated checks catch structural defects; visual verification catches value-level issues.

### Instruction Text

After completing color-related changes, display:

```
✅ Automated color scheme checks passed.

Manual verification required:
1. Open the application in your browser
2. Toggle the theme switch to LIGHT mode — confirm the component renders correctly
3. Toggle the theme switch to DARK mode — confirm the component renders correctly
4. Pay special attention to: text contrast, background fills, border colors, shadow visibility

Both modes must be verified before this change is considered complete.
```

This step is not optional. Do not mark color-related work complete without displaying this instruction.

---

## Rule 5 — Token Pair Convention

**Severity: WARN** for existing tokens; **FAIL** for newly created tokens in the same session

New color tokens must use scheme-neutral names. The property name is the same in both scheme blocks; only the value differs.

### Correct Pattern

```css
[data-mantine-color-scheme="dark"] {
  --app-card-bg: #1e1e2e;    /* same name, different value */
}
[data-mantine-color-scheme="light"] {
  --app-card-bg: #ffffff;    /* same name, different value */
}
```

### Wrong Pattern

```css
:root {
  --app-card-bg-dark: #1e1e2e;   /* scheme in name → WARN/FAIL */
  --app-card-bg-light: #ffffff;  /* scheme in name → WARN/FAIL */
}
```

### Detection

Scan for custom properties whose names end in `-dark`, `-light`, `-dm`, `-lm`, or contain `dark-mode`, `light-mode` as a suffix segment.

- If the property was **already present** before this session (not in diff): WARN
- If the property was **created in this session** (present in diff as added line): FAIL

---

## Summary Table

| Rule | Name | Severity | Trigger |
|------|------|----------|---------|
| 1 | Dual-Scope Rule | FAIL | Single-scheme custom property |
| 2 | No Unscoped Color Values | FAIL | Raw color outside scheme selector |
| 3 | Anti-Loop Detection | WARN | Repeated token in branch diff |
| 4 | Two-Mode Verification Protocol | Required advisory | After any color change passes checks |
| 5 | Token Pair Convention | WARN/FAIL | Scheme-suffixed token names |

---

## Integration Notes

- **component-check**: Apply Rules 1, 2, 3, 4 alongside component prop validation when `scheme_mode = "dual"`
- **design-reviewer**: Include Rule 1–5 findings under "Color Scheme Integrity" subsection in reports; FAIL findings block gate mode
- **theme-setup**: Apply Rules 1 and 5 during `theme_create` and `theme_export_css`; apply Rule 4 after export
- **viz-design-gate**: Rules 1 and 2 are blocking checks (count must be 0 to pass)
