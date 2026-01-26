---
description: Complete sprint and capture lessons learned to Gitea Wiki
---

# Close Sprint and Capture Lessons Learned

This command completes the sprint and captures lessons learned to Gitea Wiki. **This is critical** - after 15 sprints without lesson capture, repeated mistakes occurred (e.g., Claude Code infinite loops 2-3 times on similar issues).

## Why Lessons Learned Matter

**Problem:** Without systematic lesson capture, teams repeat the same mistakes:
- Claude Code infinite loops on similar issues (happened 2-3 times)
- Same architectural mistakes (multiple occurrences)
- Forgotten optimizations (re-discovered each time)

**Solution:** Mandatory lessons learned capture at sprint close, searchable at sprint start.

## Sprint Close Workflow

The orchestrator agent will guide you through:

1. **Review Sprint Completion**
   - Use `list_issues` to verify all issues are closed or moved to backlog
   - Check milestone completion status
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

4. **Save to Gitea Wiki**
   - Use `create_lesson` to save lessons to Gitea Wiki
   - Create lessons in project wiki under `lessons-learned/sprints/`
   - Make lessons searchable for future sprints

5. **Update Wiki Implementation Page**
   - Use `get_wiki_page` to fetch the current implementation page
   - Update status from "In Progress" to "Implemented" (or "Partial"/"Failed")
   - Add completion date
   - Link to lessons learned created in step 4
   - Use `update_wiki_page` to save changes

6. **Update Wiki Proposal Page**
   - Check if all implementations for this proposal are complete
   - If all complete: Update proposal status to "Implemented"
   - If partial: Keep status as "In Progress", note completed implementations
   - Add summary of what was accomplished

7. **Git Operations**
   - Commit any remaining work
   - Merge feature branches if needed
   - Clean up merged branches
   - Tag sprint completion

8. **Close Milestone**
   - Use `update_milestone` to close the sprint milestone
   - Document final completion status

## MCP Tools Available

**Gitea Tools:**
- `list_issues` - Review sprint issues (completed and incomplete)
- `get_issue` - Get detailed issue information for retrospective
- `update_issue` - Move incomplete issues to next sprint

**Milestone Tools:**
- `get_milestone` - Get milestone status
- `update_milestone` - Close milestone

**Lessons Learned Tools (Gitea Wiki):**
- `create_lesson` - Create lessons learned entry
- `search_lessons` - Check for similar existing lessons
- `list_wiki_pages` - Check existing lessons learned
- `get_wiki_page` - Read existing lessons or implementation pages
- `update_wiki_page` - Update implementation/proposal status

## Lesson Structure

Lessons should follow this structure:

```markdown
# Sprint X - [Lesson Title]

## Metadata
- **Implementation:** [Change VXX.X.X (Impl N)](wiki-link)
- **Issues:** #45, #46, #47
- **Sprint:** Sprint X

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

**IMPORTANT:** Always include the Implementation link in the Metadata section. This enables bidirectional traceability between lessons and the work that generated them.

## Example Lessons Learned

**Example 1: Technical Gotcha**
```markdown
# Sprint 16 - Claude Code Infinite Loop on Validation Errors

## Metadata
- **Implementation:** [Change V1.2.0 (Impl 1)](https://gitea.example.com/org/repo/wiki/Change-V1.2.0%3A-Proposal-(Implementation-1))
- **Issues:** #45, #46
- **Sprint:** Sprint 16

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

## Metadata
- **Implementation:** [Change V2.0.0 (Impl 1)](https://gitea.example.com/org/repo/wiki/Change-V2.0.0%3A-Proposal-(Implementation-1))
- **Issues:** #32, #33, #34
- **Sprint:** Sprint 14

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
5. Create lessons in Gitea Wiki using `create_lesson`
6. Ensure lessons are discoverable for future sprints
7. Handle git operations and milestone closure

## Example Sprint Close Session

```
User: /sprint-close
Orchestrator: Let's close the sprint and capture lessons learned.

First, let me review the sprint completion...

[Uses list_issues to check sprint status]

Sprint 18 Summary:
- 8 issues planned
- 7 completed (87.5%)
- 1 moved to backlog (#52: Deploy auth service - blocked by infra)

Great progress! Now, let's capture lessons learned.

What challenges did you face this sprint?

User: Claude Code got stuck in a loop when pytest validation tests failed

Orchestrator: That's a valuable lesson - this prevents future frustration.

Let me ask some clarifying questions:
1. What caused the loop? (Same error message repeated?)
2. How did you break out of it?
3. What would prevent this in future sprints?

[After gathering details]

I'll create this lesson with tags: testing, claude-code, validation, python, pytest, debugging

[Uses create_lesson to save to Gitea Wiki]

Lesson created: "Sprint 18 - Claude Code Infinite Loop on Validation Errors"
Saved to Gitea Wiki with appropriate tags.

Any other lessons from this sprint?

User: Yes, we discovered that JWT token refresh needs special handling

Orchestrator: Excellent - let's capture that too...

[Continues capturing lessons]

All lessons captured! They'll be searchable when planning future sprints.

Would you like me to handle git operations?
- Commit any remaining changes
- Merge feature branches to development
- Tag sprint completion (v0.18.0)
- Clean up merged branches
- Close milestone

[Y/n]
```

## Getting Started

Simply run `/sprint-close` when your sprint is complete. The orchestrator will guide you through:
1. Sprint review
2. Lessons learned capture
3. Gitea Wiki updates
4. Git operations
5. Milestone closure

**Don't skip this step!** Future sprints will thank you for capturing these insights.
