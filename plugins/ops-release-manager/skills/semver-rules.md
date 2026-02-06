---
description: Semantic versioning bump logic and conventional commit analysis
---

# SemVer Rules Skill

## Overview

Rules for determining the correct version bump based on the nature of changes, following Semantic Versioning 2.0.0 (semver.org).

## Bump Type Rules

### MAJOR (X.0.0)
Increment when making incompatible API changes:
- Removing a public function, class, or endpoint
- Changing function signatures (parameter types, return types)
- Renaming public exports
- Changing default behavior in a breaking way
- Dropping support for a platform or runtime version

### MINOR (x.Y.0)
Increment when adding functionality in a backwards-compatible manner:
- Adding new functions, classes, or endpoints
- Adding optional parameters to existing functions
- New configuration options with sensible defaults
- Deprecating functionality (without removing it)
- Performance improvements that do not change behavior

### PATCH (x.y.Z)
Increment when making backwards-compatible bug fixes:
- Fixing incorrect behavior
- Correcting documentation errors that affected usage
- Security patches that do not change API
- Fixing edge cases or error handling

## Conventional Commits Mapping

| Commit Prefix | Bump Type | Examples |
|---------------|-----------|---------|
| `feat:` | MINOR | New feature, new command, new option |
| `fix:` | PATCH | Bug fix, error correction |
| `docs:` | PATCH | Documentation update |
| `chore:` | PATCH | Dependency update, cleanup |
| `refactor:` | PATCH | Internal restructuring, no behavior change |
| `perf:` | PATCH | Performance improvement |
| `test:` | PATCH | Test additions or fixes |
| `BREAKING CHANGE:` | MAJOR | Any commit with this footer |
| `feat!:` / `fix!:` | MAJOR | Breaking change indicated by `!` |

## Pre-release Versions

For releases not yet stable:
- Alpha: `X.Y.Z-alpha.N` — feature incomplete, unstable
- Beta: `X.Y.Z-beta.N` — feature complete, testing
- Release Candidate: `X.Y.Z-rc.N` — ready for release, final testing

Pre-release versions have lower precedence than the normal version:
`1.0.0-alpha.1 < 1.0.0-beta.1 < 1.0.0-rc.1 < 1.0.0`

## Decision Flow

1. Any breaking changes? -> MAJOR
2. Any new features? -> MINOR
3. Only fixes and maintenance? -> PATCH
4. When in doubt, ask the user
