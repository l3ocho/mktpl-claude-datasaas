---
description: Analyze CLAUDE.md for optimization opportunities and plugin integration
---

# Analyze CLAUDE.md

This command analyzes your project's CLAUDE.md file and provides a detailed report on optimization opportunities and plugin integration status.

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚙️ CONFIG-MAINTAINER · CLAUDE.md Analysis                       │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the analysis.

## What This Command Does

1. **Read CLAUDE.md** - Locates and reads the project's CLAUDE.md file
2. **Analyze Structure** - Evaluates organization, headers, and flow
3. **Check Content** - Reviews clarity, completeness, and conciseness
4. **Identify Issues** - Finds redundancy, verbosity, and missing sections
5. **Detect Active Plugins** - Identifies marketplace plugins enabled in the project
6. **Check Plugin Integration** - Verifies CLAUDE.md references active plugins
7. **Generate Report** - Provides scored assessment with recommendations

## Usage

```
/config-analyze
```

Or invoke the maintainer agent directly:

```
Analyze the CLAUDE.md file in this project
```

## Analysis Criteria

### Structure (25 points)
- Logical section ordering
- Clear header hierarchy
- Easy navigation
- Appropriate grouping

### Clarity (25 points)
- Clear instructions
- Good examples
- Unambiguous language
- Appropriate detail level

### Completeness (25 points)
- Project overview present
- Quick start commands documented
- Critical rules highlighted
- Key workflows covered
- **Pre-Change Protocol section present** (MANDATORY - see below)

### Conciseness (25 points)
- No unnecessary repetition
- Efficient information density
- Appropriate length for project size
- No generic filler content

## Pre-Change Protocol Check (MANDATORY)

**This check is CRITICAL.** The Pre-Change Protocol section ensures Claude performs comprehensive dependency analysis before making any code changes, preventing missed references and incomplete updates.

### What to Check

Search CLAUDE.md for:
- Section header containing "Pre-Change" or "Before Any Code Change"
- References to `grep -rn` or impact search
- Checklist with "Files That Will Be Affected"
- Requirement for user verification before proceeding

### If Missing

**Flag as HIGH PRIORITY issue:**

```
1. [HIGH] Missing Pre-Change Protocol section
   CLAUDE.md lacks mandatory dependency-check protocol.
   Impact: Claude may miss file references when making changes,
   leading to broken dependencies and incomplete updates.

   Recommendation: Add Pre-Change Protocol section immediately.
   This is the #1 cause of cascading bugs from incomplete changes.
```

### Required Section Content

The Pre-Change Protocol section must include:
1. Requirement to run grep search and show results
2. List of files that will be affected
3. List of files searched but not changed (with reasoning)
4. Documentation that references the change target
5. User verification checkpoint before proceeding
6. Post-change verification step

## Plugin Integration Analysis

After the content analysis, the command detects and analyzes marketplace plugin integration:

### Detection Method

1. **Read `.claude/settings.local.json`** - Check for enabled MCP servers
2. **Map MCP servers to plugins** - Use marketplace registry to identify active plugins:
   - `gitea` → projman
   - `netbox` → cmdb-assistant
3. **Check for hooks** - Identify hook-based plugins (project-hygiene)
4. **Scan CLAUDE.md** - Look for plugin integration content

### Plugin Coverage Scoring

For each detected plugin, verify CLAUDE.md contains:
- Plugin section header or mention
- Available commands documentation
- MCP tools reference (if applicable)
- Usage guidelines

Coverage is reported as percentage: `(plugins referenced / plugins detected) * 100`

## Expected Output

```
CLAUDE.md Analysis Report
=========================

File: /path/to/project/CLAUDE.md
Lines: 245
Last Modified: 2025-01-18

Overall Score: 72/100

Category Scores:
- Structure:    20/25 (Good)
- Clarity:      18/25 (Good)
- Completeness: 22/25 (Excellent)
- Conciseness:  12/25 (Needs Work)

Strengths:
+ Clear project overview with good context
+ Critical rules prominently displayed
+ Comprehensive coverage of workflows

Issues Found:

1. [HIGH] Verbose explanations (lines 45-78)
   Section "Running Tests" has 34 lines that could be 8 lines.
   Impact: Harder to scan, important info buried

2. [MEDIUM] Duplicate content (lines 102-115, 189-200)
   Same git workflow documented twice.
   Impact: Maintenance burden, inconsistency risk

3. [MEDIUM] Missing Quick Start section
   No clear "how to get started" instructions.
   Impact: Slower onboarding for Claude

4. [LOW] Inconsistent header formatting
   Mix of "## Title" and "## Title:" styles.
   Impact: Minor readability issue

Recommendations:
1. Add Quick Start section at top (priority: high)
2. Condense Testing section to essentials (priority: high)
3. Remove duplicate git workflow (priority: medium)
4. Standardize header formatting (priority: low)

Estimated improvement: 15-20 points after changes

---

Plugin Integration Analysis
===========================

Detected Active Plugins:
  ✓ projman (via gitea MCP server)
  ✓ cmdb-assistant (via netbox MCP server)
  ✓ project-hygiene (via PostToolUse hook)

Plugin Coverage: 33% (1/3 plugins referenced)

  ✓ projman - Referenced in CLAUDE.md
  ✗ cmdb-assistant - NOT referenced
  ✗ project-hygiene - NOT referenced

Missing Integration Content:

1. cmdb-assistant
   Add infrastructure management commands and NetBox MCP tools reference.

2. project-hygiene
   Add cleanup hook documentation and configuration options.

---

Would you like me to:
[1] Implement all content recommendations
[2] Add missing plugin integrations to CLAUDE.md
[3] Do both (recommended)
[4] Show preview of changes first
```

## When to Use

Run `/config-analyze` when:
- Setting up a new project with existing CLAUDE.md
- CLAUDE.md feels too long or hard to use
- Claude seems to miss instructions
- Before major project changes
- Periodic maintenance (quarterly)
- After installing new marketplace plugins
- When Claude doesn't seem to use available plugin tools

## Follow-Up Actions

After analysis, you can:
- Run `/config-optimize` to automatically improve the file
- Manually address specific issues
- Request detailed recommendations for any section
- Compare with best practice templates

## Tips

- Run analysis after significant project changes
- Address HIGH priority issues first
- Keep scores above 70/100 for best results
- Re-analyze after making changes to verify improvement
