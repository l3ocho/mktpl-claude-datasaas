---
description: Synchronize all pending documentation updates in a single commit
---

# Documentation Sync

Apply all pending documentation updates detected by doc-guardian hooks.

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  📝 DOC-GUARDIAN · Documentation Sync                            │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the sync.

## Process

1. **Review Pending Queue**
   List all documentation drift detected during this session.

2. **Batch Updates**
   For each pending item:
   - Show the specific change needed
   - Apply the update
   - Track in change list

3. **Update Types**

   **Reference Fixes:**
   - Renamed function/class → update all doc references
   - Changed signature → update parameter documentation
   - Removed item → remove or mark deprecated in docs

   **Content Sync:**
   - Version numbers (Python, Node, dependencies)
   - Configuration keys/values
   - File paths and directory structures
   - Command examples and outputs

   **Structural:**
   - Add missing sections for new features
   - Remove sections for deleted features
   - Reorder to match current code organization

4. **Commit Strategy**
   - Stage all doc changes together
   - Single commit: `docs: sync documentation with code changes`
   - Include summary of what was updated in commit body

5. **Output**
```
## Documentation Sync Complete

### Files Updated
- README.md (3 changes)
- CLAUDE.md (1 change)
- src/api/README.md (2 changes)

### Changes Applied
- Updated function reference: calculate_total → compute_total
- Updated Python version: 3.9 → 3.11
- Added docstring to create_order()

Committed: abc123f
```
