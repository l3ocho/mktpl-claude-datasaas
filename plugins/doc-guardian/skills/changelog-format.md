---
name: changelog-format
description: Keep a Changelog format and Conventional Commits parsing
---

# Changelog Format

## Purpose

Defines Keep a Changelog format and how to parse Conventional Commits.

## When to Use

- **changelog-gen**: Generating changelog entries from commits
- **git-flow integration**: Validating commit message format

---

## Conventional Commits Pattern

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

---

## Type to Section Mapping

| Commit Type | Changelog Section |
|-------------|------------------|
| `feat` | Added |
| `fix` | Fixed |
| `docs` | Documentation |
| `perf` | Performance |
| `refactor` | Changed |
| `style` | Changed |
| `test` | Testing |
| `build` | Build |
| `ci` | CI/CD |
| `chore` | Maintenance |
| `BREAKING CHANGE` | Breaking Changes |

---

## Keep a Changelog Sections

Standard order (only include non-empty):
1. Breaking Changes
2. Added
3. Changed
4. Deprecated
5. Removed
6. Fixed
7. Security

---

## Breaking Changes Detection

Detected by:
- `!` suffix on type: `feat!: new auth system`
- `BREAKING CHANGE` in footer
- `BREAKING-CHANGE` in footer

---

## Entry Formatting

For each commit:
1. Extract scope (if present) as bold prefix: `**scope**: `
2. Use description as entry text
3. Link to commit hash if repository URL available
4. Include PR/issue references from footer

### Example Output

```markdown
## [Unreleased]

### Breaking Changes
- **auth**: Remove deprecated OAuth1 support

### Added
- **api**: New batch processing endpoint
- User preference saving feature

### Changed
- **core**: Improve error message clarity

### Fixed
- **api**: Handle null values in response
```

---

## Non-Conventional Handling

Commits not following format:
- List under "Other" section
- Flag for manual categorization
- Skip if `--strict` flag used

---

## Commit Range Detection

1. Default: commits since last tag
2. First release: all commits from initial
3. Explicit: `--from <tag> --to <ref>`

```bash
# Find last tag
git describe --tags --abbrev=0

# Commits since tag
git log v1.0.0..HEAD --oneline
```
