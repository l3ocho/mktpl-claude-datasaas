---
name: doc changelog-gen
description: Generate changelog from conventional commits in Keep-a-Changelog format
---

# /doc changelog-gen

Generate a changelog entry from conventional commits.

## Skills to Load

- skills/changelog-format.md

## Visual Output

```
+------------------------------------------------------------------+
|  DOC-GUARDIAN - Changelog Generation                             |
+------------------------------------------------------------------+
```

## Process

1. **Identify Commit Range**
   Execute `skills/changelog-format.md` - detect range from tags

2. **Parse Conventional Commits**
   Use pattern from skill: `<type>(<scope>): <description>`

3. **Group by Type**
   Map to Keep-a-Changelog sections per skill

4. **Format Entries**
   - Extract scope as bold prefix
   - Use description as entry text
   - Link commit hashes if repo URL available

5. **Output**
   Use format from `skills/changelog-format.md`

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--from <tag>` | Start from tag | Latest tag |
| `--to <ref>` | End at ref | HEAD |
| `--version <ver>` | Version header | [Unreleased] |
| `--include-merge` | Include merges | false |
| `--group-by-scope` | Group by scope | false |

## Integration

Output designed for direct copy to CHANGELOG.md:
- Follows [Keep a Changelog](https://keepachangelog.com) format
- Compatible with semantic versioning
