---
name: api validate
description: Validate routes against OpenAPI specification
agent: api-validator
---

# /api validate - OpenAPI Validation

## Skills to Load

- skills/openapi-conventions.md
- skills/route-patterns.md
- skills/visual-header.md

## Visual Output

Display header: `API-PLATFORM - Validate`

## Usage

```
/api validate [--spec=<path>] [--strict]
```

**Arguments:**
- `--spec`: Path to OpenAPI spec file (default: auto-detect `openapi.yaml` or `openapi.json`)
- `--strict`: Treat warnings as errors

## Prerequisites

Run `/api setup` first. Requires an existing OpenAPI specification to validate against.

## Process

### 1. Locate OpenAPI Spec

Search for spec file in order:
1. Path provided via `--spec` flag
2. `openapi.yaml` in project root
3. `openapi.json` in project root
4. `swagger.yaml` or `swagger.json` in project root
5. `docs/openapi.yaml` or `docs/openapi.json`

If not found, report error and suggest `/api docs` to generate one.

### 2. Parse Route Definitions

Scan route files to extract implemented endpoints:
- HTTP method and path pattern
- Path parameters and query parameters
- Request body schema (if POST/PUT/PATCH)
- Response status codes and schemas
- Authentication requirements

### 3. Compare Against Spec

Run validation checks:

| Check | Severity | Description |
|-------|----------|-------------|
| Missing endpoint in spec | FAIL | Route exists in code but not in OpenAPI spec |
| Missing endpoint in code | FAIL | Spec defines endpoint not implemented |
| Parameter mismatch | FAIL | Path/query parameters differ between code and spec |
| Schema mismatch | WARN | Request/response model fields differ from spec |
| Missing response codes | WARN | Code returns status codes not documented in spec |
| Missing descriptions | INFO | Endpoints or parameters lack descriptions |
| Missing examples | INFO | Spec lacks request/response examples |
| Deprecated endpoint still active | WARN | Spec marks endpoint deprecated but code still serves it |

### 4. Generate Report

Group findings by severity and provide actionable fixes.

## Output Format

```
+----------------------------------------------------------------------+
|  API-PLATFORM - Validate                                             |
+----------------------------------------------------------------------+

Spec: openapi.yaml (OpenAPI 3.0.3)
Routes Scanned: 14 endpoints in 4 files
Spec Endpoints: 16 defined

FINDINGS

FAIL (2)
  1. [POST /v1/orders] Missing from OpenAPI spec
     Fix: Add path definition to openapi.yaml

  2. [GET /v1/users] Query param 'role' not in spec
     Fix: Add 'role' query parameter to path definition

WARN (3)
  1. [PUT /v1/products/{id}] Response 422 not documented
     Fix: Add 422 response to spec with validation error schema

  2. [GET /v1/orders] Schema mismatch - 'total_amount' field
     Code: float, Spec: string
     Fix: Update spec to use number type

  3. [DELETE /v1/users/{id}] Marked deprecated in spec
     Suggestion: Remove endpoint or update spec status

INFO (1)
  1. [GET /v1/products] Missing response example
     Suggestion: Add example to improve documentation

SUMMARY
  Endpoints:  14 implemented / 16 in spec
  Coverage:   87.5%
  FAIL:       2 (must fix)
  WARN:       3 (should fix)
  INFO:       1 (improve)

VERDICT: FAIL (2 blocking issues)
```

## Exit Guidance

- FAIL findings: Block deployment, spec and code must agree
- WARN findings: Fix before release for accurate documentation
- INFO findings: Improve for developer experience
- `--strict` mode: All WARN become FAIL
