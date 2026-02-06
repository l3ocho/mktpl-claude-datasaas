---
name: release setup
description: Detect version locations, release conventions, and configure release workflow
---

# /release setup

Setup wizard for release management. Detects existing version locations and release conventions.

## Visual Output

```
+----------------------------------------------------------------------+
|  RELEASE-MANAGER - Setup                                              |
+----------------------------------------------------------------------+
```

## Skills to Load

- skills/version-detection.md

## Process

1. **Detect Version Locations**
   - Scan for version strings in standard files:
     - `package.json` (Node.js)
     - `pyproject.toml` (Python)
     - `setup.cfg`, `setup.py` (Python legacy)
     - `Cargo.toml` (Rust)
     - `marketplace.json` (Claude plugins)
     - `README.md` title line
     - `CHANGELOG.md` header
   - Record each location with current version value

2. **Check Version Consistency**
   - Compare all detected versions
   - Flag any mismatches between files
   - Identify the "source of truth" file

3. **Detect Release Conventions**
   - Git tags: check `git tag` for existing pattern (v1.0.0 vs 1.0.0)
   - Branching: check for release/* branches
   - Changelog format: detect Keep a Changelog vs other
   - CI/CD: check for release workflows in .github/workflows or .gitlab-ci.yml

4. **Present Configuration**
   - Show detected settings
   - Ask user to confirm or override
   - Store preferences for future commands

## Output Format

```
## Release Configuration

### Version Locations
| File | Current Version | Pattern |
|------|----------------|---------|
| package.json | 2.3.1 | "version": "X.Y.Z" |
| README.md | 2.3.1 | # Project - vX.Y.Z |
| CHANGELOG.md | 2.3.1 | ## [X.Y.Z] - YYYY-MM-DD |

### Conventions
- Tag format: vX.Y.Z
- Branch pattern: release/X.Y.Z
- Changelog: Keep a Changelog format
- Source of truth: package.json

### Status: Ready
All versions in sync. Release workflow configured.
```
