---
name: release status
description: Show current version, unreleased changes, and release readiness
---

# /release status

Display the current version, unreleased changes, and overall release readiness.

## Visual Output

```
+----------------------------------------------------------------------+
|  RELEASE-MANAGER - Status                                             |
+----------------------------------------------------------------------+
```

## Usage

```
/release status [--verbose]
```

**--verbose:** Include full unreleased changelog and commit list

## Skills to Load

- skills/version-detection.md
- skills/semver-rules.md

## Process

1. **Current Version**
   - Read version from all known locations
   - Show the latest git tag
   - Flag any version mismatches

2. **Unreleased Changes**
   - Read [Unreleased] section from CHANGELOG.md
   - Count entries by category (Added, Changed, Fixed, etc.)
   - If verbose: show full content

3. **Commit Analysis**
   - List commits since last tag
   - Parse conventional commit prefixes (feat, fix, chore, etc.)
   - Suggest bump type based on commit types:
     - Any `BREAKING CHANGE` or `!` → major
     - Any `feat` → minor
     - Only `fix`, `chore`, `docs` → patch
   - If verbose: show commit list

4. **Readiness Assessment**
   - Check if [Unreleased] has content
   - Check if all versions are in sync
   - Check git state (clean working directory)
   - Summarize blockers if any

## Output Format

```
## Release Status

### Current Version: 2.3.1 (tag: v2.3.1)
All 3 version locations in sync.

### Unreleased Changes
| Category | Count |
|----------|-------|
| Added | 3 |
| Fixed | 2 |
| Changed | 1 |

### Commits Since v2.3.1: 14
- 5 feat (new features)
- 6 fix (bug fixes)
- 3 chore (maintenance)

### Suggested Bump: MINOR (2.3.1 -> 2.4.0)
Reason: 5 new features detected

### Readiness: READY
- [x] Unreleased changes documented
- [x] Versions in sync
- [x] Working directory clean
Run `/release prepare minor` to begin.
```
