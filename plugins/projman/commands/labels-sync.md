---
description: Fetch and validate label taxonomy from Gitea, create missing required labels
---

# Sync Label Taxonomy from Gitea

This command fetches the current label taxonomy from Gitea (organization + repository labels), validates that required labels exist, and creates any missing ones.

## CRITICAL: Execution Steps

You MUST follow these steps in order. Do NOT skip any step.

### Step 1: Detect Repository from Git Remote

Run this Bash command to get the git remote URL:

```bash
git remote get-url origin
```

Parse the output to extract `owner/repo`:
- SSH format `ssh://git@host:port/owner/repo.git` → extract `owner/repo`
- SSH short `git@host:owner/repo.git` → extract `owner/repo`
- HTTPS `https://host/owner/repo.git` → extract `owner/repo`

Store this as `REPO_NAME` for all subsequent MCP calls.

### Step 2: Validate Repository Organization

Call MCP tool with the detected repo:

```
mcp__plugin_projman_gitea__validate_repo_org(repo=REPO_NAME)
```

This determines if the owner is an organization or user account.

### Step 3: Fetch Labels from Gitea

Call MCP tool with the detected repo:

```
mcp__plugin_projman_gitea__get_labels(repo=REPO_NAME)
```

This returns both organization labels (if org-owned) and repository labels.

### Step 4: Display Current Taxonomy

Show the user:
- Total organization labels count
- Total repository labels count
- Labels grouped by category (Type/*, Priority/*, etc.)

### Step 5: Check Required Labels

Verify these required label categories exist:
- **Type/***: Bug, Feature, Refactor, Documentation, Test, Chore
- **Priority/***: Low, Medium, High, Critical
- **Complexity/***: Simple, Medium, Complex
- **Effort/***: XS, S, M, L, XL (note: may be "Effort" or "Efforts")

### Step 6: Create Missing Labels (if any)

Use `create_label_smart` which automatically creates labels at the correct level:
- **Organization level**: Type/*, Priority/*, Complexity/*, Effort/*, Risk/*, Source/*, Agent/*
- **Repository level**: Component/*, Tech/*

```
mcp__plugin_projman_gitea__create_label_smart(repo=REPO_NAME, name="Type/Bug", color="d73a4a")
```

This automatically detects whether to create at org or repo level based on the category.

**Alternative (explicit control):**
- Org labels: `create_org_label(org="org-name", name="Type/Bug", color="d73a4a")`
- Repo labels: `create_label(repo=REPO_NAME, name="Component/Backend", color="5319e7")`

Use the label format that matches existing labels in the repo (slash `/` or colon-space `: `).

### Step 7: Report Results

Summarize what was found and created.

## DO NOT

- **DO NOT** call MCP tools without the `repo` parameter - they will fail
- **DO NOT** create any local files - this command only interacts with Gitea
- **DO NOT** ask the user questions - execute autonomously
- **DO NOT** create a "labels reference file" - labels are fetched dynamically from Gitea

## MCP Tools Used

All tools require the `repo` parameter in `owner/repo` format:

| Tool | Purpose |
|------|---------|
| `validate_repo_org(repo=...)` | Check if owner is organization or user |
| `get_labels(repo=...)` | Fetch all labels (org + repo) |
| `create_label(repo=..., name=..., color=...)` | Create missing labels |

## Expected Output

```
Label Taxonomy Sync
===================

Detecting repository from git remote...
Repository: personal-projects/your-repo-name
Owner type: Organization

Fetching labels from Gitea...

Current Label Taxonomy:
- Organization Labels: 27
- Repository Labels: 16
- Total: 43 labels

Organization Labels by Category:
  Type/*: 6 labels
  Priority/*: 4 labels
  Complexity/*: 3 labels
  Effort/*: 5 labels
  ...

Repository Labels by Category:
  Component/*: 9 labels
  Tech/*: 7 labels

Required Labels Check:
  Type/*: 6/6 present ✓
  Priority/*: 4/4 present ✓
  Complexity/*: 3/3 present ✓
  Effort/*: 5/5 present ✓

All required labels present. Label taxonomy is ready for use.
```

## Label Format Detection

Labels may use different naming conventions:
- Slash format: `Type/Bug`, `Priority/High`
- Colon-space format: `Type: Bug`, `Priority: High`

When creating missing labels, match the format used by existing labels in the repository.

## Troubleshooting

**Error: Use 'owner/repo' format**
- You forgot to pass the `repo` parameter to the MCP tool
- Go back to Step 1 and detect the repo from git remote

**Empty organization labels**
- If owner is a user account (not org), organization labels will be empty
- This is expected - user accounts only have repository-level labels

**Git remote not found**
- Ensure you're running in a directory with a git repository
- Check that the `origin` remote is configured

## When to Run

Run `/labels-sync` when:
- Setting up the plugin for the first time
- You notice missing labels in suggestions
- New labels are added to Gitea
- After major taxonomy updates
