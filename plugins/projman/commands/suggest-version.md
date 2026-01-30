---
description: Analyze CHANGELOG.md and suggest appropriate semantic version bump
---

# Suggest Version

Analyze CHANGELOG.md and suggest appropriate semantic version bump.

## Behavior

1. **Read current state**:
   - Read `CHANGELOG.md` to find current version and [Unreleased] content
   - Read `.claude-plugin/marketplace.json` for current marketplace version
   - Check individual plugin versions in `plugins/*/. claude-plugin/plugin.json`

2. **Analyze [Unreleased] section**:
   - Extract all entries under `### Added`, `### Changed`, `### Fixed`, `### Removed`, `### Deprecated`
   - Categorize changes by impact

3. **Apply SemVer rules**:

   | Change Type | Version Bump | Indicators |
   |-------------|--------------|------------|
   | **MAJOR** (X.0.0) | Breaking changes | `### Removed`, `### Changed` with "BREAKING:", renamed/removed APIs |
   | **MINOR** (x.Y.0) | New features, backwards compatible | `### Added` with new commands/plugins/features |
   | **PATCH** (x.y.Z) | Bug fixes only | `### Fixed` only, `### Changed` for non-breaking tweaks |

4. **Output recommendation**:
   ```
   ## Version Analysis

   **Current version:** X.Y.Z
   **[Unreleased] summary:**
   - Added: N entries (new features/plugins)
   - Changed: N entries (M breaking)
   - Fixed: N entries
   - Removed: N entries

   **Recommendation:** MINOR bump → X.(Y+1).0
   **Reason:** New features added without breaking changes

   **To release:** ./scripts/release.sh X.Y.Z
   ```

5. **Check version sync**:
   - Compare marketplace version with individual plugin versions
   - Warn if plugins are out of sync (e.g., marketplace 4.0.0 but projman 3.1.0)

## Examples

**Output when MINOR bump needed:**
```
## Version Analysis

**Current version:** 4.0.0
**[Unreleased] summary:**
- Added: 3 entries (new command, hook improvement, workflow example)
- Changed: 1 entry (0 breaking)
- Fixed: 2 entries

**Recommendation:** MINOR bump → 4.1.0
**Reason:** New features (Added section) without breaking changes

**To release:** ./scripts/release.sh 4.1.0
```

**Output when nothing to release:**
```
## Version Analysis

**Current version:** 4.0.0
**[Unreleased] summary:** Empty - no pending changes

**Recommendation:** No release needed
```

## Visual Output

When executing this command, display the plugin header:

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  Version Analysis                                                ║
╚══════════════════════════════════════════════════════════════════╝
```

Then proceed with the version analysis.

## Integration

This command helps maintain proper versioning workflow:
- Run after completing a sprint to determine version bump
- Run before `/sprint-close` to ensure version is updated
- Integrates with `./scripts/release.sh` for actual release execution
