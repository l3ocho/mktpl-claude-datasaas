# MCP Tools Reference - Gitea PR Operations

## Available Tools

Use `ToolSearch` to load these tools before use.

### Pull Request Tools

| Tool | Purpose |
|------|---------|
| `mcp__gitea__list_pull_requests` | List PRs (open, closed, all) |
| `mcp__gitea__get_pull_request` | Get PR metadata, status, labels |
| `mcp__gitea__get_pr_diff` | Get unified diff of changes |
| `mcp__gitea__get_pr_comments` | Get review comments and discussions |
| `mcp__gitea__create_pr_review` | Submit review (approve, comment, request changes) |
| `mcp__gitea__add_pr_comment` | Add single comment to PR |
| `mcp__gitea__create_pull_request` | Create new PR |

### Supporting Tools

| Tool | Purpose |
|------|---------|
| `mcp__gitea__get_issue` | Get linked issue details |
| `mcp__gitea__get_labels` | Get available labels |
| `mcp__gitea__validate_repo_org` | Validate repository exists |

## Loading Tools

Before using MCP tools, load them:

```
Use ToolSearch with query: "+gitea pull_request"
```

## Common Operations

### Fetch PR for Review

```
1. get_pull_request(pr_number) -> metadata
2. get_pr_diff(pr_number) -> code changes
3. get_pr_comments(pr_number) -> existing feedback
```

### Submit Review

```
create_pr_review:
  pr_number: number
  body: string (review summary)
  event: "APPROVE" | "COMMENT" | "REQUEST_CHANGES"
  comments: [{path, line, body}] (optional inline comments)
```

### Add Comment

```
add_pr_comment:
  pr_number: number
  body: string
```

## Environment Variables

Required in `.env`:
- `GITEA_ORG` - Organization/owner name
- `GITEA_REPO` - Repository name

Required in `~/.config/claude/gitea.env`:
- `GITEA_API_URL` - Gitea server URL
- `GITEA_API_TOKEN` - API token with repo permissions

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Tool not found | MCP not loaded | Run ToolSearch first |
| 401 Unauthorized | Invalid/expired token | Regenerate token |
| 404 Not Found | Wrong org/repo or PR doesn't exist | Check .env settings |
| 403 Forbidden | Insufficient permissions | Check token scopes |
