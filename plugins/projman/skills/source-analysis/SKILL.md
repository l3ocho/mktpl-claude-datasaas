---
description: Framework for analyzing existing codebases and systems as input to project initiation
---

# Source Analysis

## Purpose

Structured approach to analyzing an existing codebase or system before project planning. Used by `/project initiation` to understand what exists before defining what to build.

## Analysis Framework

### 1. Codebase Discovery
- Technology stack identification (languages, frameworks, databases, ORMs)
- Architecture pattern recognition (monolith, microservices, modular monolith)
- Dependency inventory (package managers, versions, lock files)
- Environment configuration (env files, config patterns, secrets management)

### 2. Feature Inventory
- User-facing features (pages, flows, API endpoints)
- Admin/internal features (dashboards, tools, scripts)
- Integration points (third-party APIs, external services)
- Background processes (cron jobs, workers, queues)

### 3. Data Model Analysis
- Database schemas and relationships
- Data migration history
- Seed data patterns
- Data validation rules

### 4. Quality Assessment
- Test coverage (types, frameworks, CI integration)
- Documentation state (README, inline, API docs)
- Code quality indicators (linting, formatting, type safety)
- Known technical debt (TODO/FIXME/HACK comments)

### 5. Deployment Assessment
- Current hosting/infrastructure
- CI/CD pipeline state
- Environment parity (dev/staging/prod)
- Monitoring and logging

## Output Format

The analysis produces a structured report stored as a wiki page (`Project: {Name}`) that feeds into the project charter and epic decomposition.

## DO NOT

- Make assumptions about missing components — document gaps explicitly
- Evaluate "good vs bad" — document facts for decision-making
- Propose solutions during analysis — that's the planning phase
