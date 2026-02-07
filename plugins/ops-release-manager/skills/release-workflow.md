---
description: Release patterns, branching strategies, tagging, and pre-release versions
---

# Release Workflow Skill

## Overview

End-to-end release workflow patterns including branching, tagging, and rollback procedures.

## Release Patterns

### Tag-Based Release (Simple)
Best for: small projects, continuous deployment

1. Commit changes to main/development
2. Update version files and changelog
3. Create annotated tag: `git tag -a vX.Y.Z -m "message"`
4. Push tag: `git push origin vX.Y.Z`
5. CI triggers deployment from tag

### Branch-Based Release (Standard)
Best for: projects with QA cycles, staged releases

1. Create branch: `git checkout -b release/X.Y.Z`
2. Update version files and changelog on branch
3. QA testing on release branch
4. Merge to main: `git merge release/X.Y.Z`
5. Tag on main: `git tag -a vX.Y.Z`
6. Merge back to development: `git merge release/X.Y.Z`
7. Delete release branch

## Git Tag Operations

### Creating Tags
```bash
# Annotated tag with release notes
git tag -a vX.Y.Z -m "Release vX.Y.Z

Added:
- Feature description

Fixed:
- Bug fix description"

# Push single tag
git push origin vX.Y.Z

# Push all tags
git push origin --tags
```

### Deleting Tags (Rollback)
```bash
# Delete local tag
git tag -d vX.Y.Z

# Delete remote tag
git push origin :refs/tags/vX.Y.Z
```

## Pre-Release Workflow

For releases that need staged rollout:

1. `vX.Y.Z-alpha.1` — First alpha, feature incomplete
2. `vX.Y.Z-alpha.2` — Updated alpha
3. `vX.Y.Z-beta.1` — Feature complete, testing
4. `vX.Y.Z-rc.1` — Release candidate, final validation
5. `vX.Y.Z` — Stable release

Each pre-release tag follows the same tagging process but does not update the main changelog section.

## Rollback Procedure

### If Tag Not Yet Pushed
1. Delete local tag
2. Revert version commit
3. Done

### If Tag Already Pushed
1. Delete remote tag
2. Delete local tag
3. Revert version commit
4. Push revert commit
5. Notify team about release revert

### If Deployment Occurred
1. Follow the above steps
2. Trigger deployment of the previous version
3. Verify rollback in production
4. Post-mortem on what went wrong

## Safety Rules

- Never force-push tags without explicit user confirmation
- Always create annotated tags (not lightweight)
- Include release notes in tag message
- Verify tag points to expected commit before pushing
