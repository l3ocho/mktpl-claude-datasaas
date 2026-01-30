# CLAUDE.md Analysis Workflow

This skill defines the workflow for analyzing CLAUDE.md files.

## Analysis Steps

1. **Locate File** - Find CLAUDE.md in project root
2. **Parse Structure** - Extract headers and sections
3. **Evaluate Content** - Score against criteria
4. **Detect Plugins** - Identify active marketplace plugins
5. **Check Integration** - Verify plugin references
6. **Generate Report** - Provide scored assessment

## Content Analysis

### What to Check

| Area | Check For |
|------|-----------|
| Structure | Header hierarchy, section ordering, grouping |
| Clarity | Clear instructions, examples, unambiguous language |
| Completeness | Required sections present, workflows documented |
| Conciseness | No redundancy, efficient density, appropriate length |

### Required Sections Check

1. Project Overview - present?
2. Quick Start - present with commands?
3. Critical Rules - present?
4. **Pre-Change Protocol** - present? (HIGH PRIORITY if missing)

## Plugin Integration Analysis

### Detection Method

1. Read `.claude/settings.local.json` for enabled MCP servers
2. Map MCP servers to plugins:
   - `gitea` -> projman
   - `netbox` -> cmdb-assistant
3. Check for hook-based plugins (project-hygiene)
4. Scan CLAUDE.md for plugin references

### Coverage Scoring

For each detected plugin, verify CLAUDE.md contains:
- Plugin section header or mention
- Available commands documentation
- MCP tools reference (if applicable)
- Usage guidelines

Coverage = (plugins referenced / plugins detected) * 100%

## Report Format

```
CLAUDE.md Analysis Report
=========================

File: /path/to/project/CLAUDE.md
Lines: N
Last Modified: YYYY-MM-DD

Overall Score: NN/100

Category Scores:
- Structure:    NN/25 (Rating)
- Clarity:      NN/25 (Rating)
- Completeness: NN/25 (Rating)
- Conciseness:  NN/25 (Rating)

Strengths:
+ [Positive finding]

Issues Found:

N. [SEVERITY] Issue description (location)
   Context explaining the problem.
   Impact: What happens if not fixed.

Recommendations:
N. Action to take (priority: high/medium/low)

---

Plugin Integration Analysis
===========================

Detected Active Plugins:
  [check] plugin-name (via detection method)

Plugin Coverage: NN% (N/N plugins referenced)

Missing Integration Content:
N. plugin-name
   What to add.
```

## Issue Severity

| Level | When to Use |
|-------|-------------|
| HIGH | Missing mandatory sections, security issues |
| MEDIUM | Missing recommended content, duplicate content |
| LOW | Formatting issues, minor improvements |

## Follow-Up Actions

After analysis, offer:
1. Implement all content recommendations
2. Add missing plugin integrations
3. Do both (recommended)
4. Show preview of changes first
