---
name: component-patterns
description: Component structure conventions including functional components, prop typing, exports, and co-located tests
---

# Component Patterns

## Purpose

Define standard patterns for React component scaffolding. This skill ensures all generated components follow consistent structure, typing, export conventions, and test co-location.

---

## Component File Structure

Every component file follows this order:

```typescript
// 1. Imports (external first, then internal, then styles)
import { type FC } from 'react';
import { Button } from '@/components/ui/Button';
import styles from './ComponentName.module.css';

// 2. Types (inline for simple, separate file for complex)
interface ComponentNameProps {
  title: string;
  onAction: () => void;
  children?: React.ReactNode;
}

// 3. Component definition
/**
 * Brief description of what this component does.
 *
 * @component
 * @example
 * <ComponentName title="Hello" onAction={() => console.log('clicked')} />
 */
const ComponentName: FC<ComponentNameProps> = ({ title, onAction, children }) => {
  return (
    <div>
      <h2>{title}</h2>
      {children}
      <button onClick={onAction}>Action</button>
    </div>
  );
};

// 4. Display name (for DevTools)
ComponentName.displayName = 'ComponentName';

// 5. Export
export default ComponentName;
```

## Component Type Templates

### UI Component (presentational)
- Props in, JSX out — no side effects, no data fetching
- Pure function: same props always produce same output
- Accept `className` prop for style override flexibility
- Accept `children` if component is a container/wrapper

### Page Component
- Includes data fetching (server component in App Router, `useEffect` in client)
- Loading state with skeleton placeholder
- Error state with retry action
- `'use client'` directive only if client interactivity required (App Router)

### Layout Component
- Accepts `children: React.ReactNode` as required prop
- Optional slot props for sidebar, header, footer
- Handles responsive behavior
- Wraps with error boundary

### Form Component
- Controlled inputs with `useState` or form library (`react-hook-form`)
- Typed form values interface
- Validation schema (Zod recommended)
- Submit handler with loading state
- Error display per field and form-level

## Test Co-location Patterns

Test file sits next to component file:

```
src/components/Button/
  Button.tsx
  Button.test.tsx
  Button.module.css  (if CSS Modules)
  index.ts           (barrel file)
```

### Minimum Test Coverage

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ComponentName from './ComponentName';

describe('ComponentName', () => {
  it('renders without crashing', () => {
    render(<ComponentName title="Test" onAction={() => {}} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('calls onAction when button clicked', async () => {
    const onAction = vi.fn();
    render(<ComponentName title="Test" onAction={onAction} />);
    await userEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalledOnce();
  });
});
```

## Barrel File Convention

Each component directory exports through `index.ts`:

```typescript
export { default as ComponentName } from './ComponentName';
export type { ComponentNameProps } from './ComponentName';
```

## Anti-Patterns to Avoid

| Pattern | Why | Alternative |
|---------|-----|-------------|
| Class components | Legacy API, verbose | Functional components + hooks |
| `React.FC` with children | Children always optional, incorrect type narrowing | Explicit `children` prop in interface |
| Prop spreading `{...props}` | Obscures expected interface | Explicitly destructure needed props |
| `useEffect` for derived state | Unnecessary render cycle | Compute during render or `useMemo` |
| `forwardRef` without `displayName` | Unnamed in DevTools | Always set `displayName` |
