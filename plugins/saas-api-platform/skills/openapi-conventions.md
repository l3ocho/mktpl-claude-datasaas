---
name: openapi-conventions
description: OpenAPI 3.x spec generation rules, path naming, schema definitions, response codes
---

# OpenAPI Conventions

## Purpose

Defines rules and patterns for generating and validating OpenAPI 3.x specifications. This skill ensures consistency between generated specs and industry best practices.

---

## Specification Structure

An OpenAPI 3.0.3 document must include:

```yaml
openapi: "3.0.3"
info:
  title: <project name>
  version: <project version>
  description: <project description>
servers:
  - url: <base url>
    description: <environment name>
paths:
  /<resource>: ...
components:
  schemas: ...
  securitySchemes: ...
tags: ...
```

---

## Path Naming Rules

| Rule | Example | Anti-Pattern |
|------|---------|-------------|
| Plural nouns for collections | `/users` | `/user`, `/getUsers` |
| Lowercase with hyphens | `/order-items` | `/orderItems`, `/order_items` |
| Resource ID in path | `/users/{user_id}` | `/users?id=123` |
| Nested resources max 2 levels | `/users/{id}/orders` | `/users/{id}/orders/{oid}/items/{iid}` |
| No verbs in paths | `/users` + POST | `/createUser` |
| Version prefix when configured | `/v1/users` | `/api/v1/users` (redundant) |

---

## Response Code Standards

| Method | Success | Client Error | Server Error |
|--------|---------|-------------|-------------|
| GET (single) | 200 | 404 | 500 |
| GET (list) | 200 | 400 (bad params) | 500 |
| POST | 201 | 400, 409 (conflict), 422 | 500 |
| PUT | 200 | 400, 404, 422 | 500 |
| PATCH | 200 | 400, 404, 422 | 500 |
| DELETE | 204 | 404 | 500 |

All endpoints should also document 401 (unauthorized) and 403 (forbidden) when auth is required.

---

## Schema Definition Rules

1. **Naming**: PascalCase for schema names (`UserCreate`, `OrderResponse`)
2. **Reuse**: Use `$ref` for shared schemas instead of duplication
3. **Required fields**: Explicitly list required fields; do not rely on defaults
4. **Types**: Use specific types (`integer` not `number` for IDs; `string` with `format: date-time` for timestamps)
5. **Descriptions**: Every property should have a `description` field
6. **Examples**: Include `example` values for key properties
7. **Nullable**: Use `nullable: true` explicitly when fields can be null

---

## Pagination Schema

List endpoints must return a paginated wrapper:

```yaml
PaginatedResponse:
  type: object
  properties:
    items:
      type: array
      items:
        $ref: '#/components/schemas/ResourceResponse'
    total:
      type: integer
      description: Total number of items
    page:
      type: integer
      description: Current page number
    page_size:
      type: integer
      description: Items per page
    pages:
      type: integer
      description: Total number of pages
```

---

## Security Scheme Patterns

**JWT Bearer:**
```yaml
securitySchemes:
  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

**API Key:**
```yaml
securitySchemes:
  ApiKeyAuth:
    type: apiKey
    in: header
    name: X-API-Key
```

Apply globally or per-operation using the `security` field.
