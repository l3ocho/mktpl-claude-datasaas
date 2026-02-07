---
name: react hook
---

# /react hook - Generate Custom Hook

## Skills to Load
- skills/typescript-patterns.md
- skills/component-patterns.md
- skills/visual-header.md

## Visual Output

Display header: `REACT-PLATFORM - Custom Hook`

## Usage

```
/react hook <hookName> [--type <data|ui|form|lifecycle>] [--no-test]
```

## Workflow

### 1. Validate Hook Name
- Must start with `use` (e.g., `useAuth`, `useDebounce`, `useLocalStorage`)
- Must be camelCase after the `use` prefix
- Check for existing hook with same name — prompt before overwriting

### 2. Determine Hook Type
- `data` (default): Hooks that manage data fetching, caching, or transformation
  - Template includes: state for data/loading/error, fetch function, cleanup
  - Example: `useUsers`, `useApiCall`, `useInfiniteScroll`
- `ui`: Hooks that manage UI state or DOM interactions
  - Template includes: ref handling, event listeners, cleanup on unmount
  - Example: `useMediaQuery`, `useClickOutside`, `useIntersectionObserver`
- `form`: Hooks that manage form state and validation
  - Template includes: values state, errors state, handlers, validation, submit
  - Example: `useForm`, `useFieldValidation`, `useMultiStepForm`
- `lifecycle`: Hooks that wrap React lifecycle patterns
  - Template includes: effect with cleanup, dependency management
  - Example: `useDebounce`, `useInterval`, `usePrevious`

### 3. Generate Hook File
- Create hook file in project's hooks directory (`src/hooks/` or `hooks/`)
- Include TypeScript generics where appropriate (e.g., `useLocalStorage<T>`)
- Include proper cleanup in `useEffect` return functions
- Follow React hooks rules: no conditional hooks, stable dependency arrays
- Include JSDoc with `@param`, `@returns`, and `@example`

### 4. Generate Test File
Unless `--no-test` specified:
- Create test file using `@testing-library/react-hooks` or `renderHook` from `@testing-library/react`
- Test initial state
- Test state transitions after actions
- Test cleanup behavior
- Test error states (for data hooks)
- Use `act()` wrapper for state updates

### 5. Generate Types
- Export hook parameter types and return type as named interfaces
- Use generics for reusable hooks (e.g., `useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void]`)
- Include discriminated union types for loading/error/success states

### 6. Update Barrel File
If hooks directory has `index.ts`:
- Add export for new hook

### 7. Summary
- Display created files
- Show usage example in a component

## Examples

```
/react hook useAuth --type data                 # Auth state management
/react hook useDebounce --type lifecycle         # Debounced value hook
/react hook useClickOutside --type ui            # Click outside detection
/react hook useContactForm --type form           # Form with validation
/react hook useLocalStorage                      # Generic localStorage hook
```
