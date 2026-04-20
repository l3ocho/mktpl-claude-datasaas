---
name: mcp-tools-reference
description: Complete reference of available Gitea MCP tools with usage patterns
---

# MCP Tools Reference

## Purpose

Provides the complete reference of available MCP tools for Gitea operations. This skill ensures consistent tool usage across all commands and agents.

## When to Use

- **All agents**: When performing any Gitea operation
- **All commands**: That interact with issues, labels, milestones, wiki, or dependencies

## Critical Rules

### NEVER Use CLI Tools

**FORBIDDEN - Do not use:**
```bash
tea issue list
tea issue create
tea pr create
gh issue list
gh pr create
curl -X POST "https://gitea.../api/..."
```

**If you find yourself about to run a bash command for Gitea, STOP and use the MCP tool instead.**

### Required Parameter Format

All tools require the `repo` parameter in `owner/repo` format:
```python
# CORRECT
get_labels(repo="org/repo")
list_issues(repo="org/repo", state="open")

# INCORRECT - Will fail!
get_labels()  # Missing repo parameter
```

---

## Issue Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_issues` | Fetch issues | `repo`, `state`, `labels`, `milestone` |
| `get_issue` | Get issue details | `repo`, `number` |
| `create_issue` | Create new issue | `repo`, `title`, `body`, `labels`, `assignee`, `milestone` |
| `update_issue` | Update issue | `repo`, `number`, `state`, `labels`, `body` |
| `add_comment` | Add comment to issue | `repo`, `number`, `body` |

## Label Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `get_labels` | Fetch all labels | `repo` |
| `suggest_labels` | Get intelligent suggestions | `repo`, `context` |
| `create_label` | Create repository label | `repo`, `name`, `color` |
| `create_label_smart` | Auto-detect org vs repo | `repo`, `name`, `color` |

## Milestone Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_milestones` | List all milestones | `repo`, `state` |
| `get_milestone` | Get milestone details | `repo`, `milestone_id` |
| `create_milestone` | Create new milestone | `repo`, `title`, `description`, `due_on` |
| `update_milestone` | Update milestone | `repo`, `milestone_id`, `state` |

## Dependency Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_issue_dependencies` | Get issue dependencies | `repo`, `issue_number` |
| `create_issue_dependency` | Create dependency | `repo`, `issue_number`, `depends_on` |
| `get_execution_order` | Get parallel batches | `repo`, `issue_numbers` |

## Wiki & Lessons Learned Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_wiki_pages` | List all wiki pages | `repo` |
| `get_wiki_page` | Fetch page content | `repo`, `page_name` |
| `create_wiki_page` | Create new page | `repo`, `title`, `content` |
| `update_wiki_page` | Update page content | `repo`, `page_name`, `content` |
| `search_lessons` | Search lessons learned | `repo`, `query`, `tags`, `limit` |
| `create_lesson` | Create lesson entry | `repo`, `title`, `content`, `tags`, `category` |

## Validation Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `validate_repo_org` | Check if repo is under org | `repo` |
| `get_branch_protection` | Check branch protection | `repo`, `branch` |

## Pull Request Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_pull_requests` | List PRs | `repo`, `state` |
| `get_pull_request` | Get PR details | `repo`, `number` |
| `create_pull_request` | Create PR | `repo`, `title`, `body`, `head`, `base` |
| `create_pr_review` | Create review | `repo`, `number`, `body`, `event` |

---

## Common Usage Examples

**Create sprint issue:**
```python
create_issue(
    repo="org/repo",
    title="[Sprint 17] feat: Implement JWT service",
    body="## Description\n...\n## Implementation\n**Wiki:** [link]",
    labels=["Type/Feature", "Priority/High"],
    milestone=17
)
```

**Get parallel execution batches:**
```python
get_execution_order(repo="org/repo", issue_numbers=[45, 46, 47, 48])
# Returns: {"batches": [[45, 48], [46], [47]]}
```

**Search lessons learned:**
```python
search_lessons(repo="org/repo", tags=["auth", "python"], limit=10)
```

**Create lesson:**
```python
create_lesson(
    repo="org/repo",
    title="Sprint 18 - JWT Token Edge Cases",
    content="# Sprint 18...\n## Context\n...",
    tags=["auth", "jwt", "python"],
    category="sprints"
)
```
