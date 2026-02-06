---
name: react setup
---

# /react setup - React Project Setup Wizard

## Skills to Load
- skills/framework-detection.md
- skills/visual-header.md

## Visual Output

Display header: `REACT-PLATFORM - Setup Wizard`

## Usage

```
/react setup
```

## Workflow

### Phase 1: Framework Detection
- Scan for `package.json` to confirm Node.js project
- Detect framework using `skills/framework-detection.md`:
  - Next.js (check for `next` in dependencies, `next.config.*`)
  - Vite + React (check for `vite` and `@vitejs/plugin-react`)
  - Create React App (check for `react-scripts`)
  - Remix (check for `@remix-run/react`)
- Detect App Router vs Pages Router for Next.js projects
- Identify TypeScript usage (`tsconfig.json`, `.tsx` files)

### Phase 2: Project Structure Analysis
- Scan directory structure for existing patterns:
  - Component directory: `src/components/`, `components/`, `app/components/`
  - Page directory: `src/pages/`, `app/`, `src/app/`
  - Hook directory: `src/hooks/`, `hooks/`
  - Test patterns: `__tests__/`, `*.test.tsx`, `*.spec.tsx`
- Detect existing barrel files (`index.ts` re-exports)
- Check for existing state management (Redux store, Zustand stores, Context providers)

### Phase 3: Convention Configuration
- Confirm or override detected patterns:
  - Component naming: PascalCase (default)
  - File naming: PascalCase (`Button.tsx`) or kebab-case (`button.tsx`)
  - Test co-location: same directory (`Button.test.tsx`) or `__tests__/` subdirectory
  - CSS approach: CSS Modules, Tailwind, styled-components, vanilla extract
  - Export style: named exports, default exports, or barrel files

### Phase 4: Summary
- Display detected configuration:
  - Framework and version
  - TypeScript: yes/no
  - Component directory
  - Routing pattern
  - State management (if detected)
  - CSS approach
  - Test runner (Jest, Vitest)
- Store configuration for future commands

## Important Notes

- Uses Bash, Read, Write, AskUserQuestion tools
- Does not install packages — only detects and configures
- Configuration stored in project for consistent scaffolding
