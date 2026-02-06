---
name: profile-management
description: Seed profile definitions with row counts, edge case ratios, and custom value overrides
---

# Profile Management

## Purpose

Define and manage reusable seed data profiles that control how much data is generated, what edge cases are included, and what custom overrides apply. Profiles enable reproducible, consistent test data across environments.

---

## Profile Storage

Profiles are stored in `seed-profiles.json` in the configured output directory (default: `seeds/` or `fixtures/`).

## Profile Schema

```json
{
  "profiles": [
    {
      "name": "profile-name",
      "description": "Human-readable description",
      "default_rows": 100,
      "table_overrides": {
        "table_name": 200
      },
      "edge_case_ratio": 0.1,
      "null_ratio": 0.05,
      "locale": "en_US",
      "seed_value": 42,
      "custom_values": {
        "table.column": ["value1", "value2", "value3"]
      },
      "relationship_density": {
        "many_to_many": 0.3,
        "self_ref_max_depth": 3
      }
    }
  ],
  "default_profile": "medium"
}
```

## Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique profile identifier (lowercase, hyphens allowed) |
| `description` | string | No | What this profile is for |
| `default_rows` | integer | Yes | Row count for tables without explicit override |
| `table_overrides` | object | No | Per-table row count overrides |
| `edge_case_ratio` | float | No | Fraction of rows with edge case values (0.0 to 1.0, default 0.1) |
| `null_ratio` | float | No | Fraction of nullable columns set to null (0.0 to 1.0, default 0.05) |
| `locale` | string | No | Faker locale for name/address generation (default "en_US") |
| `seed_value` | integer | No | Random seed for reproducibility (default: hash of profile name) |
| `custom_values` | object | No | Column-specific value pools (table.column -> array of values) |
| `relationship_density` | object | No | Controls many-to-many fill ratio and self-referential depth |

## Built-in Profiles

### small
- `default_rows`: 10
- `edge_case_ratio`: 0.0
- `null_ratio`: 0.0
- Use case: unit tests, schema validation, quick smoke tests
- Characteristics: minimal data, no edge cases, all required fields populated

### medium
- `default_rows`: 100
- `edge_case_ratio`: 0.1
- `null_ratio`: 0.05
- Use case: development, manual testing, demo environments
- Characteristics: realistic volume, occasional edge cases, some nulls

### large
- `default_rows`: 1000
- `edge_case_ratio`: 0.05
- `null_ratio`: 0.03
- Use case: performance testing, pagination testing, stress testing
- Characteristics: high volume, lower edge case ratio to avoid noise

## Custom Value Overrides

Override the faker generator for specific columns with a weighted value pool:

```json
{
  "custom_values": {
    "users.role": ["user", "user", "user", "admin"],
    "orders.status": ["completed", "completed", "pending", "cancelled", "refunded"],
    "products.currency": ["USD"]
  }
}
```

Values are selected randomly with replacement. Duplicate entries in the array increase that value's probability (e.g., "user" appears 3x = 75% probability).

## Profile Operations

### Resolution Order
When determining row count for a table:
1. Command-line `--rows` flag (highest priority)
2. Profile `table_overrides` for that specific table
3. Profile `default_rows`
4. Built-in default: 100

### Validation Rules
- Profile name must be unique within `seed-profiles.json`
- `default_rows` must be >= 1
- `edge_case_ratio` must be between 0.0 and 1.0
- `null_ratio` must be between 0.0 and 1.0
- Custom value arrays must not be empty
- Cannot delete the last remaining profile
