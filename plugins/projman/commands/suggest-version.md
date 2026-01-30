---
description: Analyze CHANGELOG.md and suggest appropriate semantic version bump
---

# Suggest Version

## Purpose

Analyze CHANGELOG.md and suggest appropriate semantic version bump.

## Invocation

Run `/suggest-version` after updating CHANGELOG or before release.

## Workflow

1. **Read Current State**
   - CHANGELOG.md for current version and [Unreleased] content
   - marketplace.json for marketplace version
   - Individual plugin versions

2. **Analyze [Unreleased] Section**
   - Extract entries under Added, Changed, Fixed, Removed, Deprecated
   - Categorize changes by impact

3. **Apply SemVer Rules**

| Change Type | Bump | Indicators |
|-------------|------|------------|
| MAJOR (X.0.0) | Breaking changes | Removed, "BREAKING:" in Changed |
| MINOR (x.Y.0) | New features | Added with new commands/plugins |
| PATCH (x.y.Z) | Bug fixes only | Fixed only |

4. **Output Recommendation**
   - Current version
   - Summary of changes
   - Recommended bump with reason
   - Release command

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  Version Analysis                                                ║
╚══════════════════════════════════════════════════════════════════╝
```
