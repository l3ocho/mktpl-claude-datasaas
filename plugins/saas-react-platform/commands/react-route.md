---
name: react route
---

# /react route - Add Route

## Skills to Load
- skills/routing-conventions.md
- skills/framework-detection.md
- skills/visual-header.md

## Visual Output

Display header: `REACT-PLATFORM - Route`

## Usage

```
/react route <path> [--dynamic <param>] [--layout <LayoutName>] [--protected] [--error-boundary]
```

## Workflow

### 1. Detect Routing System
Using `skills/framework-detection.md` and `skills/routing-conventions.md`:
- Next.js App Router: file-based routing in `app/` directory
- Next.js Pages Router: file-based routing in `pages/` directory
- React Router (Vite/CRA): route definitions in router config
- Remix: file-based routing with loader/action conventions

### 2. Create Page Component
- Generate page component file at the correct path for the routing system:
  - App Router: `app/<path>/page.tsx`
  - Pages Router: `pages/<path>.tsx` or `pages/<path>/index.tsx`
  - React Router: `src/pages/<Path>.tsx`
- Include loading and error state handling
- If `--dynamic <param>`: create dynamic route segment (`[param]` or `:param`)
- If `--protected`: wrap with authentication check or redirect

### 3. Create Layout (if requested)
If `--layout` specified:
- App Router: create `app/<path>/layout.tsx`
- Pages Router: create layout component and wrap page
- React Router: create layout route component with `<Outlet />`

### 4. Create Error Boundary
If `--error-boundary` or for page-type routes by default:
- App Router: create `app/<path>/error.tsx`
- Other frameworks: create ErrorBoundary wrapper component
- Include fallback UI with retry action
- Log errors to console (placeholder for error reporting service)

### 5. Create Loading State
For App Router projects:
- Create `app/<path>/loading.tsx` with skeleton UI
For other frameworks:
- Include Suspense boundary in page component

### 6. Update Router Config (if applicable)
For React Router projects:
- Add route entry to router configuration file
- Include lazy loading with `React.lazy()` for code splitting
- Wire up layout if specified

### 7. Summary
- Display created files with paths
- Show route URL pattern
- Note any manual steps required (e.g., adding navigation links)

## Examples

```
/react route dashboard                              # /dashboard page
/react route users --dynamic id                     # /users/:id dynamic route
/react route settings --layout SettingsLayout       # /settings with layout
/react route admin --protected                      # /admin with auth guard
/react route products --dynamic slug --error-boundary  # Full setup
```
