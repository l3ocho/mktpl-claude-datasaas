---
description: Complete sprint and capture lessons learned to Gitea Wiki
agent: orchestrator
---

# Close Sprint and Capture Lessons Learned

## Skills Required

- skills/mcp-tools-reference.md
- skills/lessons-learned.md
- skills/wiki-conventions.md
- skills/progress-tracking.md
- skills/git-workflow.md

## Purpose

Complete the sprint, capture lessons learned to Gitea Wiki, and update documentation. This is critical for preventing repeated mistakes across sprints.

## Invocation

Run `/sprint-close` when sprint work is complete.

## Workflow

Execute the sprint close workflow:

1. **Review Sprint Completion** - Verify issues closed or moved to backlog
2. **Capture Lessons Learned** - Interview user about challenges and insights
3. **Tag for Discoverability** - Apply technology, component, and pattern tags
4. **Save to Gitea Wiki** - Use `create_lesson` with metadata and implementation link
5. **Update Wiki Implementation Page** - Change status to Implemented/Partial/Failed
6. **Update Wiki Proposal Page** - Update overall status if all implementations complete
7. **New Command Verification** - Remind user new commands require session restart
8. **Update CHANGELOG** (MANDATORY) - Add changes to `[Unreleased]` section
9. **Version Check** - Run `/suggest-version` to recommend version bump
10. **Git Operations** - Commit, merge, tag, clean up branches
11. **Close Milestone** - Update milestone state to closed

**Don't skip lessons learned!** Future sprints will benefit from captured insights.

## Visual Output

```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🏁 CLOSING                                                      ║
║  [Sprint Name]                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```
