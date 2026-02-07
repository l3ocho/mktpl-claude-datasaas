---
name: doc sync
description: Synchronize all pending documentation updates in a single commit
---

# /doc sync

Apply all pending documentation updates detected by `/doc audit`.

## Skills to Load

- skills/sync-workflow.md
- skills/drift-detection.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Documentation Sync                               |
+------------------------------------------------------------------+
```

## Process

1. **Detect Drift**
   Run `/doc audit` first (or use its most recent results) to identify documentation that is out of sync with code.

2. **Batch Updates**
   For each drift item:
   - Show the specific change needed
   - Apply the update
   - Track in change list

3. **Commit Strategy**
   - Stage all doc changes together
   - Single commit: `docs: sync documentation with code changes`
   - Include summary in commit body

4. **Output**
   Use format from `skills/sync-workflow.md`
