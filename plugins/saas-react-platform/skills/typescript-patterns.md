---
name: typescript-patterns
description: Utility types, generics for components, discriminated unions for props, and strict null checks
---

# TypeScript Patterns for React

## Purpose

Define TypeScript patterns specific to React component development. This skill ensures generated code uses idiomatic TypeScript with proper generic constraints, discriminated unions, and utility types.

---

## Props Interface Conventions

### Basic Props
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'ghost';
  disabled?: boolean;
  className?: string;
}
```

### Props with Children
```typescript
interface CardProps {
  title: string;
  children: React.ReactNode;  // Explicit, not via FC
}
```

### Discriminated Union Props
Use when a component has mutually exclusive modes:
```typescript
type AlertProps =
  | { variant: 'success'; message: string }
  | { variant: 'error'; message: string; retry: () => void }
  | { variant: 'loading'; progress?: number };
```

### Extending HTML Element Props
```typescript
interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label: string;
  error?: string;
  size?: 'sm' | 'md' | 'lg';  // Custom size, not HTML size
}
```

## Generic Component Patterns

### Generic List Component
```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage }: ListProps<T>) {
  if (items.length === 0) return <p>{emptyMessage ?? 'No items'}</p>;
  return <ul>{items.map((item, i) => <li key={keyExtractor(item)}>{renderItem(item, i)}</li>)}</ul>;
}
```

### Generic Hook
```typescript
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  // Implementation
}
```

## Utility Types for React

| Type | Use Case | Example |
|------|----------|---------|
| `React.ReactNode` | Any renderable content | `children: React.ReactNode` |
| `React.ReactElement` | JSX element only (not string/number) | `icon: React.ReactElement` |
| `React.ComponentPropsWithRef<'div'>` | All div props including ref | Extending native elements |
| `React.MouseEventHandler<HTMLButtonElement>` | Typed event handler | `onClick: React.MouseEventHandler<HTMLButtonElement>` |
| `React.ChangeEvent<HTMLInputElement>` | Input change event | `(e: React.ChangeEvent<HTMLInputElement>) => void` |
| `React.FormEvent<HTMLFormElement>` | Form submit event | `onSubmit: React.FormEventHandler<HTMLFormElement>` |
| `React.CSSProperties` | Inline style object | `style?: React.CSSProperties` |

## Common Utility Patterns

### Required Pick
Make specific properties required from an otherwise optional interface:
```typescript
type RequiredName = Required<Pick<UserProps, 'firstName' | 'lastName'>> & Omit<UserProps, 'firstName' | 'lastName'>;
```

### Extract Prop Types from Component
```typescript
type ButtonProps = React.ComponentProps<typeof Button>;
```

### Async State Pattern
```typescript
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };
```

## Strict Null Checking Patterns

### Guard Hooks
```typescript
function useRequiredContext<T>(context: React.Context<T | null>, name: string): T {
  const value = useContext(context);
  if (value === null) throw new Error(`${name} must be used within its Provider`);
  return value;
}
```

### Narrowing with Type Guards
```typescript
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value && 'email' in value;
}
```

## Things to Avoid

| Anti-Pattern | Why | Alternative |
|-------------|-----|-------------|
| `React.FC` | Implicit children, no generics | Explicit typed function |
| `any` for event handlers | Loses type safety | `React.MouseEvent<HTMLButtonElement>` |
| `as` for DOM queries | Runtime type mismatch risk | Type guards or `instanceof` |
| `!` non-null assertion | Hides potential null bugs | Conditional rendering or optional chaining |
| `enum` for prop variants | Not tree-shakeable, numeric by default | String union types |
