# /git-status - Enhanced Status

## Purpose

Show comprehensive git status with recommendations and insights.

## Behavior

### Output Format

```
═══════════════════════════════════════════
Git Status: <repo-name>
═══════════════════════════════════════════

Branch: feat/password-reset
Base: development (3 commits ahead, 0 behind)
Remote: origin/feat/password-reset (synced)

─── Changes ───────────────────────────────

Staged (ready to commit):
  ✓ src/auth/reset.ts (modified)
  ✓ src/auth/types.ts (modified)

Unstaged:
  • tests/auth.test.ts (modified)
  • src/utils/email.ts (new file, untracked)

─── Recommendations ───────────────────────

1. Stage test file: git add tests/auth.test.ts
2. Consider adding new file: git add src/utils/email.ts
3. Ready to commit with 2 staged files

─── Quick Actions ─────────────────────────

• /commit - Commit staged changes
• /commit-push - Commit and push
• /commit-sync - Full sync with development

═══════════════════════════════════════════
```

## Analysis Provided

### Branch Health
- Commits ahead/behind base branch
- Sync status with remote
- Age of branch

### Change Categories
- Staged (ready to commit)
- Modified (not staged)
- Untracked (new files)
- Deleted
- Renamed

### Recommendations
- What to stage
- What to ignore
- When to commit
- When to sync

### Warnings
- Large number of changes (consider splitting)
- Old branch (consider rebasing)
- Conflicts with upstream

## Output

Always produces the formatted status report with context-aware recommendations.
