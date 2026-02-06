# Design: saas-react-platform

**Domain:** `saas`
**Target Version:** v9.4.0

## Purpose

React frontend development toolkit with component scaffolding, routing setup, state management patterns, and build configuration. Supports Next.js and Vite-based React projects with TypeScript.

## Target Users

- Frontend developers building React applications
- Teams using Next.js or Vite + React
- Projects needing consistent component architecture

## Commands

| Command | Description |
|---------|-------------|
| `/react setup` | Setup wizard — detect framework (Next.js/Vite), configure paths |
| `/react component` | Scaffold React component with props, types, tests, stories |
| `/react route` | Add route with page component, loader, and error boundary |
| `/react state` | Set up state management pattern (Context, Zustand, Redux Toolkit) |
| `/react hook` | Generate custom hook with TypeScript types and tests |
| `/react lint` | Validate component tree, check prop drilling, detect anti-patterns |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `react-architect` | sonnet | default | Component design, routing, state management |
| `react-auditor` | haiku | plan | Read-only lint and anti-pattern detection |

## Skills

| Skill | Purpose |
|-------|---------|
| `framework-detection` | Detect Next.js vs Vite, App Router vs Pages Router |
| `component-patterns` | Standard component structure, naming, file organization |
| `state-patterns` | State management patterns and when to use each |
| `routing-conventions` | Route naming, dynamic routes, middleware patterns |
| `typescript-patterns` | TypeScript utility types, generics, prop typing |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required.** All operations are file-based (component generation, route configuration).

## Integration Points

| Plugin | Integration |
|--------|-------------|
| projman | Issue labels: `Component/Frontend`, `Tech/React`, `Tech/Next.js` |
| viz-platform | DMC components integrate with React component architecture |
| saas-api-platform | API client generation from OpenAPI spec |
| saas-test-pilot | Component test generation via `/react component` |
| code-sentinel | Security scan for XSS, unsafe HTML, client-side secrets |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~800 |
| Dispatch file (`react.md`) | ~200 |
| 6 commands (avg) | ~3,600 |
| 2 agents | ~1,200 |
| 6 skills | ~3,000 |
| **Total** | **~8,800** |

## Open Questions

- Should we support Vue.js/Svelte as alternative frameworks?
- Integration with Storybook for component documentation?
