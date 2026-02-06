---
name: relationship-resolution
description: Foreign key resolution, dependency ordering, and circular dependency handling for seed data
---

# Relationship Resolution

## Purpose

Determine the correct order for generating and inserting seed data across tables with foreign key dependencies. Handle edge cases including circular dependencies, self-referential relationships, and many-to-many through tables.

---

## Dependency Graph Construction

### Step 1: Extract Foreign Keys
For each table, identify all columns with foreign key constraints:
- Direct FK references to other tables
- Self-referential FKs (same table)
- Composite FKs spanning multiple columns

### Step 2: Build Directed Graph
- Each table is a node
- Each FK creates a directed edge: child -> parent (child depends on parent)
- Self-referential edges are noted but excluded from ordering (handled separately)

### Step 3: Topological Sort
- Apply topological sort to determine insertion order
- Tables with no dependencies come first
- Tables depending on others come after their dependencies
- Result: ordered list where every table's dependencies appear before it

## Insertion Order Example

Given schema:
```
users (no FK)
categories (no FK)
products (FK -> categories)
orders (FK -> users)
order_items (FK -> orders, FK -> products)
reviews (FK -> users, FK -> products)
```

Insertion order: `users, categories, products, orders, order_items, reviews`

Deletion order (reverse): `reviews, order_items, orders, products, categories, users`

## Circular Dependency Handling

When topological sort detects a cycle:

### Strategy 1: Nullable FK Deferral
If one FK in the cycle is nullable:
1. Insert rows with nullable FK set to NULL
2. Complete the cycle for the other table
3. UPDATE the nullable FK to point to the now-existing rows

Example: `departments.manager_id -> employees`, `employees.department_id -> departments`
1. Insert departments with `manager_id = NULL`
2. Insert employees referencing departments
3. UPDATE departments to set `manager_id` to an employee

### Strategy 2: Deferred Constraints
If database supports deferred constraints (PostgreSQL):
1. Set FK constraints to DEFERRED within transaction
2. Insert all rows in any order
3. Constraints checked at COMMIT time

### Strategy 3: Two-Pass Generation
If neither strategy works:
1. First pass: generate all rows without cross-cycle FK values
2. Second pass: update FK values to reference generated rows from the other table

## Self-Referential Relationships

Common pattern: `employees.manager_id -> employees.id`

### Generation Strategy
1. Generate root rows first (manager_id = NULL) — these are top-level managers
2. Generate second tier referencing root rows
3. Generate remaining rows referencing any previously generated row
4. Depth distribution controlled by profile (default: max depth 3, pyramid shape)

### Configuration
```json
{
  "self_ref_null_ratio": 0.1,
  "self_ref_max_depth": 3,
  "self_ref_distribution": "pyramid"
}
```

## Many-to-Many Through Tables

Detection: a table with exactly two FK columns and no non-FK data columns (excluding PK and timestamps).

### Generation Strategy
1. Generate both parent tables first
2. Generate through table rows pairing random parents
3. Respect uniqueness on the (FK1, FK2) composite — no duplicate pairings
4. Density controlled by profile: sparse (10% of possible pairs), medium (30%), dense (60%)

## Deletion Order

When `--clean` is specified for `/seed apply`:
1. Reverse the insertion order
2. TRUNCATE or DELETE in this order to avoid FK violations
3. For circular dependencies: disable FK checks, truncate, re-enable (with user confirmation)

## Error Handling

| Scenario | Response |
|----------|----------|
| Unresolvable cycle (no nullable FKs, no deferred constraints) | FAIL: report cycle, suggest schema modification |
| Missing parent table in schema | FAIL: report orphaned FK reference |
| FK references non-existent column | FAIL: report schema inconsistency |
| Through table detection false positive | WARN: ask user to confirm junction table identification |
