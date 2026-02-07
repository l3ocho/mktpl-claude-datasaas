---
name: api setup
description: Setup wizard for saas-api-platform
agent: api-architect
---

# /api setup - API Platform Setup Wizard

## Skills to Load

- skills/framework-detection.md
- skills/visual-header.md

## Visual Output

Display header: `API-PLATFORM - Setup Wizard`

## Usage

```
/api setup
```

## Workflow

### Phase 1: Framework Detection

Scan the project root for framework indicators:

| File / Pattern | Framework | Confidence |
|----------------|-----------|------------|
| `main.py` with `from fastapi` | FastAPI | High |
| `app.py` with `from fastapi` | FastAPI | High |
| `requirements.txt` containing `fastapi` | FastAPI | Medium |
| `pyproject.toml` with `fastapi` dependency | FastAPI | Medium |
| `package.json` with `express` dependency | Express | High |
| `app.js` or `app.ts` with `require('express')` | Express | High |
| `tsconfig.json` + express in deps | Express (TypeScript) | High |

If no framework detected, ask user to select one.

### Phase 2: Project Structure Mapping

Identify existing project layout:

- **Route files**: Locate route/controller directories
- **Models**: Locate model/schema definition files
- **Middleware**: Locate existing middleware
- **Tests**: Locate test directories and test runner config
- **OpenAPI spec**: Check for existing `openapi.yaml`, `openapi.json`, or `swagger.json`

Report findings to user with directory tree.

### Phase 3: Convention Configuration

Ask user about project conventions:

- **Route style**: RESTful nested (`/users/{id}/posts`) vs flat (`/user-posts`)
- **Versioning**: URL prefix (`/v1/`) vs header-based vs none
- **Auth pattern**: JWT, OAuth2, API key, or none
- **Response format**: JSON:API, HAL, plain JSON

Store decisions in `.api-platform.json` in project root for future commands.

### Phase 4: Validation

Verify detected configuration:

- Confirm framework version
- Confirm route directory location
- Confirm model directory location
- Display summary with all detected settings

## Output Format

```
+----------------------------------------------------------------------+
|  API-PLATFORM - Setup Wizard                                         |
+----------------------------------------------------------------------+

Framework:     FastAPI 0.104.1
Route Dir:     ./app/routes/
Models Dir:    ./app/models/
Tests Dir:     ./tests/
OpenAPI Spec:  ./openapi.yaml (existing)

Conventions:
  Versioning:  /v1/ URL prefix
  Auth:        JWT Bearer
  Response:    Plain JSON

Configuration saved to .api-platform.json
```

## Important Notes

- This command does NOT create project files; it only detects and configures
- If `.api-platform.json` already exists, offer to update or keep existing
- All subsequent commands rely on setup configuration
