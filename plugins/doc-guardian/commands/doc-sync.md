---
name: doc sync
description: [doc-guardian] Synchronize all pending documentation updates in a single commit
---

# /doc sync

Apply all pending documentation updates detected by `/doc audit`.

## Skills to Load

- skills/doc-standards/SKILL.md
- skills/sync-workflow/SKILL.md
- skills/drift-detection/SKILL.md

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
   For each drift item, apply fixes that respect the `doc-standards` skill:
   - When updating a section, preserve the standard section hierarchy
   - When fixing a link, use the standard's link format rules (relative paths, no heading anchors)
   - When adding documentation for new code, generate it in the standard's structure (full doc vs. directory README as appropriate)
   - When a directory README's Contents table is stale, regenerate it to match actual folder contents (folders first alphabetical, then files)
   - When detecting an orphan custom doc (no code/process/decision mapping), prompt the user: "This doc appears to have no code or process it describes. Link it to a code path, or delete it?" — do not auto-delete.
   - Show the specific change needed before applying it
   - Track each update in the change list

3. **Commit Strategy**
   - Stage all doc changes together
   - Single commit: `docs: sync documentation with code changes`
   - Include summary in commit body

4. **Output**
   Use format from `skills/sync-workflow/SKILL.md`
