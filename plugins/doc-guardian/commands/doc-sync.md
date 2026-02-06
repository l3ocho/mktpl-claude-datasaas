---
name: doc sync
description: Synchronize all pending documentation updates in a single commit
---

# /doc sync

Apply all pending documentation updates detected by doc-guardian hooks.

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

1. **Review Pending Queue**
   Execute `skills/sync-workflow.md` - read `.doc-guardian-queue`

2. **Batch Updates**
   For each pending item:
   - Show the specific change needed
   - Apply the update
   - Track in change list

3. **Commit Strategy**
   - Stage all doc changes together
   - Single commit: `docs: sync documentation with code changes`
   - Include summary in commit body

4. **Clear Queue**
   After successful sync, clear the queue file

5. **Output**
   Use format from `skills/sync-workflow.md`
