---
name: react state
---

# /react state - State Management Setup

## Skills to Load
- skills/state-patterns.md
- skills/visual-header.md

## Visual Output

Display header: `REACT-PLATFORM - State Management`

## Usage

```
/react state <store-name> [--pattern <context|zustand|redux>] [--actions <action1,action2>]
```

## Workflow

### 1. Analyze State Requirements
- Ask user about the state scope:
  - **Local**: Component-level state (suggest `useState`/`useReducer` — no scaffolding needed)
  - **Shared**: Cross-component state within a feature (suggest Context or Zustand)
  - **Global**: App-wide state with complex logic (suggest Redux Toolkit or Zustand)
- If `--pattern` specified, skip detection and use requested pattern
- Check `package.json` for existing state libraries

### 2. Select Pattern
Using `skills/state-patterns.md`:
- **React Context**: For simple shared state (theme, auth, locale). No additional dependencies.
- **Zustand**: For medium complexity. Minimal boilerplate, good DevTools support.
- **Redux Toolkit**: For complex state with middleware, async thunks, entity adapters.
- If library not installed, ask user to install it first (display exact `npm install` command)

### 3. Generate Store

#### Context Pattern
- Create context file with typed state interface
- Create provider component with `useReducer` for state + dispatch
- Create custom hook (`use<StoreName>`) with context validation
- Create action types and reducer function

#### Zustand Pattern
- Create store file with typed state and actions
- Include DevTools middleware (if zustand version supports it)
- Create selector hooks for computed/derived state
- Include persist middleware setup (optional, ask user)

#### Redux Toolkit Pattern
- Create slice file with `createSlice` (state, reducers, extraReducers)
- Create async thunks with `createAsyncThunk` if API calls needed
- Create typed hooks (`useAppDispatch`, `useAppSelector`) if not existing
- Add slice to root store configuration
- Create selector functions for memoized state access

### 4. Generate Actions
If `--actions` specified:
- Create action creators/reducers for each named action
- Type the action payloads
- Include in the store/slice definition

### 5. Summary
- Display created files
- Show usage example with import and hook usage
- List available actions/selectors

## Examples

```
/react state auth --pattern context --actions login,logout,setUser
/react state cart --pattern zustand --actions addItem,removeItem,clearCart
/react state products --pattern redux --actions fetchAll,fetchById,updateProduct
/react state theme --pattern context --actions toggle,setMode
```
