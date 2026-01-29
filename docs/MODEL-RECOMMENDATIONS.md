# Model Recommendations

Guidelines for selecting Claude models (opus, sonnet, haiku) for plugin agents.

---

## Model Overview

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| **Opus** | Complex reasoning, architecture decisions, security analysis | Highest | Slower |
| **Sonnet** | Implementation, coordination, standard tasks | Medium | Balanced |
| **Haiku** | Simple validation, quick checks, status queries | Lowest | Fastest |

---

## Task-Type Recommendations

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Architecture decisions | Opus | Requires deep reasoning, trade-off analysis |
| Security analysis | Opus | Critical thinking, vulnerability pattern recognition |
| Code review (quality) | Opus | Thorough analysis, edge case detection |
| Sprint planning | Opus | Strategic thinking, dependency analysis |
| Complex data analysis | Opus | Multi-step reasoning, insight generation |
| Code implementation | Sonnet | Fast, capable code generation |
| Coordination/dispatch | Sonnet | Task management, status tracking |
| Data transformation | Sonnet | ETL operations, query building |
| Documentation | Sonnet | Clear writing, structure |
| Simple validation | Haiku | Fast prop checks, schema validation |
| Status checks | Haiku | Quick queries, cost-effective |
| Quick verification | Haiku | Simple pass/fail checks |

---

## Agent Model Assignments

### projman (Sprint Management)

| Agent | Model | Rationale |
|-------|-------|-----------|
| `planner` | opus | Architecture decisions, issue structuring |
| `orchestrator` | sonnet | Coordination, parallel execution |
| `executor` | sonnet | Code implementation |
| `code-reviewer` | opus | Quality review, security analysis |

### pr-review (PR Analysis)

| Agent | Model | Rationale |
|-------|-------|-----------|
| `coordinator` | sonnet | Task dispatch, result aggregation |
| `security-reviewer` | opus | Security vulnerability detection |
| `performance-analyst` | sonnet | Pattern recognition |
| `maintainability-auditor` | sonnet | Code quality checks |
| `test-validator` | sonnet | Test coverage analysis |

### code-sentinel (Security & Refactoring)

| Agent | Model | Rationale |
|-------|-------|-----------|
| `security-reviewer` | opus | Security scanning |
| `refactor-advisor` | sonnet | Refactoring suggestions |

### data-platform (Data Engineering)

| Agent | Model | Rationale |
|-------|-------|-----------|
| `data-analysis` | opus | Complex data insights |
| `data-ingestion` | sonnet | ETL operations |

### viz-platform (Visualization)

| Agent | Model | Rationale |
|-------|-------|-----------|
| `component-check` | haiku | Simple prop validation |
| `layout-builder` | sonnet | UI construction |
| `theme-setup` | sonnet | Design configuration |

### contract-validator (Compatibility)

| Agent | Model | Rationale |
|-------|-------|-----------|
| `full-validation` | sonnet | Contract checking |
| `agent-check` | haiku | Quick verification |

---

## Configuration Schema

### Agent-Level (Frontmatter)

Add `model` field to agent YAML frontmatter:

```yaml
---
name: planner
description: Sprint planning agent
model: opus
---
```

**Valid values:** `opus`, `sonnet`, `haiku`

### Plugin-Level (plugin.json)

Add `defaultModel` for plugin-wide fallback:

```json
{
  "name": "projman",
  "version": "3.4.0",
  "defaultModel": "sonnet"
}
```

---

## Inheritance Chain

Model selection follows this precedence:

```
1. Agent model field (highest priority)
      ↓ if not specified
2. Plugin defaultModel (plugin.json)
      ↓ if not specified
3. System default: sonnet
```

**Example:**
- Agent has `model: opus` → Uses opus
- Agent has no model, plugin has `defaultModel: sonnet` → Uses sonnet
- Neither specified → Uses sonnet (system default)

---

## Cost Optimization Tips

1. **Default to Sonnet** - Good balance for most tasks
2. **Reserve Opus** for critical decisions (security, architecture)
3. **Use Haiku** for validation and quick checks
4. **Batch simple tasks** - Use haiku for parallel validation

---

## See Also

- [Configuration Guide](CONFIGURATION.md) - Full configuration reference
- [Plugin Development](../README.md) - Adding new plugins
