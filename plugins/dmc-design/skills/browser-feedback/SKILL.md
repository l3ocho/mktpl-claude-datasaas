---
name: browser-feedback
description: Inspect a running Dash app via the Chrome DevTools MCP server to verify rendered UI against the design contract and locked patterns. Loaded by /design commands and the design-reviewer agent when a live app is being debugged. Use when reviewing a running app's rendered output, diagnosing console/network errors, "preview the app", checking why a component renders wrong, or verifying live styling against .claude/design-patterns.json. Requires the external chrome-devtools MCP server (optional, not bundled with the marketplace).
---

# Browser Feedback

## Purpose

Extend dmc-design's static validation (component registry, CSS pattern checks) with live
verification of a running Dash app. Static checks read source; this skill reads what the
browser actually rendered — catching runtime drift that source analysis misses (e.g., a
pattern correct in Python but overridden at runtime by CSS specificity, a DMC prop that
renders differently than the registry predicts, a callback failure surfacing only as a
console error).

## Prerequisites

This skill depends on the Chrome DevTools MCP server — an external, optional tool
(`npx -y chrome-devtools-mcp@latest`), NOT one of the marketplace's bundled MCP servers. It
is registered per-developer (user scope) or per consumer project, never in the marketplace
repo. Requires Node.js LTS and a Chrome stable install.

If the `mcp__chrome-devtools__*` tools are not available, or no Dash app is running, skip
this skill and fall back to static validation. Browser feedback is a dev-loop enhancement,
never a hard dependency.

## When to Load

- A `/design` command is operating on a running app
- The `design-reviewer` agent is auditing and a live app is available
- The user asks to preview, inspect, or debug the rendered output of a running Dash app

## Tool Discovery

Do not hardcode tool names — the chrome-devtools server's API varies by version. Discover
the available `mcp__chrome-devtools__*` tools at runtime (ToolSearch) and use the ones
providing these capabilities:

- Navigation — open / select a page at a URL
- Console — read console messages (filter to errors and warnings)
- Network — list requests (flag non-2xx, especially failed `/_dash-update-component`)
- DOM snapshot — capture the rendered accessibility/DOM tree
- Screenshot — capture rendered output for visual checks
- Script evaluation — read computed styles / element state in page context

## The Loop

1. Confirm the app is running. Determine the dev server URL — read the project's run command
   / `.env` for a port; default Dash is `http://127.0.0.1:8050`. Do not start the server
   yourself unless the task explicitly asks; report and stop if nothing is serving.
2. Navigate to the target page (or each route under review).
3. Pull console messages — surface errors and warnings. Dash callback exceptions and React
   prop warnings appear here.
4. Pull network requests — flag failed requests; watch failing `/_dash-update-component`
   calls (broken callbacks).
5. Snapshot the DOM / capture a screenshot of the surface under review.
6. Cross-reference against the design system:
   - Load `.claude/design-patterns.json` via pattern-enforcement. For each `css`/`component`
     pattern, verify the rendered result, not just source. `severity: fail` violations are
     hard findings; `severity: warn` are warnings.
   - Load `.claude/design-contract.json`. Verify rendered surfaces (base/raised/overlay)
     match the contract's tokens and that locked component specs hold in the DOM.
7. Report findings with route + element reference, separating static-confirmed from
   live-only findings.

## Read-Only Discipline

Inspection only: navigate, read, snapshot, evaluate. Do not drive app mutations (form fills,
clicks that submit) unless the task explicitly requires reproducing an interaction. Never
write captured screenshots into the repository — they are transient debug artifacts.

## Integration

- pattern-enforcement — provides the locked-pattern set this skill verifies against.
- color-scheme-validation — when `scheme_mode = "dual"`, verify both light and dark rendered
  output, not just CSS source.
- design-reviewer agent — calls this skill for its Live Render Verification step when the
  tools and a running app are present.
