---
name: framework-detection
description: Detect React framework, TypeScript configuration, routing structure, and project conventions
---

# Framework Detection

## Purpose

Analyze a project's `package.json`, configuration files, and directory structure to determine the React framework, TypeScript usage, routing pattern, and CSS approach. This skill is loaded at the start of setup and routing commands to adapt output to the project's specific toolchain.

---

## Framework Detection Rules

Check `package.json` dependencies and devDependencies in this order (first match wins):

| Framework | Detection Criteria | Routing |
|-----------|-------------------|---------|
| **Next.js (App Router)** | `next` in deps + `app/` directory exists | File-based (`app/page.tsx`) |
| **Next.js (Pages Router)** | `next` in deps + `pages/` directory exists (no `app/`) | File-based (`pages/index.tsx`) |
| **Remix** | `@remix-run/react` in deps | File-based with loaders (`routes/`) |
| **Vite + React** | `vite` in deps + `@vitejs/plugin-react` | Client-side (react-router or tanstack-router) |
| **Create React App** | `react-scripts` in deps | Client-side (react-router) |
| **Gatsby** | `gatsby` in deps | File-based (`src/pages/`) |

## TypeScript Detection

| Signal | Conclusion |
|--------|------------|
| `tsconfig.json` exists | TypeScript project |
| `typescript` in devDependencies | TypeScript project |
| `.tsx` files in `src/` or `app/` | TypeScript project |
| None of the above | JavaScript project — generate `.jsx` files |

## CSS Approach Detection

Check in order:

| Signal | Approach |
|--------|----------|
| `tailwindcss` in deps + `tailwind.config.*` | Tailwind CSS |
| `*.module.css` or `*.module.scss` files exist | CSS Modules |
| `styled-components` in deps | styled-components |
| `@emotion/react` in deps | Emotion |
| `vanilla-extract` in deps | Vanilla Extract |
| None detected | Plain CSS or inline styles |

## Test Runner Detection

| Signal | Runner |
|--------|--------|
| `vitest` in devDependencies | Vitest |
| `jest` in devDependencies or `jest.config.*` exists | Jest |
| `@testing-library/react` in deps | Testing Library (works with both) |
| `cypress` in deps | Cypress (E2E, not unit) |

## State Management Detection

| Signal | Library |
|--------|---------|
| `zustand` in dependencies | Zustand |
| `@reduxjs/toolkit` in dependencies | Redux Toolkit |
| `recoil` in dependencies | Recoil |
| `jotai` in dependencies | Jotai |
| `mobx-react` in dependencies | MobX |
| Files with `createContext` + `useReducer` pattern | React Context (built-in) |

## Directory Structure Patterns

Common patterns to detect and respect:

| Pattern | Typical Path | Detection |
|---------|-------------|-----------|
| Feature-based | `src/features/<feature>/components/` | `features/` directory with subdirectories |
| Component-based | `src/components/<Component>/` | `components/` with PascalCase subdirectories |
| Flat components | `src/components/*.tsx` | `components/` with files only, no subdirectories |
| Atomic design | `src/components/atoms/`, `molecules/`, `organisms/` | Atomic naming directories |

## Output

Store detected configuration as a reference object for other skills:

```json
{
  "framework": "nextjs-app",
  "typescript": true,
  "css_approach": "tailwind",
  "test_runner": "vitest",
  "state_management": "zustand",
  "component_dir": "src/components",
  "pages_dir": "app",
  "hooks_dir": "src/hooks",
  "structure_pattern": "feature-based"
}
```
