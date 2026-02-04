---
name: planning-workflow
description: The complete sprint planning process steps
---

# Planning Workflow

## Purpose

Defines the complete 11-step planning workflow from validation through approval.

## When to Use

- **Planner agent**: When executing `/sprint-plan`
- **Commands**: `/sprint-plan`

---

## Workflow Steps

### 1. Understand Sprint Goals

Ask clarifying questions:
- What are the sprint objectives?
- What's the scope and priority?
- Are there any constraints (time, resources, dependencies)?
- What's the desired outcome?

**Never rush - take time to understand requirements fully.**

### 2. Run Pre-Planning Validations

Execute in order:
1. **Branch detection** - See `skills/branch-security.md`
2. **Repository org check** - See `skills/repo-validation.md`
3. **Label taxonomy validation** - See `skills/repo-validation.md`

**STOP if any validation fails.**

### 3. Detect Input Source

Follow `skills/input-detection.md`:
1. **Check for approved RFCs** (Priority 0)
2. Check for `docs/changes/*.md` files
3. Check for existing wiki proposal
4. If neither: use conversation context
5. If ambiguous: ask user

### 3a. RFC Status Update (if RFC selected)

If input source is an RFC:
1. **Note the RFC number** for later status update
2. RFC status update happens AFTER sprint approval (Step 11)
3. The RFC provides the planning context - use its Summary, Motivation, and Design sections

### 4. Search Relevant Lessons Learned

Follow `skills/lessons-learned.md`:
```python
search_lessons(repo="org/repo", query="sprint keywords", tags=["relevant", "tags"])
```

Present findings to user before proceeding.

### 5. Create/Update Wiki Proposal

Follow `skills/wiki-conventions.md`:
- If local file: migrate content to wiki, create proposal page
- If conversation: create proposal from discussion
- If existing wiki: skip creation, use as-is

### 6. Create Wiki Implementation Page

Follow `skills/wiki-conventions.md`:
- Create `Change VXX.X.X: Proposal (Implementation N)`
- Update proposal page with link to implementation

### 7. Architecture Analysis

Think through:
- What components will be affected?
- What are the integration points?
- Are there edge cases to handle?
- What dependencies exist?
- What are potential risks?

### 8. Draft Issue Specifications (DO NOT create yet)

Follow `skills/issue-conventions.md` and `skills/task-sizing.md` to prepare the complete specification for ALL issues. **Do NOT call `create_issue` yet.**

For each issue, resolve completely:
- Title: `[Sprint XX] <type>: <description>`
- Body: Full description with wiki reference, acceptance criteria, technical notes
- Labels: Use `suggest_labels` to determine, then finalize the list
- Milestone: The sprint milestone (create first if needed)
- Dependencies: Which issues depend on which (by draft order index)

**Refuse to create L/XL tasks without breakdown.**

Output: A complete execution manifest per `skills/batch-execution.md` Phase 2 format.

### 8a. Batch Execute Issue Creation

Follow `skills/batch-execution.md` Phase 3:
1. Execute all `create_issue` calls — collect returned issue numbers
2. Execute all `create_issue_dependency` calls — using collected numbers
3. Assign all issues to milestone
4. Report batch results per Phase 4 format

**Only `skills/mcp-tools-reference.md` is needed for this step.** Do NOT re-read other skill files.

### 9. (Merged into Step 8a)

Dependencies are now created as part of the batch execution in Step 8a. No separate step needed.

### 10. Create or Select Milestone (before batch)

**This step runs BEFORE Step 8a** — the milestone must exist before batch issue creation can assign to it.

```python
create_milestone(
    repo="org/repo",
    title="Sprint 17 - Feature Name",
    description="Sprint description",
    due_on="2025-02-01T00:00:00Z"
)
```

If milestone already exists, select it. Record the milestone ID for use in the batch manifest.

### 11. Request Sprint Approval

Follow `skills/sprint-approval.md`:
- Present approval request with scope summary
- Wait for explicit user approval
- Record approval in milestone description

### 12. Update RFC Status (if applicable)

If planning input was an RFC:

1. **Fetch RFC page:**
   ```python
   get_wiki_page(page_name="RFC-NNNN:-Title", repo="org/repo")
   ```

2. **Update RFC page:**
   - Change status: Approved → Implementing
   - Add Sprint reference to frontmatter
   - Add Implementation section with sprint details and issue links
   ```python
   update_wiki_page(
       page_name="RFC-NNNN:-Title",
       content="[updated content with Implementing status]",
       repo="org/repo"
   )
   ```

3. **Update RFC-Index:**
   - Remove from "## Approved" section
   - Add to "## Implementing" section with sprint reference

---

## Cleanup After Planning

- Delete local input file (wiki is now source of truth)
- Summarize architectural decisions
- List created issues with labels
- Document dependency graph
- Provide sprint overview with wiki links

---

## Visual Output

Display header at start:
```
╔══════════════════════════════════════════════════════════════════╗
║  📋 PROJMAN                                                      ║
║  🎯 PLANNING                                                     ║
║  [Sprint Name]                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```
