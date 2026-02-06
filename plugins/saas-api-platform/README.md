# saas-api-platform

REST and GraphQL API scaffolding, validation, and documentation for FastAPI and Express.

## Overview

The saas-api-platform plugin provides a complete API development toolkit. It detects your framework, generates routes and models following RESTful conventions, validates implemented endpoints against OpenAPI specifications, and manages middleware configuration.

## Supported Frameworks

- **FastAPI** (Python) - Pydantic models, dependency injection, async endpoints
- **Express** (Node.js/TypeScript) - Router patterns, Zod/Joi validation, middleware chains

## Commands

| Command | Description |
|---------|-------------|
| `/api setup` | Setup wizard - detect framework, map project structure |
| `/api scaffold <resource>` | Generate CRUD routes, models, and schemas |
| `/api validate` | Validate routes against OpenAPI specification |
| `/api docs` | Generate or update OpenAPI 3.x specification from code |
| `/api test-routes` | Generate test cases for API endpoints |
| `/api middleware <type>` | Add and configure middleware (auth, CORS, rate-limit, etc.) |

## Agents

| Agent | Model | Mode | Purpose |
|-------|-------|------|---------|
| `api-architect` | sonnet | default | Route design, schema generation, middleware planning |
| `api-validator` | haiku | plan (read-only) | OpenAPI compliance validation |

## Installation

This plugin is part of the Leo Claude Marketplace. It is installed automatically when the marketplace is configured.

### Prerequisites

- A FastAPI or Express project to work with
- Run `/api setup` before using other commands

## Configuration

The `/api setup` command creates `.api-platform.json` in your project root with detected settings. All subsequent commands read this file for framework and convention configuration.
