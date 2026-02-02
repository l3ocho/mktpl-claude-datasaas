---
name: domain-consultation
description: Cross-plugin domain consultation for specialized planning and validation
---

# Domain Consultation

## Purpose

Enables projman agents to detect domain-specific work and consult specialized plugins for expert validation during planning and execution phases. This skill is the backbone of the Domain Advisory Pattern.

---

## When to Use

| Agent | Phase | Action |
|-------|-------|--------|
| Planner | After task sizing, before issue creation | Detect domains, add acceptance criteria |
| Orchestrator | Before marking issue complete | Run domain gates, block if violations |
| Code Reviewer | During review | Include domain compliance in findings |

---

## Domain Detection Rules

| Signal Type | Detection Pattern | Domain Plugin | Action |
|-------------|-------------------|---------------|--------|
| Label-based | `Component/Frontend`, `Component/UI` | viz-platform | Add design system criteria, apply `Domain/Viz` |
| Content-based | Keywords: DMC, Dash, layout, theme, component, dashboard, chart, responsive, color, UI, frontend, Plotly | viz-platform | Same as above |
| Label-based | `Component/Database`, `Component/Data` | data-platform | Add data validation criteria, apply `Domain/Data` |
| Content-based | Keywords: schema, migration, pipeline, dbt, table, column, query, PostgreSQL, lineage, data model | data-platform | Same as above |
| Both signals | Frontend + Data signals present | Both plugins | Apply both sets of criteria |

---

## Planning Protocol

When creating issues, the planner MUST:

1. **Analyze each issue** for domain signals (check labels AND scan description for keywords)

2. **For Domain/Viz issues**, append this acceptance criteria block:
   ```markdown
   ## Design System Compliance
   - [ ] All DMC components validated against registry
   - [ ] Theme tokens used (no hardcoded colors/sizes)
   - [ ] Accessibility check passed (WCAG contrast)
   - [ ] Responsive breakpoints verified
   ```

3. **For Domain/Data issues**, append this acceptance criteria block:
   ```markdown
   ## Data Integrity
   - [ ] Schema changes validated
   - [ ] dbt tests pass
   - [ ] Lineage intact (no orphaned models)
   - [ ] Data types verified
   ```

4. **Apply the corresponding `Domain/*` label** to route the issue through gates

5. **Document in planning summary** which issues have domain gates active

---

## Execution Gate Protocol

Before marking any issue as complete, the orchestrator MUST:

1. **Check issue labels** for `Domain/*` labels

2. **If `Domain/Viz` label present:**
   - Identify files changed by this issue
   - Invoke `/design-gate <path-to-changed-files>`
   - Gate PASS → proceed to mark issue complete
   - Gate FAIL → add comment to issue with failure details, keep issue open

3. **If `Domain/Data` label present:**
   - Identify files changed by this issue
   - Invoke `/data-gate <path-to-changed-files>`
   - Gate PASS → proceed to mark issue complete
   - Gate FAIL → add comment to issue with failure details, keep issue open

4. **If gate command unavailable** (MCP server not running):
   - Warn user: "Domain gate unavailable - proceeding without validation"
   - Proceed with completion (non-blocking degradation)
   - Do NOT silently skip - always inform user

---

## Review Protocol

During code review, the code reviewer SHOULD:

1. After completing standard code quality and security checks, check for `Domain/*` labels

2. **If Domain/Viz:** Include "Design System Compliance" section in review report
   - Reference `/design-review` findings if available
   - Check for hardcoded colors, invalid props, accessibility issues

3. **If Domain/Data:** Include "Data Integrity" section in review report
   - Reference `/data-gate` findings if available
   - Check for schema validity, lineage integrity

---

## Extensibility

To add a new domain (e.g., `Domain/Infra` for cmdb-assistant):

1. **In domain plugin:** Create advisory agent + gate command
   - Agent: `agents/infra-advisor.md`
   - Gate command: `commands/infra-gate.md`
   - Audit skill: `skills/infra-audit.md`

2. **In this skill:** Add detection rules to the Detection Rules table above
   - Define label-based signals (e.g., `Component/Infrastructure`)
   - Define content-based keywords (e.g., "server", "network", "NetBox")

3. **In label taxonomy:** Add `Domain/Infra` label with appropriate color
   - Update `plugins/projman/skills/label-taxonomy/labels-reference.md`

4. **No changes needed** to planner.md or orchestrator.md agent files
   - They read this skill dynamically
   - Detection rules table is the single source of truth

This pattern ensures domain expertise stays in domain plugins while projman orchestrates when to ask.

---

## Domain Acceptance Criteria Templates

### Design System Compliance (Domain/Viz)

```markdown
## Design System Compliance
- [ ] All DMC components validated against registry
- [ ] Theme tokens used (no hardcoded colors/sizes)
- [ ] Accessibility check passed (WCAG contrast)
- [ ] Responsive breakpoints verified
```

### Data Integrity (Domain/Data)

```markdown
## Data Integrity
- [ ] Schema changes validated
- [ ] dbt tests pass
- [ ] Lineage intact (no orphaned models)
- [ ] Data types verified
```

---

## Gate Command Reference

| Domain | Gate Command | Review Command | Advisory Agent |
|--------|--------------|----------------|----------------|
| Viz | `/design-gate <path>` | `/design-review <path>` | `design-reviewer` |
| Data | `/data-gate <path>` | `/data-review <path>` | `data-advisor` |

Gate commands return binary PASS/FAIL for automation.
Review commands return detailed reports for human review.
