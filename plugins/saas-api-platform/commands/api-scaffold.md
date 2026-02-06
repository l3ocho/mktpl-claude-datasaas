---
name: api scaffold
description: Generate API routes, models, and schemas
agent: api-architect
---

# /api scaffold - Route and Model Scaffolding

## Skills to Load

- skills/framework-detection.md
- skills/route-patterns.md
- skills/openapi-conventions.md
- skills/visual-header.md

## Visual Output

Display header: `API-PLATFORM - Scaffold`

## Usage

```
/api scaffold <resource-name> [--methods=GET,POST,PUT,DELETE] [--nested-under=<parent>]
```

**Arguments:**
- `<resource-name>`: Name of the resource (e.g., `users`, `orders`, `products`)
- `--methods`: Comma-separated HTTP methods (default: all CRUD)
- `--nested-under`: Create as nested resource under parent (e.g., `--nested-under=users`)

## Prerequisites

Run `/api setup` first. This command reads `.api-platform.json` for framework and conventions.

## Process

### 1. Read Configuration

Load `.api-platform.json` to determine:
- Target framework (FastAPI or Express)
- Route and model directories
- Versioning scheme
- Response format conventions

### 2. Generate Route File

Create route/controller file with endpoints:

**FastAPI Example (`routes/{resource}.py`):**
- `GET /{version}/{resource}` - List with pagination, filtering, sorting
- `GET /{version}/{resource}/{id}` - Get by ID with 404 handling
- `POST /{version}/{resource}` - Create with request body validation
- `PUT /{version}/{resource}/{id}` - Full update with 404 handling
- `PATCH /{version}/{resource}/{id}` - Partial update
- `DELETE /{version}/{resource}/{id}` - Delete with 204 response

**Express Example (`routes/{resource}.js`):**
- Same endpoints adapted to Express router patterns
- Includes error handling middleware chain

### 3. Generate Request/Response Models

Create schema definitions appropriate to the framework:

- **FastAPI**: Pydantic models in `models/{resource}.py`
  - `{Resource}Create` - POST/PUT request body
  - `{Resource}Update` - PATCH request body (all fields optional)
  - `{Resource}Response` - Response model with `id`, timestamps
  - `{Resource}List` - Paginated list wrapper

- **Express**: JSON Schema or Zod schemas in `schemas/{resource}.js`
  - Create schema, Update schema, Response schema

### 4. Generate Validation Schemas

Add input validation:
- Required fields, type constraints, string length limits
- Enum values where appropriate
- Nested object validation for complex resources

### 5. Register Routes

Update the main router/app file to include new routes:
- Add import statement
- Register route prefix
- Maintain alphabetical ordering of imports

## Output Format

```
+----------------------------------------------------------------------+
|  API-PLATFORM - Scaffold                                             |
+----------------------------------------------------------------------+

Resource: orders
Framework: FastAPI
Versioning: /v1/

Files Created:
  [+] app/routes/orders.py      (6 endpoints)
  [+] app/models/orders.py      (4 Pydantic models)
  [~] app/main.py               (route registered)

Endpoints Generated:
  GET    /v1/orders              List with pagination
  GET    /v1/orders/{id}         Get by ID
  POST   /v1/orders              Create
  PUT    /v1/orders/{id}         Full update
  PATCH  /v1/orders/{id}         Partial update
  DELETE /v1/orders/{id}         Delete

Next Steps:
  - Add business logic to route handlers
  - Run /api validate to check against OpenAPI spec
  - Run /api test-routes to generate test cases
```

## Nested Resources

When `--nested-under` is specified:
- Routes are prefixed: `/{parent}/{parent_id}/{resource}`
- Models include `{parent}_id` foreign key field
- Route file includes parent ID path parameter validation
