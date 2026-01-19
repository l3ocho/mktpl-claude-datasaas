---
description: Analyze CLAUDE.md for optimization opportunities
---

# Analyze CLAUDE.md

This command analyzes your project's CLAUDE.md file and provides a detailed report on optimization opportunities.

## What This Command Does

1. **Read CLAUDE.md** - Locates and reads the project's CLAUDE.md file
2. **Analyze Structure** - Evaluates organization, headers, and flow
3. **Check Content** - Reviews clarity, completeness, and conciseness
4. **Identify Issues** - Finds redundancy, verbosity, and missing sections
5. **Generate Report** - Provides scored assessment with recommendations

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

### Conciseness (25 points)
- No unnecessary repetition
- Efficient information density
- Appropriate length for project size
- No generic filler content

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

Would you like me to:
[1] Implement all recommended changes
[2] Show before/after for specific section
[3] Generate optimized version for review
```

## When to Use

Run `/config-analyze` when:
- Setting up a new project with existing CLAUDE.md
- CLAUDE.md feels too long or hard to use
- Claude seems to miss instructions
- Before major project changes
- Periodic maintenance (quarterly)

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
