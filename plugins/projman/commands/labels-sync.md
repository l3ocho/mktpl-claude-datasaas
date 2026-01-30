---
description: Fetch and validate label taxonomy from Gitea, create missing required labels
---

# Sync Label Taxonomy

## Skills Required

- skills/mcp-tools-reference.md
- skills/repo-validation.md
- skills/label-taxonomy/labels-reference.md

## Purpose

Fetch current label taxonomy from Gitea, validate required labels exist, and create any missing ones.

## Invocation

Run `/labels-sync` when setting up the plugin or after taxonomy updates.

## Workflow

1. **Detect Repository** - Parse `git remote get-url origin` to get `owner/repo`
2. **Validate Repository** - Use `validate_repo_org` to check if org-owned
3. **Fetch Labels** - Use `get_labels(repo=...)` to get org + repo labels
4. **Display Taxonomy** - Show labels grouped by category
5. **Check Required Labels** - Verify Type/*, Priority/*, Complexity/*, Effort/* exist
6. **Create Missing** - Use `create_label_smart` which auto-detects org vs repo level
7. **Report Results** - Summarize what was found and created

## Required Label Categories

| Category | Required Labels |
|----------|-----------------|
| Type/* | Bug, Feature, Refactor, Documentation, Test, Chore |
| Priority/* | Low, Medium, High, Critical |
| Complexity/* | Simple, Medium, Complex |
| Efforts/* | XS, S, M, L, XL |

## DO NOT

- Call MCP tools without the `repo` parameter
- Create local files - this command only interacts with Gitea
- Ask user questions - execute autonomously

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  Labels Sync                                                     ║
╚══════════════════════════════════════════════════════════════════╝
```
