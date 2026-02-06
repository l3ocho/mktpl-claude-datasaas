---
description: Token consumption estimation model and display format for sprint workflows
---

# Token Budget Report

## Purpose

Provides directional token consumption estimates at sprint workflow boundaries. Not exact — Claude Code doesn't expose token metrics — but accurate enough to identify which phases and components consume the most context budget.

## When to Display

- End of `/sprint plan` (after all issues created)
- End of `/sprint close` (after lessons captured)
- On explicit request: `/sprint status --tokens`

---

## Estimation Model

### MCP Tool Definitions (Static Overhead)

These are loaded once at session start. Update this table if MCP servers change.

| MCP Server | Default Tools | Est. Tokens | With Module Filter |
|------------|--------------|-------------|-------------------|
| netbox | 182 | ~19,810 | ~4,500 (dcim,ipam,virt,extras) |
| gitea | 36 | ~4,785 | — |
| data-platform | 32 | ~3,458 | — |
| viz-platform | 20 | ~3,055 | — |
| contract-validator | 8 | ~1,048 | — |
| **Total (default)** | **278** | **~32,156** | — |
| **Total (filtered)** | **~139** | **~16,846** | — |

### Skill Loading (Per Phase)

| Phase | Typical Skills Loaded | Est. Tokens |
|-------|----------------------|-------------|
| Planning (`/sprint plan`) | mcp-tools-reference, label-taxonomy, sprint-planning, architecture-analysis, rfc-workflow | ~3,000–5,000 |
| Execution (`/sprint start`) | mcp-tools-reference, branch-security, plan-then-batch | ~2,000–3,000 |
| Review (`/sprint review`) | mcp-tools-reference, review-checklist | ~1,500–2,500 |
| Close (`/sprint close`) | mcp-tools-reference, sprint-lifecycle, lessons-learned | ~2,000–3,000 |

To get actual numbers: count characters in each skill file loaded during the phase, divide by 4.

### Agent Overhead

| Agent | Model | Est. Overhead per Invocation |
|-------|-------|------------------------------|
| Planner | sonnet | ~500 tokens (frontmatter + system context) |
| Orchestrator | sonnet | ~500 tokens |
| Executor | sonnet | ~400 tokens |
| Code Reviewer | sonnet | ~400 tokens |

---

## Display Format

```
+-- Token Budget Report -----------------------------------------------+
|  Phase: [PLANNING / CLOSING]                                         |
|  Sprint: [Sprint Name]                                               |
+----------------------------------------------------------------------+
|                                                                      |
|  MCP Overhead (session-wide):                                        |
|    netbox ........... ~4,500 tk  (filtered: dcim,ipam,virt,extras)   |
|    gitea ............ ~4,785 tk                                      |
|    data-platform .... ~3,458 tk                                      |
|    viz-platform ..... ~3,055 tk                                      |
|    contract-valid ... ~1,048 tk                                      |
|    Subtotal ......... ~16,846 tk                                     |
|                                                                      |
|  This Phase:                                                         |
|    Skills loaded .... ~X,XXX tk  (N files)                           |
|    Agent overhead ... ~X,XXX tk  (model: sonnet)                     |
|    Command file ..... ~XXX tk                                        |
|    Subtotal ......... ~X,XXX tk                                      |
|                                                                      |
|  Estimated Session Total: ~XX,XXX tk                                 |
|  Typical Claude Code Budget: ~200,000 tk                             |
|  Estimated Usage: ~XX%                                               |
|                                                                      |
|  Tip: Run `/doctor` for exact MCP overhead numbers.                  |
+----------------------------------------------------------------------+
```

---

## Instructions for the Agent

When generating this report:

1. **MCP Overhead**: List the MCP servers from `.mcp.json` and use the static token estimates from the table above. If `NETBOX_ENABLED_MODULES` is set in the environment, use the filtered estimate for netbox.

2. **Skills Loaded**: Count the skill files that were loaded (referenced in the command's "Skills Required" section). Estimate tokens by reading each file's character count and dividing by 4.

3. **Agent Overhead**: Use the table above based on which agent ran during this phase.

4. **Totals**: Sum the phase subtotal. Add to MCP overhead for session estimate.

5. **Percentage**: Express as a percentage of ~200,000 tokens (typical Claude Code context window).

---

## Accuracy Disclaimer

These are estimates based on known file sizes and static overhead tables. Actual consumption varies based on:
- Conversation length
- Tool call results (especially large grep/read outputs)
- File content read during the session
- Number of agent invocations

For exact MCP overhead, run `/doctor`.

This report helps identify which *components* consume the most budget — not the precise total.
