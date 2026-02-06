---
name: release tag
description: Create annotated git tag with release notes extracted from changelog
---

# /release tag

Create and push an annotated git tag with release notes from the changelog.

## Visual Output

```
+----------------------------------------------------------------------+
|  RELEASE-MANAGER - Tag Release                                        |
+----------------------------------------------------------------------+
```

## Usage

```
/release tag [--push] [--draft]
```

**--push:** Push tag to remote immediately (default: ask)
**--draft:** Create tag locally without pushing

## Skills to Load

- skills/release-workflow.md

## Process

1. **Pre-flight**
   - Verify `/release validate` passes (run automatically if not done)
   - Confirm current version from version files
   - Check that tag does not already exist

2. **Extract Release Notes**
   - Read the current version's section from CHANGELOG.md
   - Format as tag annotation body
   - Include version number and date in tag message

3. **Create Tag**
   - Tag name: `vX.Y.Z` (matching project convention)
   - Annotated tag with release notes as message
   - Command: `git tag -a vX.Y.Z -m "Release vX.Y.Z\n\n<release notes>"`

4. **Push Decision**
   - If --push: push tag to origin
   - If --draft: keep local only
   - Otherwise: show tag details and ask user

5. **Post-Tag Actions**
   - If release branch exists: remind to merge back and delete branch
   - If CI release pipeline detected: note it will be triggered
   - Show the complete release summary

## Output Format

```
## Release Tagged: v2.4.0

### Tag
- Name: v2.4.0
- Commit: abc1234 (HEAD)
- Date: 2026-02-06

### Release Notes
#### Added
- New feature X
- New feature Y

#### Fixed
- Bug fix Z

### Status: Tag created locally
Run `git push origin v2.4.0` to publish.

### Post-Release
- [ ] Merge release/2.4.0 back to development
- [ ] Delete release/2.4.0 branch
- [ ] Verify CI pipeline triggered
```
