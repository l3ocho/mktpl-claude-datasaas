---
name: sprint-status
description: Check current sprint progress and identify blockers
---

# Sprint Status Check

This command provides a quick overview of your current sprint progress, including open issues, completed work, and potential blockers.

## What This Command Does

1. **Fetch Sprint Issues** - Lists all issues with current sprint labels/milestone
2. **Categorize by Status** - Groups issues into: Open, In Progress, Blocked, Completed
3. **Identify Blockers** - Highlights issues with blocker comments or dependencies
4. **Show Progress Summary** - Provides completion percentage and velocity insights
5. **Highlight Priorities** - Shows critical and high-priority items needing attention

## Usage

Simply run `/sprint-status` to get a comprehensive sprint overview.

## MCP Tools Used

This command uses the following Gitea MCP tools:

- `list_issues(state="open")` - Fetch open issues
- `list_issues(state="closed")` - Fetch completed issues
- `get_issue(number)` - Get detailed issue information for blockers

## Expected Output

```
Sprint Status Report
====================

Sprint: Sprint 16 - Authentication System
Date: 2025-01-18

Progress Summary:
- Total Issues: 8
- Completed: 3 (37.5%)
- In Progress: 2 (25%)
- Open: 2 (25%)
- Blocked: 1 (12.5%)

Completed Issues (3):
✅ #45: Implement JWT token generation [Type/Feature, Priority/High]
✅ #46: Build user login endpoint [Type/Feature, Priority/High]
✅ #48: Write authentication tests [Type/Test, Priority/Medium]

In Progress (2):
🔄 #47: Create user registration form [Type/Feature, Priority/Medium]
🔄 #49: Add password reset flow [Type/Feature, Priority/Low]

Open Issues (2):
📋 #50: Integrate OAuth providers [Type/Feature, Priority/Low]
📋 #51: Add email verification [Type/Feature, Priority/Medium]

Blocked Issues (1):
🚫 #52: Deploy auth service [Type/Deploy, Priority/High]
   Blocker: Waiting for database migration approval

Priority Alerts:
⚠️  1 high-priority item blocked: #52
✅ All critical items completed

Recommendations:
1. Focus on unblocking #52 (Deploy auth service)
2. Continue work on #47 (User registration form)
3. Consider starting #51 (Email verification) next
```

## Filtering Options

You can optionally filter the status check:

**By Label:**
```
Show only high-priority issues:
list_issues(labels=["Priority/High"])
```

**By Milestone:**
```
Show issues for specific sprint:
list_issues(milestone="Sprint 16")
```

**By Component:**
```
Show only backend issues:
list_issues(labels=["Component/Backend"])
```

## Blocker Detection

The command identifies blocked issues by:
1. Checking issue comments for keywords: "blocked", "blocker", "waiting for", "dependency"
2. Looking for issues with no recent activity (>7 days)
3. Identifying issues with unresolved dependencies

## When to Use

Run `/sprint-status` when you want to:
- Start your day and see what needs attention
- Prepare for standup meetings
- Check if the sprint is on track
- Identify bottlenecks or blockers
- Decide what to work on next

## Integration with Other Commands

- Use `/sprint-start` to begin working on identified tasks
- Use `/sprint-close` when all issues are completed
- Use `/sprint-plan` to adjust scope if blocked items can't be unblocked

## Example Usage

```
User: /sprint-status