---
name: api docs
description: Generate or update OpenAPI specification from code
agent: api-architect
---

# /api docs - OpenAPI Specification Generator

## Skills to Load

- skills/openapi-conventions.md
- skills/framework-detection.md
- skills/visual-header.md

## Visual Output

Display header: `API-PLATFORM - Docs`

## Usage

```
/api docs [--format=yaml|json] [--output=<path>] [--update]
```

**Arguments:**
- `--format`: Output format, default `yaml`
- `--output`: Output file path (default: `openapi.yaml` or `openapi.json` in project root)
- `--update`: Update existing spec instead of regenerating from scratch

## Process

### 1. Scan Route Definitions

Read all route files identified during `/api setup`:

**FastAPI:**
- Parse `@app.get`, `@app.post`, `@router.get`, etc. decorators
- Extract path, method, response_model, status_code, dependencies
- Read Pydantic model definitions for schema extraction
- Capture docstrings as endpoint descriptions

**Express:**
- Parse `router.get`, `router.post`, etc. calls
- Extract path patterns and middleware chains
- Read Zod/Joi/JSON Schema validators for schema extraction
- Capture JSDoc comments as endpoint descriptions

### 2. Build OpenAPI Document

Generate OpenAPI 3.x specification:

- **Info section**: Title from package name, version from package config
- **Servers**: Extract from environment or configuration
- **Paths**: One entry per endpoint with method, parameters, request body, responses
- **Components/Schemas**: Extracted from model/schema definitions
- **Security schemes**: Based on detected auth patterns (JWT, API key, OAuth2)
- **Tags**: Group endpoints by resource/router prefix

### 3. Handle Updates (--update mode)

When updating existing spec:
- Preserve manually-added descriptions, examples, and extensions
- Add new endpoints not yet in spec
- Flag removed endpoints for user review (do not auto-delete)
- Update schemas that changed in code
- Show diff of changes before writing

### 4. Write Output

Write the generated or updated spec to the target file.

## Output Format

```
+----------------------------------------------------------------------+
|  API-PLATFORM - Docs                                                 |
+----------------------------------------------------------------------+

Mode: Generate (new)
Format: YAML
Output: ./openapi.yaml

Extracted:
  Routes:     14 endpoints from 4 files
  Schemas:    8 models extracted
  Auth:       JWT Bearer scheme detected
  Tags:       users, orders, products, auth

OpenAPI 3.0.3 spec written to openapi.yaml

Sections Generated:
  [+] info          (title, version, description)
  [+] servers       (1 server)
  [+] paths         (14 operations)
  [+] components    (8 schemas, 1 security scheme)
  [+] tags          (4 tags)

Next Steps:
  - Review generated spec for accuracy
  - Add examples to request/response bodies
  - Run /api validate to verify consistency
```

## Important Notes

- Generated spec is a starting point; review and enrich with examples
- Descriptions are extracted from docstrings when available
- Complex schemas (inheritance, unions) may need manual adjustment
- The `--update` flag preserves manual additions to the spec
