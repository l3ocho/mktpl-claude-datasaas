---
name: schema-inference
description: Infer data types, constraints, and relationships from ORM models or raw SQL DDL
---

# Schema Inference

## Purpose

Parse and normalize schema definitions from multiple ORM dialects into a unified internal representation. This skill enables data generation and validation commands to work across SQLAlchemy, Prisma, Django ORM, and raw SQL DDL without dialect-specific logic in every command.

---

## Supported Schema Sources

| Source | Detection | File Patterns |
|--------|-----------|---------------|
| SQLAlchemy | `from sqlalchemy import`, `Column(`, `mapped_column(` | `models.py`, `models/*.py` |
| Prisma | `model` blocks with `@id`, `@relation` | `prisma/schema.prisma` |
| Django ORM | `from django.db import models`, `models.CharField` | `models.py` with Django imports |
| Raw SQL DDL | `CREATE TABLE` statements | `*.sql`, `schema.sql`, `migrations/*.sql` |
| JSON Schema | `"type": "object"`, `"properties":` | `*.schema.json` |

## Type Normalization

Map dialect-specific types to a canonical set:

| Canonical Type | SQLAlchemy | Prisma | Django | SQL |
|----------------|------------|--------|--------|-----|
| `string` | `String(N)`, `Text` | `String` | `CharField`, `TextField` | `VARCHAR(N)`, `TEXT` |
| `integer` | `Integer`, `BigInteger`, `SmallInteger` | `Int`, `BigInt` | `IntegerField`, `BigIntegerField` | `INT`, `BIGINT`, `SMALLINT` |
| `float` | `Float`, `Numeric` | `Float` | `FloatField` | `FLOAT`, `REAL`, `DOUBLE` |
| `decimal` | `Numeric(P,S)` | `Decimal` | `DecimalField` | `DECIMAL(P,S)`, `NUMERIC(P,S)` |
| `boolean` | `Boolean` | `Boolean` | `BooleanField` | `BOOLEAN`, `BIT` |
| `datetime` | `DateTime` | `DateTime` | `DateTimeField` | `TIMESTAMP`, `DATETIME` |
| `date` | `Date` | `DateTime` | `DateField` | `DATE` |
| `uuid` | `UUID` | `String @default(uuid())` | `UUIDField` | `UUID` |
| `json` | `JSON` | `Json` | `JSONField` | `JSON`, `JSONB` |
| `enum` | `Enum(...)` | `enum` block | `choices=` | `ENUM(...)`, `CHECK IN (...)` |

## Constraint Extraction

For each column, extract:
- **nullable**: Whether NULL values are allowed (default: true unless PK or explicit NOT NULL)
- **unique**: Whether values must be unique
- **max_length**: For string types, the maximum character length
- **precision/scale**: For decimal types
- **default**: Default value expression
- **check**: CHECK constraint expressions (e.g., `age >= 0`)
- **primary_key**: Whether this column is part of the primary key

## Relationship Extraction

Identify foreign key relationships:
- **parent_table**: The referenced table
- **parent_column**: The referenced column (usually PK)
- **on_delete**: CASCADE, SET NULL, RESTRICT, NO ACTION
- **self_referential**: True if FK references same table
- **many_to_many**: Detected from junction/through tables with two FKs and no additional non-FK columns

## Output Format

Internal representation used by other skills:

```json
{
  "tables": {
    "users": {
      "columns": {
        "id": {"type": "integer", "primary_key": true, "nullable": false},
        "email": {"type": "string", "max_length": 255, "unique": true, "nullable": false},
        "name": {"type": "string", "max_length": 100, "nullable": false},
        "manager_id": {"type": "integer", "nullable": true, "foreign_key": {"table": "users", "column": "id"}}
      },
      "relationships": [
        {"type": "self_referential", "column": "manager_id", "references": "users.id"}
      ]
    }
  }
}
```
