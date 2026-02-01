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

### 8. Create Gitea Issues

Follow `skills/issue-conventions.md` and `skills/task-sizing.md`:
- Use proper title format: `[Sprint XX] <type>: <description>`
- Include wiki implementation reference
- Apply appropriate labels using `suggest_labels`
- **Refuse to create L/XL tasks without breakdown**

### 9. Set Up Dependencies

```python
create_issue_dependency(repo="org/repo", issue_number=46, depends_on=45)
```

### 10. Create or Select Milestone

```python
create_milestone(
    repo="org/repo",
    title="Sprint 17 - Feature Name",
    description="Sprint description",
    due_on="2025-02-01T00:00:00Z"
)
```

Assign issues to the milestone.

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
