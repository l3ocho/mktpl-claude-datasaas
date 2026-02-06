---
name: state-patterns
description: State management patterns — React Context for simple, Zustand for medium, Redux Toolkit for complex
---

# State Management Patterns

## Purpose

Guide state management decisions and provide scaffolding templates for React Context, Zustand, and Redux Toolkit. This skill helps select the right pattern based on complexity and generates consistent store implementations.

---

## Decision Framework

| Criteria | Context | Zustand | Redux Toolkit |
|----------|---------|---------|---------------|
| **Scope** | Single feature, few consumers | Multiple features, medium consumers | App-wide, many consumers |
| **Complexity** | Simple values (theme, locale, auth) | Medium (cart, form wizard, filters) | Complex (normalized entities, async workflows) |
| **Async logic** | Manual with `useEffect` | Built-in with async actions | `createAsyncThunk` with lifecycle |
| **DevTools** | None built-in | Optional middleware | Full Redux DevTools integration |
| **Dependencies** | None (built-in React) | ~2KB, zero config | ~12KB, more boilerplate |
| **Learning curve** | Low | Low | Medium-High |

### Quick Decision

- Need to share a simple value across a few components? **Context**
- Need a store with some async logic and moderate complexity? **Zustand**
- Need normalized state, middleware, complex async flows, or strict patterns? **Redux Toolkit**

## React Context Template

```typescript
// stores/auth-context.tsx
import { createContext, useContext, useReducer, type ReactNode } from 'react';

// State type
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Action types
type AuthAction =
  | { type: 'LOGIN'; payload: User }
  | { type: 'LOGOUT' }
  | { type: 'SET_LOADING'; payload: boolean };

// Initial state
const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
};

// Reducer
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN':
      return { ...state, user: action.payload, isAuthenticated: true, isLoading: false };
    case 'LOGOUT':
      return { ...state, user: null, isAuthenticated: false };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    default:
      return state;
  }
}

// Context
const AuthContext = createContext<{
  state: AuthState;
  dispatch: React.Dispatch<AuthAction>;
} | null>(null);

// Provider
export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState);
  return (
    <AuthContext.Provider value={{ state, dispatch }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook with validation
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

## Zustand Template

```typescript
// stores/cart-store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
  totalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],
        addItem: (item) => set((state) => {
          const existing = state.items.find((i) => i.id === item.id);
          if (existing) {
            return { items: state.items.map((i) =>
              i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
            )};
          }
          return { items: [...state.items, { ...item, quantity: 1 }] };
        }),
        removeItem: (id) => set((state) => ({
          items: state.items.filter((i) => i.id !== id),
        })),
        clearCart: () => set({ items: [] }),
        totalPrice: () => get().items.reduce(
          (sum, item) => sum + item.price * item.quantity, 0
        ),
      }),
      { name: 'cart-storage' }
    )
  )
);
```

## Redux Toolkit Template

```typescript
// store/slices/productsSlice.ts
import { createSlice, createAsyncThunk, type PayloadAction } from '@reduxjs/toolkit';

// Async thunk
export const fetchProducts = createAsyncThunk(
  'products/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/products');
      return await response.json();
    } catch (error) {
      return rejectWithValue('Failed to fetch products');
    }
  }
);

// Slice
const productsSlice = createSlice({
  name: 'products',
  initialState: {
    items: [] as Product[],
    status: 'idle' as 'idle' | 'loading' | 'succeeded' | 'failed',
    error: null as string | null,
  },
  reducers: {
    updateProduct: (state, action: PayloadAction<Product>) => {
      const index = state.items.findIndex((p) => p.id === action.payload.id);
      if (index !== -1) state.items[index] = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload as string;
      });
  },
});

export const { updateProduct } = productsSlice.actions;
export default productsSlice.reducer;
```

## When NOT to Use Global State

- Form input values (use local `useState` or `react-hook-form`)
- UI toggle state (modal open/close) unless shared across routes
- Computed values derivable from existing state (compute inline or `useMemo`)
- Server cache data (use TanStack Query or SWR instead of Redux)
