---
name: sync-workflow
description: Documentation synchronization process and queue management
---

# Sync Workflow

## Purpose

Defines how to synchronize documentation with code changes.

## When to Use

- **doc sync**: Apply pending documentation updates
- **doc audit**: Detect drift manually (PostToolUse hook removed per Decision #29)

---

## Drift Detection

Run `/doc audit` to detect documentation drift. The audit produces a list of files and changes that need synchronization. Use those results as input to the sync process below.

> **Note:** The queue file (`.doc-guardian-queue`) was removed in v8.1.0 when the PostToolUse hook was deleted (Decision #29). Drift detection is now manual via `/doc audit`.

---

## Update Types

### Reference Fixes
- Renamed function/class: update all doc references
- Changed signature: update parameter documentation
- Removed item: remove or mark deprecated in docs

### Content Sync
- Version numbers (Python, Node, dependencies)
- Configuration keys/values
- File paths and directory structures
- Command examples and outputs

### Structural
- Add missing sections for new features
- Remove sections for deleted features
- Reorder to match current code organization

---

## Sync Process

1. **Review Drift Results**
   - Use output from `/doc audit`
   - List all items needing sync

2. **Batch Updates**
   - Apply each update
   - Track in change list

3. **Commit Strategy**
   - Stage all doc changes together
   - Single commit: `docs: sync documentation with code changes`
   - Include summary in commit body

---

## Output Format

```
## Documentation Sync Complete

### Files Updated
- README.md (3 changes)
- CLAUDE.md (1 change)
- src/api/README.md (2 changes)

### Changes Applied
- Updated function reference: calculate_total -> compute_total
- Updated Python version: 3.9 -> 3.11
- Added docstring to create_order()

Committed: abc123f
```

---

## Queue Entry Format

```
<file>:<line> | <type> | <old> -> <new>
```

Types:
- `reference` - Function/class name change
- `version` - Version number update
- `path` - File path change
- `config` - Configuration key/value
- `missing` - New documentation needed
