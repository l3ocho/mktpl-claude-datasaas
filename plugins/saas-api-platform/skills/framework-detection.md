---
name: framework-detection
description: Detect FastAPI vs Express, identify project structure, locate route files and models
---

# Framework Detection

## Purpose

Identify the API framework in use and map the project structure. This skill is loaded by the `api-architect` agent during setup and code generation to ensure framework-appropriate output.

---

## Detection Rules

### FastAPI Detection

| Indicator | Location | Confidence |
|-----------|----------|------------|
| `from fastapi import` in Python files | `*.py` | High |
| `fastapi` in `requirements.txt` | Project root | Medium |
| `fastapi` in `pyproject.toml` dependencies | Project root | Medium |
| `uvicorn` in requirements alongside fastapi | Project root | High |
| `@app.get`, `@router.post` decorators | `*.py` | High |

**FastAPI Project Structure (typical):**
```
app/
  __init__.py
  main.py              # FastAPI app instance, middleware, router includes
  routes/              # Route modules (one per resource)
  models/              # Pydantic models (request/response schemas)
  dependencies/        # Dependency injection functions
  middleware/           # Custom middleware
  core/                # Config, security, database setup
```

### Express Detection

| Indicator | Location | Confidence |
|-----------|----------|------------|
| `express` in `package.json` dependencies | Project root | High |
| `require('express')` or `import express` | `*.js`, `*.ts` | High |
| `express.Router()` usage | `*.js`, `*.ts` | High |
| `tsconfig.json` present alongside Express | Project root | Express+TS variant |

**Express Project Structure (typical):**
```
src/
  app.js or app.ts     # Express app instance, middleware, router mounts
  routes/              # Route modules (one per resource)
  models/              # Database models (Sequelize, Mongoose, etc.)
  schemas/             # Validation schemas (Zod, Joi)
  middleware/           # Custom middleware
  config/              # Environment config, database setup
```

---

## Project Mapping Procedure

1. **Check package files first**: `requirements.txt`, `pyproject.toml`, `package.json`
2. **Scan entry points**: `main.py`, `app.py`, `app.js`, `app.ts`, `index.js`, `index.ts`
3. **Locate route directory**: Search for `routes/`, `routers/`, `controllers/`, `api/`
4. **Locate model directory**: Search for `models/`, `schemas/`, `entities/`
5. **Locate test directory**: Search for `tests/`, `test/`, `__tests__/`, `spec/`
6. **Check for existing OpenAPI spec**: `openapi.yaml`, `openapi.json`, `swagger.*`

---

## Framework Version Detection

**FastAPI**: Parse version from `requirements.txt` pin or `pyproject.toml` constraint. Important for feature availability (e.g., `lifespan` parameter in 0.93+).

**Express**: Parse version from `package.json` dependencies. Important for middleware compatibility (Express 4 vs 5).

---

## Ambiguous Projects

If both FastAPI and Express indicators are found (monorepo), ask the user which service to target. Store the selection in `.api-platform.json` with a `service_root` field pointing to the specific service directory.
