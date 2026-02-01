---
name: input-detection
description: Detect planning input source (RFC, file, wiki, or conversation)
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
| 0 | Approved RFC | RFC-Index has entries in "Approved" section | Offer RFC selection or new work |
| 1 | Local file | `docs/changes/*.md` exists | Parse frontmatter, migrate to wiki, delete local |
| 2 | Existing wiki | `Change VXX.X.X: Proposal` exists | Use as-is, create implementation page |
| 3 | Conversation | Neither exists | Create wiki from discussion context |

---

## RFC Detection (Priority 0)

Before checking for local files or wiki proposals, check for approved RFCs.

### Detection Steps

1. **Fetch RFC-Index:**
   ```python
   get_wiki_page(page_name="RFC-Index", repo="org/repo")
   ```

2. **Parse Approved Section:**
   - Find "## Approved" section
   - Extract RFC entries from table

3. **If Approved RFCs Exist:**
   ```
   Approved RFCs available for implementation:

   | RFC | Title | Champion |
   |-----|-------|----------|
   | RFC-0003 | Feature X | @user |
   | RFC-0007 | Enhancement Y | @user |

   Options:
   [1] Implement RFC-0003: Feature X
   [2] Implement RFC-0007: Enhancement Y
   [3] Describe new work (skip RFCs)

   Select an option:
   ```

4. **If RFC Selected:**
   - Use RFC content as planning input
   - Status will transition to Implementing after planning approval
   - Skip local file and wiki proposal detection

5. **If "New Work" Selected:**
   - Continue with normal Priority 1-3 detection
   - Optionally offer: "Would you like to create an RFC first? (y/n)"

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
