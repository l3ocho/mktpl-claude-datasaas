---
name: react lint
---

# /react lint - Component Tree Analysis

## Skills to Load
- skills/component-patterns.md
- skills/typescript-patterns.md
- skills/visual-header.md

## Visual Output

Display header: `REACT-PLATFORM - Lint`

## Usage

```
/react lint [path] [--fix] [--strict]
```

## Workflow

### 1. Scan Target
- Default path: project root (all `.tsx`, `.ts`, `.jsx`, `.js` files)
- If specific path provided, scan only that directory/file
- Exclude: `node_modules/`, `dist/`, `build/`, `.next/`, `coverage/`

### 2. Component Structure Analysis
Check each component file for:

| Check | Severity | Description |
|-------|----------|-------------|
| Missing prop types | FAIL | Components without TypeScript interface or PropTypes |
| Unused props | WARN | Props declared in interface but never used in JSX |
| Missing display name | INFO | Components without `displayName` (matters for DevTools) |
| Inline function props | WARN | Functions defined inline in JSX (`onClick={() => ...}`) |
| Missing key prop | FAIL | List rendering without `key` prop |
| Index as key | WARN | Using array index as `key` in dynamic lists |
| Large component | WARN | Component exceeds 200 lines (suggest splitting) |
| Mixed concerns | WARN | Data fetching + rendering in same component |
| Missing error boundary | INFO | Page components without error boundary |

### 3. Hook Analysis
Check custom hooks for:

| Check | Severity | Description |
|-------|----------|-------------|
| Missing cleanup | WARN | `useEffect` with subscription/listener but no cleanup return |
| Stale closure | WARN | State variables used in effect without being in dependency array |
| Conditional hook call | FAIL | Hook called inside condition, loop, or after early return |
| Missing dependency | WARN | Values used in effect but missing from dependency array |

### 4. State Management Analysis
Check state patterns for:

| Check | Severity | Description |
|-------|----------|-------------|
| Prop drilling | WARN | Same prop passed through 3+ component levels |
| Unnecessary state | INFO | State that could be derived from existing state or props |
| Multiple setState calls | INFO | Sequential `setState` calls that could be a single update |
| Context overuse | WARN | Context provider wrapping entire app for localized state |

### 5. TypeScript Analysis (--strict mode)
Additional checks when `--strict` enabled:

| Check | Severity | Description |
|-------|----------|-------------|
| `any` type usage | WARN | Explicit or implicit `any` in component code |
| Missing return type | INFO | Components without explicit return type |
| Non-null assertion | WARN | Use of `!` operator instead of proper null checking |
| Type assertion overuse | WARN | Frequent `as` casts suggesting type design issues |

### 6. Report

```
+----------------------------------------------------------------------+
|  REACT-PLATFORM - Lint                                               |
|  /src/components                                                     |
+----------------------------------------------------------------------+

Files Scanned: 24
Components Analyzed: 18
Hooks Analyzed: 6

FAIL (2)
  1. [src/components/UserList.tsx:45] Missing key prop
     Found: <UserCard user={user} /> inside .map()
     Fix: Add key={user.id} to <UserCard>

  2. [src/hooks/useData.ts:12] Conditional hook call
     Found: if (enabled) { useState(...) }
     Fix: Move hook before condition, use enabled as guard inside

WARN (3)
  1. [src/components/Dashboard.tsx] Large component (287 lines)
     Suggestion: Extract chart section into DashboardCharts component

  2. [src/components/Form.tsx:23] Inline function prop
     Found: onChange={() => setValue(e.target.value)}
     Suggestion: Extract to named handler function

  3. [src/hooks/useWebSocket.ts:18] Missing cleanup
     Found: useEffect with addEventListener but no removeEventListener
     Fix: Return cleanup function from useEffect

INFO (1)
  1. [src/components/Card.tsx] Missing displayName
     Suggestion: Add Card.displayName = 'Card'

SUMMARY
  Components: 16 clean, 2 with issues
  Hooks: 5 clean, 1 with issues
  Anti-patterns: 0 FAIL, 3 WARN, 1 INFO

VERDICT: FAIL (2 blocking issues)
```

## Examples

```
/react lint                              # Lint entire project
/react lint src/components/              # Lint specific directory
/react lint src/components/Form.tsx      # Lint single file
/react lint --strict                     # Include TypeScript checks
/react lint --fix                        # Auto-fix where possible
```
