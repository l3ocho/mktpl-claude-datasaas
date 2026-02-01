## Sprint Management (projman)

This project uses the **projman** plugin for sprint planning and project management with Gitea integration.

### Available Commands

| Command | Description |
|---------|-------------|
| `/sprint-plan` | Start sprint planning with AI-guided architecture analysis |
| `/sprint-start` | Begin sprint execution with relevant lessons learned |
| `/sprint-status` | Check current sprint progress and identify blockers |
| `/sprint-close` | Complete sprint and capture lessons learned to Gitea Wiki |
| `/labels-sync` | Synchronize label taxonomy from Gitea |
| `/initial-setup` | Run initial setup for projman plugin |
| `/rfc-create` | Create new RFC from conversation or clarified spec |
| `/rfc-list` | List all RFCs grouped by status |
| `/rfc-review` | Submit Draft RFC for review |
| `/rfc-approve` | Approve RFC for sprint planning |
| `/rfc-reject` | Reject RFC with documented reason |

### MCP Tools Available

The following Gitea MCP tools are available for issue and project management:

**Issue Management:**
- `list_issues` - Query issues with filters (state, labels)
- `get_issue` - Fetch single issue details
- `create_issue` - Create new issue with labels
- `update_issue` - Modify existing issue
- `add_comment` - Add comments to issues

**Labels:**
- `get_labels` - Fetch org + repo label taxonomy
- `suggest_labels` - Analyze context and suggest appropriate labels
- `create_label` - Create missing required labels

**Milestones:**
- `list_milestones` - List sprint milestones
- `get_milestone` - Get milestone details
- `create_milestone` - Create sprint milestone
- `update_milestone` - Update/close milestone

**Dependencies:**
- `list_issue_dependencies` - Get issue dependencies
- `create_issue_dependency` - Create dependency between issues
- `get_execution_order` - Get parallel execution batches

**Wiki (Lessons Learned & RFCs):**
- `list_wiki_pages` - List wiki pages
- `get_wiki_page` - Fetch specific page content
- `create_wiki_page` - Create new wiki page
- `update_wiki_page` - Update existing wiki page
- `create_lesson` - Create lessons learned document
- `search_lessons` - Search past lessons by tags
- `allocate_rfc_number` - Get next available RFC number

### Usage Guidelines

- **Always use `/sprint-plan`** when starting new development work
- **Check `/sprint-status`** regularly during active sprints
- **Run `/sprint-close`** at the end of each sprint to capture lessons learned
- Use `suggest_labels` when creating issues to ensure proper categorization
- Search lessons learned with `search_lessons` before implementing features to avoid repeated mistakes
