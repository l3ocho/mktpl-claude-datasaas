---
name: release validate
description: Pre-release validation — verify version consistency, changelog, dependencies, and readiness
---

# /release validate

Run pre-release checks to verify the project is ready for release.

## Visual Output

```
+----------------------------------------------------------------------+
|  RELEASE-MANAGER - Validate Release                                   |
+----------------------------------------------------------------------+
```

## Skills to Load

- skills/version-detection.md
- skills/changelog-conventions.md

## Process

1. **Version Consistency**
   - Read version from all known locations
   - Verify all locations report the same version
   - Check version is greater than the latest git tag
   - Verify version follows SemVer format

2. **Changelog Validation**
   - Verify [X.Y.Z] section exists with today's date (or recent date)
   - Check all required categories are present if entries exist
   - Verify no empty [Unreleased] content was left behind
   - Check comparison links are updated

3. **Git State**
   - Working directory is clean
   - Branch is up to date with remote
   - No merge conflicts pending
   - All CI checks passing (if detectable)

4. **Dependency Check**
   - Lock file is up to date (package-lock.json, poetry.lock, Cargo.lock)
   - No known vulnerable dependencies (if audit tool available)
   - No unpinned dependencies in production config

5. **Documentation**
   - README references correct version
   - Migration guide exists for major versions
   - Breaking changes are documented

6. **Report**
   - Show pass/fail for each check
   - Block release if any critical check fails
   - Warn on non-critical issues

## Output Format

```
## Release Validation: v2.4.0

### Checks
| Check | Status | Details |
|-------|--------|---------|
| Version consistency | PASS | 3/3 files match v2.4.0 |
| Changelog | PASS | [2.4.0] section with 5 entries |
| Git state | PASS | Clean, up to date |
| Lock file | PASS | package-lock.json current |
| Dependencies | WARN | 1 advisory (low severity) |
| Documentation | PASS | README updated |

### Result: READY FOR RELEASE
1 warning (non-blocking). Proceed with `/release tag`.
```
