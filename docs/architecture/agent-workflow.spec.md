# Agent Workflow - Draw.io Specification

**Target File:** `docs/architecture/agent-workflow.drawio`

**Purpose:** Shows when Planner, Orchestrator, Executor, and Code Reviewer agents trigger during sprint lifecycle.

**Diagram Type:** Swimlane / Sequence Diagram

---

## SWIMLANES

| ID | Label | Color | Position |
|----|-------|-------|----------|
| user-lane | User | #E3F2FD | 1 (leftmost) |
| planner-lane | Planner Agent | #4A90D9 | 2 |
| orchestrator-lane | Orchestrator Agent | #7CB342 | 3 |
| executor-lane | Executor Agent | #FF9800 | 4 |
| reviewer-lane | Code Reviewer Agent | #9C27B0 | 5 |
| gitea-lane | Gitea (Issues + Wiki) | #9E9E9E | 6 (rightmost) |

---

## PHASE 1: SPRINT PLANNING

### Nodes

| ID | Label | Type | Lane | Sequence |
|----|-------|------|------|----------|
| p1-start | /sprint plan | rounded-rect | user-lane | 1 |
| p1-activate | Planner Activates | rectangle | planner-lane | 2 |
| p1-search-lessons | Search Lessons Learned | rectangle | planner-lane | 3 |
| p1-gitea-wiki-query | Query Past Lessons (Wiki) | rectangle | gitea-lane | 4 |
| p1-return-lessons | Return Relevant Lessons | rectangle | planner-lane | 5 |
| p1-clarify | Ask Clarifying Questions | diamond | planner-lane | 6 |
| p1-user-answers | Provide Answers | rectangle | user-lane | 7 |
| p1-create-issues | Create Issues with Labels | rectangle | planner-lane | 8 |
| p1-gitea-create | Store Issues | rectangle | gitea-lane | 9 |
| p1-plan-complete | Planning Complete | rounded-rect | planner-lane | 10 |

### Edges

| From | To | Label | Style |
|------|----|-------|-------|
| p1-start | p1-activate | invokes | solid |
| p1-activate | p1-search-lessons | | solid |
| p1-search-lessons | p1-gitea-wiki-query | REST API (search_lessons) | solid |
| p1-gitea-wiki-query | p1-return-lessons | lessons data | dashed |
| p1-return-lessons | p1-clarify | | solid |
| p1-clarify | p1-user-answers | questions | solid |
| p1-user-answers | p1-clarify | answers | dashed |
| p1-clarify | p1-create-issues | | solid |
| p1-create-issues | p1-gitea-create | REST API | solid |
| p1-gitea-create | p1-plan-complete | confirm | dashed |

---

## PHASE 2: SPRINT EXECUTION

### Nodes

| ID | Label | Type | Lane | Sequence |
|----|-------|------|------|----------|
| p2-start | /sprint start | rounded-rect | user-lane | 11 |
| p2-orch-activate | Orchestrator Activates | rectangle | orchestrator-lane | 12 |
| p2-fetch-issues | Fetch Sprint Issues | rectangle | orchestrator-lane | 13 |
| p2-gitea-list | List Open Issues | rectangle | gitea-lane | 14 |
| p2-sequence | Sequence Work (Dependencies) | rectangle | orchestrator-lane | 15 |
| p2-dispatch | Dispatch Task | rectangle | orchestrator-lane | 16 |
| p2-exec-activate | Executor Activates | rectangle | executor-lane | 17 |
| p2-implement | Implement Task | rectangle | executor-lane | 18 |
| p2-update-status | Update Issue Status | rectangle | executor-lane | 19 |
| p2-gitea-update | Update Issue | rectangle | gitea-lane | 20 |
| p2-report | Report Completion | rectangle | executor-lane | 21 |
| p2-loop | More Tasks? | diamond | orchestrator-lane | 22 |
| p2-exec-complete | Execution Complete | rounded-rect | orchestrator-lane | 23 |

### Edges

