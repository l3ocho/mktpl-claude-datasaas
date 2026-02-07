---
name: react component
---

# /react component - Scaffold React Component

## Skills to Load
- skills/component-patterns.md
- skills/typescript-patterns.md
- skills/visual-header.md

## Visual Output

Display header: `REACT-PLATFORM - Component`

## Usage

```
/react component <ComponentName> [--type <ui|page|layout|form>] [--props <prop1:type,prop2:type>] [--no-test]
```

## Workflow

### 1. Validate Component Name
- Must be PascalCase (e.g., `UserProfile`, `DataTable`)
- Reject reserved React names (`Component`, `Fragment`, `Suspense`)
- Check for existing component with same name — prompt before overwriting

### 2. Determine Component Type
- `ui` (default): Presentational component — props in, JSX out, no side effects
- `page`: Page-level component with data fetching, loading/error states
- `layout`: Layout wrapper with children prop and optional sidebar/header slots
- `form`: Form component with controlled inputs, validation, submit handler

### 3. Generate Component File
Using `skills/component-patterns.md` and `skills/typescript-patterns.md`:
- Create functional component with typed props interface
- Apply component type template (ui, page, layout, form)
- Use project's CSS approach (Tailwind classes, CSS modules import, styled-components)
- Include JSDoc comment block with `@component` and `@example`
- Export according to project convention (default or named)

### 4. Generate Test File
Unless `--no-test` specified:
- Create co-located test file (`ComponentName.test.tsx`)
- Include basic render test
- Include props variation tests for each required prop
- Include accessibility test if `@testing-library/jest-dom` is available
- Use project's test runner (Jest or Vitest)

### 5. Generate Types File (if complex props)
If more than 5 props or nested types:
- Create separate types file (`ComponentName.types.ts`)
- Export props interface and any supporting types
- Import types in component file

### 6. Update Barrel File
If project uses barrel files (`index.ts`):
- Add export to nearest `index.ts`
- Create `index.ts` if component is in its own directory

### 7. Summary
- Display created files with paths
- Show component usage example in JSX

## Examples

```
/react component Button                                 # Basic UI component
/react component UserProfile --type page                # Page with data fetching
/react component DashboardLayout --type layout          # Layout wrapper
/react component LoginForm --type form                  # Form with validation
/react component DataTable --props data:T[],columns:Column[],onSort:Function
```
