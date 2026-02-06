---
name: routing-conventions
description: File-based routing (Next.js), react-router conventions, dynamic routes, layouts, and middleware
---

# Routing Conventions

## Purpose

Define routing patterns for each supported framework. This skill ensures route scaffolding produces the correct file structure, naming conventions, and framework-specific boilerplate.

---

## Next.js App Router (v13.4+)

### File Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI — required to make segment publicly accessible |
| `layout.tsx` | Shared layout wrapping child pages — persists across navigations |
| `loading.tsx` | Loading UI shown while page is loading (Suspense boundary) |
| `error.tsx` | Error UI shown when page throws (must be client component) |
| `not-found.tsx` | 404 UI for segment |
| `route.ts` | API route handler (GET, POST, etc.) |

### Route Patterns

```
app/
  page.tsx                          # /
  about/page.tsx                    # /about
  blog/page.tsx                     # /blog
  blog/[slug]/page.tsx              # /blog/:slug (dynamic)
  dashboard/
    layout.tsx                      # Shared dashboard layout
    page.tsx                        # /dashboard
    settings/page.tsx               # /dashboard/settings
  (marketing)/                      # Route group (no URL segment)
    pricing/page.tsx                # /pricing
```

### Dynamic Routes

| Pattern | File Path | URL Match |
|---------|-----------|-----------|
| Dynamic segment | `[id]/page.tsx` | `/users/123` |
| Catch-all | `[...slug]/page.tsx` | `/docs/a/b/c` |
| Optional catch-all | `[[...slug]]/page.tsx` | `/docs` or `/docs/a/b` |

### Server vs Client Components

- Pages are Server Components by default
- Add `'use client'` directive only when using: `useState`, `useEffect`, `onClick`, browser APIs
- Pass data from server to client via props, not through context

## Next.js Pages Router (Legacy)

### File Conventions

```
pages/
  index.tsx                         # /
  about.tsx                         # /about
  blog/index.tsx                    # /blog
  blog/[slug].tsx                   # /blog/:slug
  _app.tsx                          # App wrapper (layouts)
  _document.tsx                     # HTML document customization
  404.tsx                           # Custom 404 page
  api/users.ts                      # API route: /api/users
```

### Data Fetching

| Method | When | Use Case |
|--------|------|----------|
| `getServerSideProps` | Every request | Dynamic data, auth-gated pages |
| `getStaticProps` | Build time | Blog posts, marketing pages |
| `getStaticPaths` | Build time | Dynamic routes with static generation |

## React Router (v6+)

### Route Definition

```typescript
// router.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorBoundary />,
    children: [
      { index: true, element: <Home /> },
      {
        path: 'dashboard',
        element: <Suspense fallback={<Loading />}><Dashboard /></Suspense>,
      },
      {
        path: 'users/:id',
        element: <UserProfile />,
        loader: userLoader,
      },
    ],
  },
]);
```

### Layout Pattern

```typescript
// layouts/RootLayout.tsx
import { Outlet } from 'react-router-dom';

export function RootLayout() {
  return (
    <div>
      <Header />
      <main>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
```

## Protected Routes

### Pattern: Auth Guard Component

```typescript
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <LoadingSkeleton />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  return <>{children}</>;
}
```

### App Router: Middleware

```typescript
// middleware.ts (project root)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session');
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*'] };
```

## Error Boundaries

Every page route should have an error boundary:

- App Router: `error.tsx` file in route segment (automatically client component)
- React Router: `errorElement` prop on route definition
- Fallback: Generic `ErrorBoundary` component wrapping page content

Include retry functionality and user-friendly error message. Log error details to console (placeholder for error reporting service).