| From | To | Label | Style |
|------|----|-------|-------|
| p2-start | p2-orch-activate | invokes | solid |
| p2-orch-activate | p2-fetch-issues | | solid |
| p2-fetch-issues | p2-gitea-list | REST API | solid |
| p2-gitea-list | p2-sequence | issues data | dashed |
| p2-sequence | p2-dispatch | parallel batching | solid |
| p2-dispatch | p2-exec-activate | execution prompt | solid |
| p2-exec-activate | p2-implement | | solid |
| p2-implement | p2-update-status | | solid |
| p2-update-status | p2-gitea-update | REST API | solid |
| p2-gitea-update | p2-report | confirm | dashed |
| p2-report | p2-loop | | solid |
| p2-loop | p2-dispatch | yes | solid |
| p2-loop | p2-exec-complete | no | solid |

---

## PHASE 2.5: CODE REVIEW (Pre-Close)

### Nodes

| ID | Label | Type | Lane | Sequence |
|----|-------|------|------|----------|
| p25-start | /review | rounded-rect | user-lane | 24 |
| p25-reviewer-activate | Code Reviewer Activates | rectangle | reviewer-lane | 25 |
| p25-scan-changes | Scan Recent Changes | rectangle | reviewer-lane | 26 |
| p25-check-quality | Check Code Quality | rectangle | reviewer-lane | 27 |
| p25-security-scan | Security Scan | rectangle | reviewer-lane | 28 |
| p25-report | Generate Review Report | rectangle | reviewer-lane | 29 |
| p25-complete | Review Complete | rounded-rect | reviewer-lane | 30 |

### Edges

| From | To | Label | Style |
|------|----|-------|-------|
| p25-start | p25-reviewer-activate | invokes | solid |
| p25-reviewer-activate | p25-scan-changes | | solid |
| p25-scan-changes | p25-check-quality | | solid |
| p25-check-quality | p25-security-scan | | solid |
| p25-security-scan | p25-report | | solid |
| p25-report | p25-complete | | solid |

---

## PHASE 3: SPRINT CLOSE

### Nodes

| ID | Label | Type | Lane | Sequence |
|----|-------|------|------|----------|
| p3-start | /sprint close | rounded-rect | user-lane | 31 |
| p3-orch-activate | Orchestrator Activates | rectangle | orchestrator-lane | 32 |
| p3-review | Review Sprint | rectangle | orchestrator-lane | 33 |
| p3-gitea-status | Get Final Status | rectangle | gitea-lane | 34 |
| p3-capture | Capture Lessons Learned | rectangle | orchestrator-lane | 35 |
| p3-user-input | Confirm Lessons | diamond | user-lane | 36 |
| p3-create-wiki | Create Wiki Pages | rectangle | orchestrator-lane | 37 |
| p3-gitea-wiki-create | Store Lessons (Wiki) | rectangle | gitea-lane | 38 |
| p3-close-issues | Close Issues | rectangle | orchestrator-lane | 39 |
| p3-gitea-close | Mark Closed | rectangle | gitea-lane | 40 |
| p3-complete | Sprint Closed | rounded-rect | orchestrator-lane | 41 |

### Edges

| From | To | Label | Style |
|------|----|-------|-------|
| p3-start | p3-orch-activate | invokes | solid |
| p3-orch-activate | p3-review | | solid |
| p3-review | p3-gitea-status | REST API | solid |
| p3-gitea-status | p3-capture | status data | dashed |
| p3-capture | p3-user-input | proposed lessons | solid |
| p3-user-input | p3-create-wiki | confirmed | solid |
| p3-create-wiki | p3-gitea-wiki-create | REST API (create_lesson) | solid |
| p3-gitea-wiki-create | p3-close-issues | confirm | dashed |
| p3-close-issues | p3-gitea-close | REST API | solid |
| p3-gitea-close | p3-complete | confirm | dashed |

---

## LAYOUT NOTES

