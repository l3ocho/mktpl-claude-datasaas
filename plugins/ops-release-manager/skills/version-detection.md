---
description: Detect version locations across project files and parse current version
---

# Version Detection Skill

## Overview

Find and parse version strings from all standard locations in a project. Supports multiple language ecosystems.

## Detection Targets

### Node.js / JavaScript
| File | Pattern | Example |
|------|---------|---------|
| `package.json` | `"version": "X.Y.Z"` | `"version": "2.3.1"` |
| `package-lock.json` | `"version": "X.Y.Z"` (root) | `"version": "2.3.1"` |

### Python
| File | Pattern | Example |
|------|---------|---------|
| `pyproject.toml` | `version = "X.Y.Z"` | `version = "2.3.1"` |
| `setup.cfg` | `version = X.Y.Z` | `version = 2.3.1` |
| `setup.py` | `version="X.Y.Z"` | `version="2.3.1"` |
| `__version__.py` | `__version__ = "X.Y.Z"` | `__version__ = "2.3.1"` |

### Rust
| File | Pattern | Example |
|------|---------|---------|
| `Cargo.toml` | `version = "X.Y.Z"` | `version = "2.3.1"` |

### Claude Marketplace
| File | Pattern | Example |
|------|---------|---------|
| `marketplace.json` | `"version": "X.Y.Z"` | `"version": "2.3.1"` |
| `plugin.json` | `"version": "X.Y.Z"` | `"version": "2.3.1"` |

### Documentation
| File | Pattern | Example |
|------|---------|---------|
| `README.md` | Title containing `vX.Y.Z` | `# Project - v2.3.1` |
| `CHANGELOG.md` | `## [X.Y.Z]` | `## [2.3.1] - 2026-01-15` |

## Git Tags

Parse existing tags to determine latest released version:
- `git tag --sort=-v:refname` — list tags by version
- Support both `vX.Y.Z` and `X.Y.Z` formats
- Detect the project's tag convention from existing tags

## Version Parsing

Extract and validate SemVer components:
- Major, Minor, Patch (required)
- Pre-release identifier (optional): `-alpha.1`, `-beta.2`, `-rc.1`
- Build metadata (optional): `+build.123`

Report any versions that do not conform to SemVer.
