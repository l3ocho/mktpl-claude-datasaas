---
name: test fixtures
description: Generate or manage test fixtures, factories, and mock data
---

# /test fixtures

Generate and organize test fixtures, factories, and mock data.

## Visual Output

```
+----------------------------------------------------------------------+
|  TEST-PILOT - Fixtures                                                |
+----------------------------------------------------------------------+
```

## Usage

```
/test fixtures <action> [<target>]
```

**Actions:**
- `generate <model/schema>` — Create fixture/factory for a data model
- `list` — Show existing fixtures and their usage
- `audit` — Find unused or duplicate fixtures
- `organize` — Restructure fixtures into standard layout

## Skills to Load

- skills/fixture-management.md
- skills/mock-patterns.md

## Process

### Generate

1. **Analyze Target Model**
   - Read model/schema definition (ORM model, Pydantic, TypeScript interface)
   - Map field types, constraints, and relationships
   - Identify required vs optional fields

2. **Create Fixture**
   - Python: generate conftest.py fixture or factory_boy factory
   - JavaScript: generate factory function or test helper
   - Include realistic sample data (not just "test123")
   - Handle relationships (foreign keys, nested objects)
   - Create variants (minimal, full, edge-case)

3. **Place Fixture**
   - Follow project conventions for fixture location
   - Add to appropriate conftest.py or fixtures directory
   - Import from shared location, not duplicated per test

### List

1. Scan test directories for fixture definitions
2. Map each fixture to its consumers (which tests use it)
3. Display fixture tree with usage counts

### Audit

1. Find fixtures with zero consumers
2. Detect duplicate/near-duplicate fixtures
3. Identify fixtures with hardcoded data that should be parameterized

## Output Format

```
## Fixture: UserFactory

### Generated for: models.User
### Location: tests/conftest.py

### Variants
- user_factory() — standard user with defaults
- admin_factory() — user with is_admin=True
- minimal_user() — only required fields

### Fields
| Field | Type | Default | Notes |
|-------|------|---------|-------|
| email | str | faker.email() | unique |
| name | str | faker.name() | — |
| role | enum | "viewer" | — |
```
