# PR Analysis Patterns

## Data Collection

### Step 1: Fetch PR Metadata

```
get_pull_request(pr_number) returns:
- title, description
- author, assignees
- base/head branches
- status (open, closed, merged)
- labels, milestone
- created_at, updated_at
```

### Step 2: Get Code Changes

```
get_pr_diff(pr_number) returns:
- Unified diff format
- File paths with +/- indicators
- Hunk headers with line numbers
```

### Step 3: Get Existing Feedback

```
get_pr_comments(pr_number) returns:
- Review comments with file/line
- General comments
- Author, timestamp
- Thread context (replies)
```

## Change Analysis

### Categorize Changes

| Pattern | Category |
|---------|----------|
| New files only | Feature addition |
| Modified test files | Test updates |
| Modified + deleted | Refactoring |
| Single file fix | Bug fix |
| Config/docs only | Infrastructure |

### Calculate Statistics

- Files changed count
- Lines added/removed
- Net change (+added - removed)
- New vs modified vs deleted files

### Identify Key Files

Priority order:
1. Security-sensitive (`auth`, `crypto`, `sql`)
2. API endpoints
3. Database migrations
4. Core business logic
5. Utilities and helpers
6. Tests
7. Documentation

## Risk Assessment

### Scope Assessment

| Files Changed | Lines Changed | Scope |
|---------------|---------------|-------|
| 1-3 | < 50 | Small |
| 4-10 | 50-200 | Medium |
| 10+ | 200+ | Large |

### Risk Indicators

| Indicator | Risk Level |
|-----------|------------|
| Security-sensitive files | High |
| Database migrations | High |
| API changes | Medium |
| New dependencies | Medium |
| Test-only changes | Low |
| Docs-only changes | Low |

## Summary Generation

### Quick Summary Template

```
This PR [adds|updates|fixes|removes] [feature/component]:

1. **[Category 1]**
   - Change description

2. **[Category 2]**
   - Change description

Key files:
- path/to/important/file.ts (+lines)
```

### Assessment Template

```
Scope: [Small|Medium|Large]
Risk: [Low|Medium|High]
Recommendation: [/pr review suggested | Looks good to merge]
```

## Annotated Diff Display

### Format

```
File: src/api/users.ts (+85 / -12)
----------------------------------------

@@ -42,6 +42,15 @@ function description
   42 |   existing line
   43 |
   44 |-  removed line
      |   [COMMENT by @user (time ago)]
      |   Comment text here
   45 |+  added line
   46 |+  another added line
```

### Comment Overlay

Position comments at their file/line locations:
- Show commenter username and time
- Include reply threads
- Mark resolved vs open
