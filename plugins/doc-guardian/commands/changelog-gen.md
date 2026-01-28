---
description: Generate changelog from conventional commits in Keep-a-Changelog format
---

# Changelog Generation

Generate a changelog entry from conventional commits.

## Process

1. **Identify Commit Range**
   - Default: commits since last tag
   - Optional: specify range (e.g., `v1.0.0..HEAD`)
   - Detect if this is first release (no previous tags)

2. **Parse Conventional Commits**
   Extract from commit messages following the pattern:
   ```
   <type>(<scope>): <description>

   [optional body]

   [optional footer(s)]
   ```

   **Recognized Types:**
   | Type | Changelog Section |
   |------|------------------|
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

3. **Group by Type**
   Organize commits into Keep-a-Changelog sections:
   - Breaking Changes (if any `!` suffix or `BREAKING CHANGE` footer)
   - Added (feat)
   - Changed (refactor, style, perf)
   - Deprecated
   - Removed
   - Fixed (fix)
   - Security

4. **Format Entries**
   For each commit:
   - Extract scope (if present) as prefix
   - Use description as entry text
   - Link to commit hash if repository URL available
   - Include PR/issue references from footer

5. **Output Format**
```markdown
## [Unreleased]

### Breaking Changes
- **scope**: Description of breaking change

### Added
- **scope**: New feature description
- Another feature without scope

### Changed
- **scope**: Refactoring description

### Fixed
- **scope**: Bug fix description

### Documentation
- Updated README with new examples
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--from <tag>` | Start from specific tag | Latest tag |
| `--to <ref>` | End at specific ref | HEAD |
| `--version <ver>` | Set version header | [Unreleased] |
| `--include-merge` | Include merge commits | false |
| `--group-by-scope` | Group by scope within sections | false |

## Integration

The generated output is designed to be copied directly into CHANGELOG.md:
- Follows [Keep a Changelog](https://keepachangelog.com) format
- Compatible with semantic versioning
- Excludes non-user-facing commits (chore, ci, test by default)

## Example Usage

```
/changelog-gen
/changelog-gen --from v1.0.0 --version 1.1.0
/changelog-gen --include-merge --group-by-scope
```

## Non-Conventional Commits

Commits not following conventional format are:
- Listed under "Other" section
- Flagged for manual categorization
- Skipped if `--strict` flag is used
