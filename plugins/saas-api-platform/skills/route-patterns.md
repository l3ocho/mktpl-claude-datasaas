---
name: route-patterns
description: RESTful naming, versioning, pagination, filtering, and sorting conventions
---

# Route Patterns

## Purpose

Defines standard patterns for RESTful route design. This skill is loaded during scaffolding and validation to ensure generated routes follow consistent, industry-standard conventions.

---

## RESTful Resource Naming

| Pattern | URL | Method | Purpose |
|---------|-----|--------|---------|
| List | `/{resource}` | GET | Retrieve paginated collection |
| Create | `/{resource}` | POST | Create new resource |
| Get | `/{resource}/{id}` | GET | Retrieve single resource |
| Replace | `/{resource}/{id}` | PUT | Full replacement of resource |
| Update | `/{resource}/{id}` | PATCH | Partial update |
| Delete | `/{resource}/{id}` | DELETE | Remove resource |

### Nested Resources

For parent-child relationships (max 2 levels deep):

| Pattern | URL | Example |
|---------|-----|---------|
| Child list | `/{parent}/{parent_id}/{child}` | `/users/42/orders` |
| Child create | `/{parent}/{parent_id}/{child}` | POST `/users/42/orders` |
| Child get | `/{parent}/{parent_id}/{child}/{child_id}` | `/users/42/orders/7` |

Beyond 2 levels, flatten with query filters: `/items?order_id=7&user_id=42`

---

## Versioning

| Strategy | Format | Example |
|----------|--------|---------|
| URL prefix (recommended) | `/v{N}/` | `/v1/users`, `/v2/users` |
| Header-based | `Accept: application/vnd.api.v1+json` | Header value |
| Query param (discouraged) | `?version=1` | `/users?version=1` |

URL prefix versioning is the default. Only bump major version for breaking changes.

---

## Pagination

All list endpoints must support pagination:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (1-indexed) |
| `page_size` | integer | 20 | Items per page (max 100) |

Response must include pagination metadata:
```json
{
  "items": [...],
  "total": 142,
  "page": 2,
  "page_size": 20,
  "pages": 8
}
```

---

## Filtering

Use query parameters for filtering:

| Pattern | Example | Description |
|---------|---------|-------------|
| Exact match | `?status=active` | Field equals value |
| Multiple values | `?status=active,pending` | Field in list |
| Range | `?created_after=2024-01-01&created_before=2024-12-31` | Date/number range |
| Search | `?q=search+term` | Full-text search |

---

## Sorting

| Parameter | Format | Example |
|-----------|--------|---------|
| `sort` | `field` (asc) or `-field` (desc) | `?sort=-created_at` |
| Multiple | Comma-separated | `?sort=-created_at,name` |

---

## Error Response Format

All errors must use a consistent structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ],
    "request_id": "abc-123"
  }
}
```

Error codes should be uppercase snake_case constants: `NOT_FOUND`, `UNAUTHORIZED`, `VALIDATION_ERROR`, `CONFLICT`, `INTERNAL_ERROR`.