```
+--------+------------+---------------+------------+----------+------------------+
|  User  |  Planner   | Orchestrator  |  Executor  | Reviewer | Gitea            |
|        |            |               |            |          | (Issues + Wiki)  |
+--------+------------+---------------+------------+----------+------------------+
|        |            |               |            |          |                  |
| PHASE 1: SPRINT PLANNING                                                       |
|-------------------------------------------------------------------------------|
|  O     |            |               |            |          |                  |
|  |     |            |               |            |          |                  |
|  +---->| O          |               |            |          |                  |
|        | |          |               |            |          |                  |
|        | +----------|---------------|------------|--------->| O (Wiki Query)   |
|        | |<---------|---------------|------------|----------+ |                |
|        | |          |               |            |          |                  |
|        | O<>        |               |            |          |                  |
|  O<--->+ |          |               |            |          |                  |
|        | |          |               |            |          |                  |
|        | +----------|---------------|------------|--------->| O (Issues)       |
|        | O          |               |            |          |                  |
|        |            |               |            |          |                  |
|-------------------------------------------------------------------------------|
| PHASE 2: SPRINT EXECUTION                                                      |
|-------------------------------------------------------------------------------|
|  O     |            |               |            |          |                  |
|  |     |            |               |            |          |                  |
|  +-----|----------->| O             |            |          |                  |
|        |            | |             |            |          |                  |
|        |            | +-------------|------------|--------->| O (Issues)       |
|        |            | |<------------|------------|----------+ |                |
|        |            | |             |            |          |                  |
|        |            | +------------>| O          |          |                  |
|        |            |               | |          |          |                  |
|        |            |               | +----------|--------->| O (Issues)       |
|        |            |               | |<---------|----------+ |                |
|        |            | O<------------+ |          |          |                  |
|        |            | |             |            |          |                  |
|        |            | O (loop)      |            |          |                  |
|        |            |               |            |          |                  |
|-------------------------------------------------------------------------------|
| PHASE 2.5: CODE REVIEW                                                         |
|-------------------------------------------------------------------------------|
|  O     |            |               |            |          |                  |
|  |     |            |               |            |          |                  |
|  +-----|------------|---------------|----------->| O        |                  |
|        |            |               |            | |        |                  |
|        |            |               |            | O->O->O  |                  |
|        |            |               |            | |        |                  |
|        |            |               |            | O        |                  |
|        |            |               |            |          |                  |
|-------------------------------------------------------------------------------|
| PHASE 3: SPRINT CLOSE                                                          |
|-------------------------------------------------------------------------------|
|  O     |            |               |            |          |                  |
|  |     |            |               |            |          |                  |
|  +-----|----------->| O             |            |          |                  |
|        |            | +-------------|------------|--------->| O (Issues)       |
|        |            | |<------------|------------|----------+ |                |
|        |            | |             |            |          |                  |
|  O<----|-----------<+ |             |            |          |                  |
|  +-----|----------->| |             |            |          |                  |
|        |            | +-------------|------------|--------->| O (Wiki Create)  |
|        |            | |<------------|------------|----------+ |                |
|        |            | +-------------|------------|--------->| O (Issues Close) |
|        |            | O             |            |          |                  |
+--------+------------+---------------+------------+----------+------------------+
```

---

## COLOR LEGEND

| Color | Hex | Meaning |
|-------|-----|---------|
| Light Blue | #E3F2FD | User actions |
| Blue | #4A90D9 | Planner Agent |
| Green | #7CB342 | Orchestrator Agent |
| Orange | #FF9800 | Executor Agent |
| Purple | #9C27B0 | Code Reviewer Agent |
| Gray | #9E9E9E | External Services (Gitea) |

---

## SHAPE LEGEND

| Shape | Meaning |
|-------|---------|
| Rounded Rectangle | Start/End points (commands) |
| Rectangle | Process/Action |
| Diamond | Decision point |
| Cylinder | Data store (in component map) |

---

## ARROW LEGEND

| Style | Meaning |
|-------|---------|
| Solid | Action/Request |
| Dashed | Response/Data return |

---

## ARCHITECTURE NOTES

- **Gitea provides BOTH issue tracking AND wiki** (no separate wiki service)
- All wiki operations use Gitea REST API via MCP tools
- Lessons learned stored in Gitea Wiki under `lessons-learned/sprints/`
- MCP tools: `search_lessons`, `create_lesson`, `list_wiki_pages`, `get_wiki_page`
- Four-agent model: Planner, Orchestrator, Executor, Code Reviewer
