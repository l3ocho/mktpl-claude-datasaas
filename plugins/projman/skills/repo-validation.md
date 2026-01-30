---
name: repo-validation
description: Repository organization check and label taxonomy validation
---

# Repository Validation

## Purpose

Validates that the repository belongs to an organization and has the required label taxonomy.

## When to Use

- **Planner agent**: At start of sprint planning
- **Commands**: `/sprint-plan`, `/labels-sync`, `/project-init`

---

## Step 1: Detect Repository from Git Remote

```bash
git remote get-url origin
```

Parse output to extract `owner/repo`:
- SSH: `git@host:owner/repo.git` → `owner/repo`
- SSH with port: `ssh://git@host:port/owner/repo.git` → `owner/repo`
- HTTPS: `https://host/owner/repo.git` → `owner/repo`

---

## Step 2: Validate Organization Ownership

```python
validate_repo_org(repo="owner/repo")
```

**If NOT an organization repository:**
```
REPOSITORY VALIDATION FAILED

This plugin requires the repository to belong to an organization, not a user.
Current repository appears to be a personal repository.

Please:
1. Create an organization in Gitea
2. Transfer or create the repository under that organization
3. Update your configuration
```

---

## Step 3: Validate Label Taxonomy

```python
get_labels(repo="owner/repo")
```

**Required label categories:**

| Category | Required Labels |
|----------|-----------------|
| Type/* | Bug, Feature, Refactor, Documentation, Test, Chore |
| Priority/* | Low, Medium, High, Critical |
| Complexity/* | Simple, Medium, Complex |
| Efforts/* | XS, S, M, L, XL |

**If labels are missing:**
- Use `create_label_smart()` to create them (auto-detects org vs repo level)
- Report which labels were created

---

## Validation Report Format

```
Repository Validation
=====================

Git Remote: git@gitea.example.com:org/repo.git
Detected: org/repo

Organization Check:
  ✓ Repository belongs to organization "org"

Label Taxonomy:
  ✓ Type/* labels: 6/6 present
  ✓ Priority/* labels: 4/4 present
  ✓ Complexity/* labels: 3/3 present
  ✓ Efforts/* labels: 5/5 present

All validations passed. Ready for planning.
```

---

## Error Handling

### Repository Not Found (404)
```
Repository validation failed: Not found

The repository "owner/repo" does not exist or you don't have access.
Please verify:
1. Repository name is correct
2. Your token has repository access
3. Organization/owner name is correct
```

### Authentication Error (401/403)
```
Repository validation failed: Authentication error

Your Gitea token may be invalid or lack permissions.
Please verify:
1. Token is valid and not expired
2. Token has 'repo' scope
3. You have access to this repository
```
