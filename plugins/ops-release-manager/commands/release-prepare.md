---
name: release prepare
description: Prepare a release — bump versions across all files, update changelog, create release branch
---

# /release prepare

Prepare a new release by bumping version numbers, updating the changelog, and optionally creating a release branch.

## Visual Output

```
+----------------------------------------------------------------------+
|  RELEASE-MANAGER - Prepare Release                                    |
+----------------------------------------------------------------------+
```

## Usage

```
/release prepare <version|bump-type> [--branch] [--no-branch]
```

**Version:** Explicit version (e.g., `2.4.0`) or bump type (`major`, `minor`, `patch`)
**--branch:** Create a release/X.Y.Z branch (default for minor/major)
**--no-branch:** Skip branch creation

## Skills to Load

- skills/version-detection.md
- skills/semver-rules.md
- skills/changelog-conventions.md

## Process

1. **Determine Target Version**
   - If explicit version: validate it follows SemVer
   - If bump type: calculate from current version
     - `patch`: 2.3.1 -> 2.3.2
     - `minor`: 2.3.1 -> 2.4.0
     - `major`: 2.3.1 -> 3.0.0
   - If no argument: analyze commits since last tag, suggest bump type

2. **Pre-flight Checks**
   - Working directory is clean (no uncommitted changes)
   - On correct base branch (development or main)
   - [Unreleased] section in CHANGELOG.md has content
   - All tests passing (if CI status available)

3. **Update Version Files**
   - Update all detected version locations (from setup)
   - Show diff for each file before applying
   - Maintain format consistency (quotes, spacing)

4. **Update Changelog**
   - Replace `[Unreleased]` with `[X.Y.Z] - YYYY-MM-DD`
   - Add new empty `[Unreleased]` section above
   - Update comparison links at bottom if present

5. **Create Release Branch** (if applicable)
   - Branch name: `release/X.Y.Z`
   - Commit all version changes
   - Commit message: `chore(release): prepare vX.Y.Z`

6. **Summary**
   - List all files modified
   - Show the new version
   - Next steps: review, validate, then tag

## Output Format

```
## Release Preparation: v2.4.0

### Files Updated
- package.json: 2.3.1 -> 2.4.0
- README.md: v2.3.1 -> v2.4.0
- CHANGELOG.md: [Unreleased] -> [2.4.0] - 2026-02-06

### Branch
- Created: release/2.4.0
- Commit: chore(release): prepare v2.4.0

### Next Steps
1. Review changes: `git diff development`
2. Validate: `/release validate`
3. Tag: `/release tag`
```
