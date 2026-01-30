---
name: input-detection
description: Detect planning input source (file, wiki, or conversation)
---

# Input Source Detection

## Purpose

Defines how to detect where planning input is coming from and how to handle each source.

## When to Use

- **Planner agent**: At start of sprint planning
- **Commands**: `/sprint-plan`

---

## Detection Priority

| Priority | Source | Detection | Action |
|----------|--------|-----------|--------|
| 1 | Local file | `docs/changes/*.md` exists | Parse frontmatter, migrate to wiki, delete local |
| 2 | Existing wiki | `Change VXX.X.X: Proposal` exists | Use as-is, create implementation page |
| 3 | Conversation | Neither exists | Create wiki from discussion context |

---

## Local File Format

```yaml
---
version: "4.1.0"        # or "sprint-17" for internal work
title: "Feature Name"
plugin: plugin-name     # optional
type: feature           # feature | bugfix | refactor | infra
---

# Feature Description
[Free-form content...]
```

---

## Detection Steps

1. **Check for local files:**
   ```bash
   ls docs/changes/*.md
   ```

2. **Check for existing wiki proposal:**
   ```python
   list_wiki_pages(repo="org/repo")
   # Filter for "Change V" prefix matching version
   ```

3. **If neither found:** Use conversation context

4. **If multiple sources found:** Ask user which to use

---

## Report to User

```
Input source detected:
✓ Found: docs/changes/v4.1.0-wiki-planning.md
  - Version: 4.1.0
  - Title: Wiki-Based Planning Workflow
  - Type: feature

I'll use this as the planning input. Proceed? (y/n)
```

---

## Migration Flow (Local File → Wiki)

When using local file as input:

1. **Parse frontmatter** to extract metadata
2. **Create wiki proposal page:** `Change V4.1.0: Proposal`
3. **Create implementation page:** `Change V4.1.0: Proposal (Implementation 1)`
4. **Delete local file** - wiki is now source of truth

```
Migration complete:
✓ Created: "Change V4.1.0: Proposal" (wiki)
✓ Created: "Change V4.1.0: Proposal (Implementation 1)" (wiki)
✓ Deleted: docs/changes/v4.1.0-wiki-planning.md (migrated)
```

---

## Ambiguous Input Handling

If multiple valid sources found:

```
Multiple input sources detected:

1. Local file: docs/changes/v4.1.0-feature.md
   - Version: 4.1.0
   - Title: New Feature

2. Wiki proposal: Change V4.1.0: Proposal
   - Status: In Progress
   - Date: 2026-01-20

Which should I use for planning?
  [1] Local file (will migrate to wiki)
  [2] Existing wiki proposal
  [3] Start fresh from conversation
```
