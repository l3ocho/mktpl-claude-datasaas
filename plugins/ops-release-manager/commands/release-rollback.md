---
name: release rollback
description: Revert a release — remove git tag, revert version bump commit, restore previous state
---

# /release rollback

Revert a release by removing the git tag and reverting version bump changes.

## Visual Output

```
+----------------------------------------------------------------------+
|  RELEASE-MANAGER - Rollback Release                                   |
+----------------------------------------------------------------------+
```

## Usage

```
/release rollback [<version>] [--tag-only] [--force]
```

**Version:** Version to rollback (defaults to latest tag)
**--tag-only:** Only remove the tag, keep version changes
**--force:** Skip confirmation prompts

## Skills to Load

- skills/release-workflow.md

## Process

1. **Identify Release to Rollback**
   - If version specified: find matching tag
   - If not specified: use most recent tag
   - Show the release details for confirmation

2. **Safety Checks**
   - Warn if tag has been pushed to remote
   - Warn if other branches have been based on this release
   - Warn if CI pipeline has already deployed
   - Require explicit confirmation (unless --force)

3. **Remove Git Tag**
   - Delete local tag: `git tag -d vX.Y.Z`
   - If tag was pushed: `git push origin :refs/tags/vX.Y.Z`
   - Confirm tag removal

4. **Revert Version Changes** (unless --tag-only)
   - Find the version bump commit
   - Create a revert commit: `git revert <commit> --no-edit`
   - This restores CHANGELOG.md, version files to previous state

5. **Cleanup**
   - If release branch exists: offer to delete it
   - Update any tracking references
   - Show final state

## Output Format

```
## Rollback: v2.4.0

### Actions Taken
- [x] Deleted local tag v2.4.0
- [x] Deleted remote tag v2.4.0
- [x] Reverted commit abc1234 (chore(release): prepare v2.4.0)
- [x] Deleted branch release/2.4.0

### Current State
- Version: 2.3.1 (restored)
- Latest tag: v2.3.1
- CHANGELOG.md: [Unreleased] section restored

### Warnings
- If any deployments were triggered, manual rollback may be needed
- Notify team members of the release revert
```
