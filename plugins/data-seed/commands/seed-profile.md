---
name: seed profile
---

# /seed profile - Manage Data Profiles

## Skills to Load
- skills/profile-management.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-SEED - Profile Management`

## Usage

```
/seed profile list
/seed profile show <name>
/seed profile create <name>
/seed profile edit <name>
/seed profile delete <name>
```

## Workflow

### list — Show All Profiles
- Read `seed-profiles.json` from configured output directory
- Display table: name, row counts per table, edge case ratio, description
- Highlight the default profile

### show — Profile Details
- Display full profile definition including:
  - Per-table row counts
  - Edge case configuration (null ratio, boundary values, unicode strings)
  - Custom value overrides per column
  - Locale settings
  - Relationship density settings

### create — New Profile
- Ask user for profile name and description
- Ask for base row count (applies to all tables unless overridden)
- Ask for per-table overrides (optional)
- Ask for edge case ratio (0.0 = no edge cases, 1.0 = all edge cases)
- Ask for custom column overrides (e.g., `users.role` always "admin")
- Save to `seed-profiles.json`

### edit — Modify Profile
- Load existing profile, display current values
- Allow user to modify any field interactively
- Save updated profile

### delete — Remove Profile
- Confirm deletion with user
- Cannot delete the last remaining profile
- Remove from `seed-profiles.json`

## Profile Schema

```json
{
  "name": "medium",
  "description": "Realistic dataset for development and manual testing",
  "default_rows": 100,
  "table_overrides": {
    "users": 50,
    "orders": 200,
    "order_items": 500
  },
  "edge_case_ratio": 0.1,
  "null_ratio": 0.05,
  "locale": "en_US",
  "custom_values": {
    "users.status": ["active", "active", "active", "inactive"],
    "users.role": ["user", "user", "user", "admin"]
  }
}
```

## Built-in Profiles

| Profile | Rows | Edge Cases | Use Case |
|---------|------|------------|----------|
| `small` | 10 | 0% | Unit tests, quick validation |
| `medium` | 100 | 10% | Development, manual testing |
| `large` | 1000 | 5% | Performance testing, stress testing |
