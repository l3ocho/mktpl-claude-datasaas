---
description: Complete sprint and capture lessons learned to Wiki.js
---

# Close Sprint and Capture Lessons Learned

This command completes the sprint and captures lessons learned to Wiki.js. **This is critical** - after 15 sprints without lesson capture, repeated mistakes occurred (e.g., Claude Code infinite loops 2-3 times on similar issues).

## Why Lessons Learned Matter

**Problem:** Without systematic lesson capture, teams repeat the same mistakes:
- Claude Code infinite loops on similar issues (happened 2-3 times)
- Same architectural mistakes (multiple occurrences)
- Forgotten optimizations (re-discovered each time)

**Solution:** Mandatory lessons learned capture at sprint close, searchable at sprint start.

## Sprint Close Workflow

The orchestrator agent will guide you through:

1. **Review Sprint Completion**
   - Verify all issues are closed or moved to backlog
   - Check for incomplete work needing carryover
   - Review overall sprint goals vs. actual completion

2. **Capture Lessons Learned**
   - What went wrong and why
   - What went right and should be repeated
   - Preventable repetitions to avoid in future sprints
   - Technical insights and gotchas discovered

3. **Tag for Discoverability**
   - Apply relevant tags: technology, component, type of lesson
   - Ensure future sprints can find these lessons via search
   - Use consistent tagging for patterns

4. **Update Wiki.js**
   - Use `create_lesson` to save lessons to Wiki.js
   - Create lessons in `/projects/{project}/lessons-learned/sprints/`
   - Update INDEX.md automatically
   - Make lessons searchable for future sprints

5. **Git Operations**
   - Commit any remaining work
   - Merge feature branches if needed
   - Clean up merged branches
   - Tag sprint completion

## MCP Tools Available

**Gitea Tools:**
- `list_issues` - Review sprint issues (completed and incomplete)
- `get_issue` - Get detailed issue information for retrospective
- `update_issue` - Move incomplete issues to next sprint

**Wiki.js Tools:**
- `create_lesson` - Create lessons learned entry
- `tag_lesson` - Add/update tags on lessons
- `list_pages` - Check existing lessons learned
- `update_page` - Update INDEX.md if needed

## Lesson Structure

Lessons should follow this structure:

```markdown
# Sprint X - [Lesson Title]

## Context
[What were you trying to do? What was the sprint goal?]

## Problem
[What went wrong? What insight emerged? What challenge did you face?]

## Solution
[How did you solve it? What approach worked?]

## Prevention
[How can this be avoided or optimized in the future? What should future sprints know?]

## Tags
[Comma-separated tags for search: technology, component, type]
```

## Example Lessons Learned

**Example 1: Technical Gotcha**
```markdown
# Sprint 16 - Claude Code Infinite Loop on Validation Errors

## Context
Implementing input validation for authentication API endpoints.

## Problem
Claude Code entered an infinite loop when pytest validation tests failed.
The loop occurred because the error message didn't change between attempts,
causing Claude to retry the same fix repeatedly.

## Solution
Added more descriptive error messages to validation tests that specify
exactly what value failed and why. This gave Claude clear feedback
to adjust the approach rather than retrying the same fix.

## Prevention
- Always write validation test errors with specific values and expectations
- If Claude loops, check if error messages provide unique information per failure
- Add a "loop detection" check in test output (fail after 3 identical errors)

## Tags
testing, claude-code, validation, python, pytest, debugging
```

**Example 2: Architectural Decision**
```markdown
# Sprint 14 - Extracting Services Too Early

## Context
Planning to extract Intuit Engine service from monolith.

## Problem
Initial plan was to extract immediately without testing the API boundaries
first. This would have caused integration issues discovered late.

## Solution
Added a sprint phase to:
1. Define clear API contracts first
2. Add integration tests for the boundaries
3. THEN extract the service

Delayed extraction by one sprint but avoided major rework.

## Prevention
- Always define API contracts before service extraction
- Write integration tests FIRST, extraction SECOND
- Don't rush architectural changes - test boundaries first

## Tags
architecture, service-extraction, refactoring, api-design, planning
```

## Tagging Strategy

Use consistent tags for discoverability:

**By Technology:**
- `python`, `javascript`, `docker`, `postgresql`, `redis`, `vue`, `fastapi`

**By Component:**
- `backend`, `frontend`, `api`, `database`, `auth`, `deploy`, `testing`, `docs`

**By Type:**
- `bug`, `feature`, `refactor`, `architecture`, `performance`, `security`

**By Issue:**
- `claude-code`, `validation`, `testing`, `debugging`, `deployment`, `configuration`

**By Pattern:**
- `infinite-loop`, `edge-case`, `integration`, `boundaries`, `dependencies`

## Orchestrator's Role

The orchestrator agent will:
1. Ask probing questions about the sprint
2. Identify preventable mistakes vs. expected challenges
3. Structure lessons in the proper format
4. Suggest appropriate tags
5. Create lessons in Wiki.js using `create_lesson`
6. Ensure lessons are discoverable for future sprints

## Example Sprint Close Session

```
User: /sprint-close
Orchestrator: Let's close the sprint and capture lessons learned.

First, let me review the sprint completion...

[Uses list_issues to check sprint status]

Sprint 16 Summary:
- 8 issues planned
- 7 completed (87.5%)
- 1 moved to backlog (#52: Deploy auth service - blocked by infra)

Great progress! Now, let's capture lessons learned.

What went wrong or what challenges did you face this sprint?

User: Claude Code got stuck in a loop when pytest validation tests failed

Orchestrator: That's a valuable lesson - this prevents future frustration.

Let me ask some clarifying questions:
1. What caused the loop? (Same error message repeated?)
2. How did you break out of it?
3. What would prevent this in future sprints?

[After gathering details]

I'll create this lesson with tags: testing, claude-code, validation, python, pytest, debugging

[Uses create_lesson to save to Wiki.js]

Lesson created: "Sprint 16 - Claude Code Infinite Loop on Validation Errors"
Path: /projects/cuisineflow/lessons-learned/sprints/sprint-16-validation-loop.md

Any other lessons from this sprint?

User: Yes, we discovered that JWT token refresh needs special handling

Orchestrator: Excellent - let's capture that too...

[Continues capturing lessons]

All lessons captured! They'll be searchable when planning future sprints.

Would you like me to handle git operations (merge branches, tag release)?
```

## Getting Started

Simply run `/sprint-close` when your sprint is complete. The orchestrator will guide you through:
1. Sprint review
2. Lessons learned capture
3. Wiki.js updates
4. Git operations

**Don't skip this step!** Future sprints will thank you for capturing these insights.
