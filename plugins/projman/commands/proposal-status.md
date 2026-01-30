---
description: View proposal and implementation hierarchy with status tracking
---

# Proposal Status

## Skills Required

- skills/mcp-tools-reference.md
- skills/wiki-conventions.md

## Purpose

View status of all change proposals and their implementations in Gitea Wiki.

## Invocation

```
/proposal-status
/proposal-status --version V04.1.0
/proposal-status --status "In Progress"
```

## Workflow

1. **Fetch Wiki Pages** - Use `list_wiki_pages()` to get all pages
2. **Filter Proposals** - Match `Change V*: Proposal*` pattern
3. **Parse Structure** - Group implementations under parent proposals
4. **Extract Status** - Read page metadata (In Progress, Implemented, Abandoned)
5. **Fetch Linked Artifacts** - Find issues and lessons referencing each implementation
6. **Display Tree View** - Show hierarchy with status and links

## Status Definitions

| Status | Meaning |
|--------|---------|
| Pending | Proposal created, no implementation started |
| In Progress | At least one implementation is active |
| Implemented | All planned implementations complete |
| Abandoned | Proposal cancelled or superseded |

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  Proposal Status                                                 ║
╚══════════════════════════════════════════════════════════════════╝
```
