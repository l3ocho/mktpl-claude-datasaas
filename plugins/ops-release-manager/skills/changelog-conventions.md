---
description: Keep a Changelog format, Unreleased section management, and category ordering
---

# Changelog Conventions Skill

## Overview

Standards for maintaining a changelog following the Keep a Changelog format (keepachangelog.com). The changelog is the primary release communication artifact.

## File Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com),
and this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added
- New features go here during development

## [2.3.1] - 2026-01-15

### Fixed
- Bug fix description

## [2.3.0] - 2026-01-01

### Added
- Feature description

[Unreleased]: https://github.com/user/repo/compare/v2.3.1...HEAD
[2.3.1]: https://github.com/user/repo/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/user/repo/releases/tag/v2.3.0
```

## Category Ordering

Categories must appear in this order (only include categories with entries):

1. **Added** — New features
2. **Changed** — Changes to existing functionality
3. **Deprecated** — Features that will be removed in future
4. **Removed** — Features removed in this release
5. **Fixed** — Bug fixes
6. **Security** — Security vulnerability fixes

## Unreleased Section Management

### During Development
All changes go under `[Unreleased]`. Never create a versioned section until release time.

### At Release Time
1. Replace `[Unreleased]` heading with `[X.Y.Z] - YYYY-MM-DD`
2. Add new empty `[Unreleased]` section above
3. Update comparison links at bottom of file

### Entry Writing Guidelines
- Start with a verb (Add, Fix, Change, Remove, Deprecate)
- Focus on user impact, not implementation details
- Reference issue numbers where applicable
- Keep entries concise (one line preferred)
- Group related changes into a single entry when appropriate

## Comparison Links

Maintain comparison links at the bottom of the file:
- `[Unreleased]` compares latest tag to HEAD
- Each version compares to the previous version
- First version links to the release tag
