---
description: View proposal and implementation hierarchy with status tracking
---

# Proposal Status

View the status of all change proposals and their implementations in the Gitea Wiki.

## Overview

This command provides a tree view of:
- All change proposals (`Change VXX.X.X: Proposal`)
- Their implementations (`Change VXX.X.X: Proposal (Implementation N)`)
- Linked issues and lessons learned

## Workflow

1. **Fetch All Wiki Pages**
   - Use `list_wiki_pages()` to get all wiki pages
   - Filter for pages matching `Change V*: Proposal*` pattern

2. **Parse Proposal Structure**
   - Group implementations under their parent proposals
   - Extract status from page metadata (In Progress, Implemented, Abandoned)

3. **Fetch Linked Artifacts**
   - For each implementation, search for issues referencing it
   - Search lessons learned that link to the implementation

4. **Display Tree View**
   ```
   Change V04.1.0: Proposal [In Progress]
   ├── Implementation 1 [In Progress] - 2026-01-26
   │   ├── Issues: #161, #162, #163, #164
   │   └── Lessons: (pending)
   └── Implementation 2 [Not Started]

   Change V04.0.0: Proposal [Implemented]
   └── Implementation 1 [Implemented] - 2026-01-20
       ├── Issues: #150, #151
       └── Lessons: v4.0.0-impl-1-lessons
   ```

## MCP Tools Used

- `list_wiki_pages()` - List all wiki pages
- `get_wiki_page(page_name)` - Get page content for status extraction
- `list_issues(state, labels)` - Find linked issues
- `search_lessons(query, tags)` - Find linked lessons

## Status Definitions

| Status | Meaning |
|--------|---------|
| **Pending** | Proposal created but no implementation started |
| **In Progress** | At least one implementation is active |
| **Implemented** | All planned implementations complete |
| **Abandoned** | Proposal was cancelled or superseded |

## Filtering Options

The command accepts optional filters:

```
/proposal-status                    # Show all proposals
/proposal-status --version V04.1.0  # Show specific version
/proposal-status --status "In Progress"  # Filter by status
```

## Example Output

```
Proposal Status Report
======================

Change V04.1.0: Wiki-Based Planning Workflow [In Progress]
├── Implementation 1 [In Progress] - Started: 2026-01-26
│   ├── Issues: #161 (closed), #162 (closed), #163 (closed), #164 (open)
│   └── Lessons: (pending - sprint not closed)
│
└── (No additional implementations planned)

Change V04.0.0: MCP Server Consolidation [Implemented]
├── Implementation 1 [Implemented] - 2026-01-15 to 2026-01-20
│   ├── Issues: #150 (closed), #151 (closed), #152 (closed)
│   └── Lessons:
│       • Sprint 15 - MCP Server Symlink Best Practices
│       • Sprint 15 - Venv Path Resolution in Plugins
│
└── (Complete)

Change V03.2.0: Label Taxonomy Sync [Implemented]
└── Implementation 1 [Implemented] - 2026-01-10 to 2026-01-12
    ├── Issues: #140 (closed), #141 (closed)
    └── Lessons:
        • Sprint 14 - Organization vs Repository Labels

Summary:
- Total Proposals: 3
- In Progress: 1
- Implemented: 2
- Pending: 0
```

## Implementation Notes

**Page Name Parsing:**
- Proposals: `Change VXX.X.X: Proposal` or `Change Sprint-NN: Proposal`
- Implementations: `Change VXX.X.X: Proposal (Implementation N)`

**Status Extraction:**
- Parse the `> **Status:**` line from page metadata
- Default to "Unknown" if not found

**Issue Linking:**
- Search for issues containing wiki link in body
- Or search for issues with `[Sprint XX]` prefix matching implementation

**Lesson Linking:**
- Search lessons with implementation link in metadata
- Or search by version/sprint tags

## Visual Output

When executing this command, display the plugin header:

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  Proposal Status                                                 ║
╚══════════════════════════════════════════════════════════════════╝
```

Then proceed with the status report.
