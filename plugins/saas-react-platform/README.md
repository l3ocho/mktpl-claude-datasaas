# saas-react-platform Plugin

React frontend development toolkit with component scaffolding, routing, state management, and anti-pattern detection for Claude Code.

## Overview

The saas-react-platform plugin provides a complete React development toolkit that adapts to your project's framework (Next.js, Vite, CRA, Remix). It generates TypeScript-first components, configures routing, sets up state management patterns, and audits your component tree for anti-patterns.

Key features:
- **Framework-aware**: Detects Next.js (App Router/Pages Router), Vite, CRA, Remix
- **TypeScript-first**: Every generated file includes proper types, generics, and interfaces
- **Component scaffolding**: UI, page, layout, and form component templates with tests
- **Routing setup**: File-based routing (Next.js) and client-side routing (React Router)
- **State patterns**: Context, Zustand, and Redux Toolkit with guided selection
- **Anti-pattern detection**: Component tree analysis, hook compliance, TypeScript strictness

## Installation

This plugin is part of the Leo Claude Marketplace. Install via the marketplace or copy the `plugins/saas-react-platform/` directory to your Claude Code plugins path.

## Commands

| Command | Description |
|---------|-------------|
| `/react setup` | Setup wizard — detect framework, TypeScript, CSS approach |
| `/react component` | Scaffold component with props, types, and tests |
| `/react route` | Add route with page component, layout, and error boundary |
| `/react state` | Set up state management (Context, Zustand, Redux Toolkit) |
| `/react hook` | Generate custom hook with types and tests |
| `/react lint` | Validate component tree and detect anti-patterns |

## Quick Start

```
/react setup                           # Detect project configuration
/react component UserProfile --type page   # Scaffold a page component
/react route dashboard --protected     # Add protected route
/react state auth --pattern context    # Set up auth context
/react hook useDebounce --type lifecycle   # Generate custom hook
/react lint                            # Audit component tree
```

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `react-architect` | Sonnet | Component design, routing, state management, hook generation |
| `react-auditor` | Haiku | Read-only component tree analysis and anti-pattern detection |

## Skills

| Skill | Purpose |
|-------|---------|
| `framework-detection` | Detect Next.js, Vite, CRA, Remix, TypeScript, CSS approach |
| `component-patterns` | Functional components, prop typing, exports, co-located tests |
| `state-patterns` | React Context, Zustand, Redux Toolkit selection and templates |
| `routing-conventions` | File-based and client-side routing patterns |
| `typescript-patterns` | Utility types, generics, discriminated unions for React |
| `visual-header` | Standard visual output formatting |

## Supported Frameworks

| Framework | Version | Routing | Status |
|-----------|---------|---------|--------|
| Next.js (App Router) | 13.4+ | File-based (`app/`) | Full support |
| Next.js (Pages Router) | 12+ | File-based (`pages/`) | Full support |
| Vite + React | 4+ | React Router | Full support |
| Create React App | 5+ | React Router | Full support |
| Remix | 2+ | File-based (`routes/`) | Basic support |

## License

MIT License — Part of the Leo Claude Marketplace.
