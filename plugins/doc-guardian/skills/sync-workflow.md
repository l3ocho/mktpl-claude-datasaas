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

## Queue File

Location: `.doc-guardian-queue` in project root

Format:
```
# Doc Guardian Queue
# Generated: YYYY-MM-DD HH:MM:SS

## Pending Updates
- README.md:45 | reference | calculate_total -> compute_total
- CLAUDE.md:23 | version | Python 3.9 -> 3.11
- src/api/README.md:12 | path | old/path.py -> new/path.py
```

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

1. **Review Queue**
   - Read `.doc-guardian-queue`
   - List all pending items

2. **Batch Updates**
   - Apply each update
   - Track in change list

3. **Commit Strategy**
   - Stage all doc changes together
   - Single commit: `docs: sync documentation with code changes`
   - Include summary in commit body

4. **Clear Queue**
   ```bash
   echo "# Doc Guardian Queue - cleared after sync on $(date +%Y-%m-%d)" > .doc-guardian-queue
   ```

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
