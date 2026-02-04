---
description: Complete sprint and capture lessons learned to Gitea Wiki
agent: orchestrator
---

# Close Sprint and Capture Lessons Learned

## Skills Required

- skills/mcp-tools-reference.md
- skills/lessons-learned.md
- skills/wiki-conventions.md
- skills/rfc-workflow.md
- skills/progress-tracking.md
- skills/git-workflow.md
- skills/sprint-lifecycle.md
- skills/token-budget-report.md

## Purpose

Complete the sprint, capture lessons learned to Gitea Wiki, and update documentation. This is critical for preventing repeated mistakes across sprints.

## Invocation

Run `/sprint-close` when sprint work is complete.

## Workflow

Execute the sprint close workflow:

0. **Check Lifecycle State** - Execute `skills/sprint-lifecycle.md` check protocol. Expect `Sprint/Reviewing`. Clear all Sprint/* labels (return to idle) at the END of close workflow, after all other steps. Warn if in wrong state (allow with `--force`).
1. **Review Sprint Completion** - Verify issues closed or moved to backlog
2. **Capture Lessons Learned** - Interview user about challenges and insights
3. **Tag for Discoverability** - Apply technology, component, and pattern tags
4. **Save to Gitea Wiki** - Use `create_lesson` with metadata and implementation link
5. **Update Wiki Implementation Page** - Change status to Implemented/Partial/Failed
6. **Update Wiki Proposal Page** - Update overall status if all implementations complete
7. **Update RFC Status (if applicable)** - See RFC Update section below
8. **New Command Verification** - Remind user new commands require session restart
9. **Update CHANGELOG** (MANDATORY) - Add changes to `[Unreleased]` section
10. **Version Check** - Run `/suggest-version` to recommend version bump
11. **Git Operations** - Commit, merge, tag, clean up branches
12. **Close Milestone** - Update milestone state to closed

## RFC Status Update (Step 7)

If the sprint was linked to an RFC:

1. **Check Sprint Completion Status:**
   - All issues completed → RFC status = Implemented
   - Partial completion → RFC status stays Implementing (note progress)
   - Blocked/Failed → RFC status reverts to Draft (with notes)

2. **Update RFC Page (if Implemented):**
   - Change status: Implementing → Implemented
   - Add Completion section with date and release version
   - Link to lessons learned page
   ```python
   update_wiki_page(
       page_name="RFC-NNNN:-Title",
       content="[content with Implemented status and completion details]",
       repo="org/repo"
   )
   ```

3. **Update RFC-Index:**
   - Remove from "## Implementing" section
   - Add to "## Implemented" section with completion date and release

4. **Handle Partial Completion:**
   - Keep RFC in Implementing status
   - Add progress notes to Implementation section
   - Next sprint can continue the work

**Don't skip lessons learned!** Future sprints will benefit from captured insights.

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🏁 CLOSING                                                      ║
║  [Sprint Name]                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

## Final Step: Token Budget Report

After displaying the closing summary and completing all workflow steps, generate a Token Budget Report per `skills/token-budget-report.md`.

- Phase: CLOSING
- List all skills that were loaded during this closing session
- Use the orchestrator agent's model (sonnet) for agent overhead
- Display the formatted report
