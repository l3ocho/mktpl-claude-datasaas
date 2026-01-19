---
description: Check current sprint progress and identify blockers
---

# Sprint Status Check

This command provides a quick overview of your current sprint progress, including open issues, completed work, dependency status, and potential blockers.

## What This Command Does

1. **Fetch Sprint Issues** - Lists all issues with current sprint labels/milestone
2. **Analyze Dependencies** - Shows dependency graph and blocked/unblocked tasks
3. **Categorize by Status** - Groups issues into: Open, In Progress, Blocked, Completed
4. **Identify Blockers** - Highlights issues with blocker comments or unmet dependencies
5. **Show Progress Summary** - Provides completion percentage and parallel execution status
6. **Highlight Priorities** - Shows critical and high-priority items needing attention

## Usage

Simply run `/sprint-status` to get a comprehensive sprint overview.

## MCP Tools Used

This command uses the following Gitea MCP tools:

**Issue Tools:**
- `list_issues(state="open")` - Fetch open issues
- `list_issues(state="closed")` - Fetch completed issues
- `get_issue(number)` - Get detailed issue information for blockers

**Dependency Tools:**
- `list_issue_dependencies(issue_number)` - Get dependencies for each issue
- `get_execution_order(issue_numbers)` - Get parallel execution batches

**Milestone Tools:**
- `get_milestone(milestone_id)` - Get milestone progress

## Expected Output

```
Sprint Status Report
====================

Sprint: Sprint 18 - Authentication System
Milestone: Due 2025-02-01 (5 days remaining)
Date: 2025-01-18

Progress Summary:
- Total Issues: 8
- Completed: 3 (37.5%)
- In Progress: 2 (25%)
- Ready: 2 (25%)
- Blocked: 1 (12.5%)

Dependency Graph:
#45 -> #46 -> #47
  |
  v
#49 -> #50

Parallel Execution Status:
+-----------------------------------------------+
| Batch 1 (COMPLETED):                           |
|   #45 - Implement JWT service                  |
|   #48 - Update API documentation               |
+-----------------------------------------------+
| Batch 2 (IN PROGRESS):                         |
|   #46 - Build login endpoint (75%)             |
|   #49 - Add auth tests (50%)                   |
+-----------------------------------------------+
| Batch 3 (BLOCKED):                             |
|   #47 - Create login form (waiting for #46)    |
+-----------------------------------------------+

Completed Issues (3):
  #45: [Sprint 18] feat: Implement JWT service [Type/Feature, Priority/High]
  #48: [Sprint 18] docs: Update API documentation [Type/Docs, Priority/Medium]
  #51: [Sprint 18] chore: Update dependencies [Type/Chore, Priority/Low]

In Progress (2):
  #46: [Sprint 18] feat: Build login endpoint [Type/Feature, Priority/High]
  #49: [Sprint 18] test: Add auth tests [Type/Test, Priority/Medium]

Ready to Start (2):
  #50: [Sprint 18] feat: Integrate OAuth providers [Type/Feature, Priority/Low]
  #52: [Sprint 18] feat: Add email verification [Type/Feature, Priority/Medium]

Blocked Issues (1):
  #47: [Sprint 18] feat: Create login form [Type/Feature, Priority/High]
     Blocked by: #46 (in progress)

Priority Alerts:
  1 high-priority item blocked: #47
  All critical items completed

Recommendations:
1. Focus on completing #46 (Login endpoint) - unblocks #47
2. Continue parallel work on #49 (Auth tests)
3. #50 and #52 are ready - can start in parallel
```

## Dependency Analysis

The status check analyzes dependencies to show:

**Blocked Issues:**
- Issues waiting for other issues to complete
- Shows which issue is blocking and its current status

**Unblocked Issues:**
- Issues with no pending dependencies
- Ready to be picked up immediately

**Parallel Opportunities:**
- Multiple unblocked issues that can run simultaneously
- Maximizes sprint velocity

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
list_issues(milestone="Sprint 18")
```

**By Component:**
```
Show only backend issues:
list_issues(labels=["Component/Backend"])
```

## Blocker Detection

The command identifies blocked issues by:
1. **Dependency Analysis** - Uses `list_issue_dependencies` to find unmet dependencies
2. **Comment Keywords** - Checks for "blocked", "blocker", "waiting for"
3. **Stale Issues** - Issues with no recent activity (>7 days)

## When to Use

Run `/sprint-status` when you want to:
- Start your day and see what needs attention
- Prepare for standup meetings
- Check if the sprint is on track
- Identify bottlenecks or blockers
- Decide what to work on next
- See which tasks can run in parallel

## Integration with Other Commands

- Use `/sprint-start` to begin working on identified tasks
- Use `/sprint-close` when all issues are completed
- Use `/sprint-plan` to adjust scope if blocked items can't be unblocked

## Example Usage

```
User: /sprint-status

Sprint Status Report
====================

Sprint: Sprint 18 - Authentication System
Progress: 3/8 (37.5%)

Next Actions:
1. Complete #46 - it's blocking #47
2. Start #50 or #52 - both are unblocked

Would you like me to generate execution prompts for the unblocked tasks?
```
