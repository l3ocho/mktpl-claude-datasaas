---
description: Synchronize current machine state with existing NetBox record
---

# CMDB Machine Sync

Update an existing NetBox device record with the current machine state.

## Skills to Load

- `skills/visual-header.md`
- `skills/sync-workflow.md`
- `skills/system-discovery.md`
- `skills/mcp-tools-reference.md`

## Usage

```
/cmdb-sync [--full] [--dry-run]
```

**Options:**
- `--full`: Force refresh all fields, even unchanged ones
- `--dry-run`: Show what would change without applying updates

## Instructions

Execute `skills/visual-header.md` with context "Machine Sync".

Execute `skills/sync-workflow.md` which covers:
1. Device lookup via MCP
2. Current state discovery via Bash
3. Comparison of NetBox vs local state
4. Diff report generation
5. User confirmation (unless dry-run)
6. Apply updates via MCP
7. Journal entry creation

## Modes

| Mode | Behavior |
|------|----------|
| Default | Show diff, ask confirmation, apply changes |
| `--dry-run` | Show diff only, no changes applied |
| `--full` | Skip confirmation, update all fields |

## Error Handling

| Error | Action |
|-------|--------|
| Device not found | Suggest `/cmdb-register` |
| Permission denied | Note which failed, continue others |
| Cluster not found | Offer to create or skip container sync |

## User Request

$ARGUMENTS
