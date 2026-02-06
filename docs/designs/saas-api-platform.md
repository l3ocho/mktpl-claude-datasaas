# Design: saas-api-platform

**Domain:** `saas`
**Target Version:** v9.1.0

## Purpose

Provides scaffolding, validation, and development workflow tools for REST and GraphQL API backends. Supports FastAPI (Python) and Express (Node.js) with OpenAPI spec generation, route validation, and middleware management.

## Target Users

- Backend developers building API services
- Teams using FastAPI or Express frameworks
- Projects requiring OpenAPI/Swagger documentation

## Commands

| Command | Description |
|---------|-------------|
| `/api setup` | Setup wizard — detect framework, configure MCP server |
| `/api scaffold` | Generate API routes, models, schemas from spec or description |
| `/api validate` | Validate routes against OpenAPI spec, check missing endpoints |
| `/api docs` | Generate/update OpenAPI spec from code annotations |
| `/api test-routes` | Generate request/response test cases for API endpoints |
| `/api middleware` | Add/configure middleware (auth, CORS, rate-limiting, logging) |

## Agent Architecture

| Agent | Model | Mode | Role |
|-------|-------|------|------|
| `api-architect` | sonnet | default | Route design, schema generation, middleware planning |
| `api-validator` | haiku | plan | Read-only validation of routes against spec |

## Skills

| Skill | Purpose |
|-------|---------|
| `framework-detection` | Detect FastAPI vs Express, identify project structure |
| `openapi-conventions` | OpenAPI 3.x spec generation rules and patterns |
| `route-patterns` | RESTful route naming, versioning, pagination conventions |
| `middleware-catalog` | Common middleware patterns per framework |
| `visual-header` | Standard command output headers |

## MCP Server

**Not required.** All operations are file-based (reading/writing code and specs). No external API needed.

## Integration Points

| Plugin | Integration |
|--------|-------------|
| projman | Issue labels: `Component/API`, `Tech/FastAPI`, `Tech/Express` |
| code-sentinel | PreToolUse hook scans generated routes for security issues |
| saas-test-pilot | `/api test-routes` generates stubs consumable by test-pilot |
| saas-db-migrate | Schema models shared between API models and migrations |

## Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| `claude-md-integration.md` | ~800 |
| Dispatch file (`api.md`) | ~200 |
| 6 commands (avg) | ~3,600 |
| 2 agents | ~1,200 |
| 5 skills | ~2,500 |
| **Total** | **~8,300** |

## Open Questions

- Should MCP server be added later for live API testing (curl-like requests)?
- Support for gRPC/tRPC in addition to REST/GraphQL?
