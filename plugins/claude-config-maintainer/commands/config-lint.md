---
description: Lint CLAUDE.md for common anti-patterns and best practices
---

# Lint CLAUDE.md

This command checks your CLAUDE.md file against best practices and detects common anti-patterns that can cause issues with Claude Code.

## Visual Output

When executing this command, display the plugin header:

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚙️ CONFIG-MAINTAINER · CLAUDE.md Lint                           │
└──────────────────────────────────────────────────────────────────┘
```

Then proceed with the linting.

## What This Command Does

1. **Parse Structure** - Validates markdown structure and hierarchy
2. **Check Security** - Detects hardcoded paths, secrets, and sensitive data
3. **Validate Content** - Identifies anti-patterns and problematic instructions
4. **Verify Format** - Ensures consistent formatting and style
5. **Generate Report** - Provides actionable findings with fix suggestions

## Usage

```
/config-lint
```

Lint with auto-fix:

```
/config-lint --fix
```

Check specific rules only:

```
/config-lint --rules=security,structure
```

## Linting Rules

### Security Rules (SEC)

| Rule | Description | Severity |
|------|-------------|----------|
| SEC001 | Hardcoded absolute paths | Warning |
| SEC002 | Potential secrets/API keys | Error |
| SEC003 | Hardcoded IP addresses | Warning |
| SEC004 | Exposed credentials patterns | Error |
| SEC005 | Hardcoded URLs with tokens | Error |
| SEC006 | Environment variable values (not names) | Warning |

### Structure Rules (STR)

| Rule | Description | Severity |
|------|-------------|----------|
| STR001 | Missing required sections | Error |
| STR002 | Invalid header hierarchy (h3 before h2) | Warning |
| STR003 | Orphaned content (text before first header) | Info |
| STR004 | Excessive nesting depth (>4 levels) | Warning |
| STR005 | Empty sections | Warning |
| STR006 | Missing section content | Warning |

### Content Rules (CNT)

| Rule | Description | Severity |
|------|-------------|----------|
| CNT001 | Contradictory instructions | Error |
| CNT002 | Vague or ambiguous rules | Warning |
| CNT003 | Overly long sections (>100 lines) | Info |
| CNT004 | Duplicate content | Warning |
| CNT005 | TODO/FIXME in production config | Warning |
| CNT006 | Outdated version references | Info |
| CNT007 | Broken internal links | Warning |

### Format Rules (FMT)

| Rule | Description | Severity |
|------|-------------|----------|
| FMT001 | Inconsistent header styles | Info |
| FMT002 | Inconsistent list markers | Info |
| FMT003 | Missing code block language | Info |
| FMT004 | Trailing whitespace | Info |
| FMT005 | Missing blank lines around headers | Info |
| FMT006 | Inconsistent indentation | Info |

### Best Practice Rules (BPR)

| Rule | Description | Severity |
|------|-------------|----------|
| BPR001 | No Quick Start section | Warning |
| BPR002 | No Critical Rules section | Warning |
| BPR003 | Instructions without examples | Info |
| BPR004 | Commands without explanation | Info |
| BPR005 | Rules without rationale | Info |
| BPR006 | Missing plugin integration docs | Info |

## Expected Output

```
CLAUDE.md Lint Report
=====================

File: /path/to/project/CLAUDE.md
Rules checked: 25
Time: 0.3s

Summary:
  Errors:   2
  Warnings: 5
  Info:     3

Findings:
---------

[ERROR] SEC002: Potential secret detected (line 45)
  │ api_key = "sk-1234567890abcdef"
  │          ^^^^^^^^^^^^^^^^^^^^^^
  └─ Hardcoded API key found. Use environment variable reference instead.

  Suggested fix:
  - api_key = "sk-1234567890abcdef"
  + api_key = $OPENAI_API_KEY  # Set in environment

[ERROR] CNT001: Contradictory instructions (lines 23, 67)
  │ Line 23: "Always run tests before committing"
  │ Line 67: "Skip tests for documentation-only changes"
  │
  └─ These rules conflict. Clarify the exception explicitly.

  Suggested fix:
  + "Always run tests before committing, except for documentation-only
  +  changes (files in docs/ directory)"

[WARNING] SEC001: Hardcoded absolute path (line 12)
  │ Database location: /home/user/data/myapp.db
  │                    ^^^^^^^^^^^^^^^^^^^^^^^^
  └─ Absolute paths break portability. Use relative or variable.

  Suggested fix:
  - Database location: /home/user/data/myapp.db
  + Database location: ./data/myapp.db  # Or $DATA_DIR/myapp.db

[WARNING] STR002: Invalid header hierarchy (line 34)
  │ ### Subsection
  │ (no preceding ## header)
  │
  └─ H3 header without parent H2. Add H2 or promote to H2.

[WARNING] CNT004: Duplicate content (lines 45-52, 89-96)
  │ Same git workflow documented twice
  │
  └─ Remove duplicate or consolidate into single section.

[WARNING] STR005: Empty section (line 78)
  │ ## Troubleshooting
  │ (no content)
  │
  └─ Add content or remove empty section.

[WARNING] BPR002: No Critical Rules section
  │ Missing "Critical Rules" or "Important Rules" section
  │
  └─ Add a section highlighting must-follow rules for Claude.

[INFO] FMT003: Missing code block language (line 56)
  │ ```
  │ npm install
  │ ```
  │
  └─ Specify language for syntax highlighting: ```bash

[INFO] CNT003: Overly long section (lines 100-215)
  │ "Architecture" section is 115 lines
  │
  └─ Consider breaking into subsections or condensing.

[INFO] FMT001: Inconsistent header styles
  │ Line 10: "## Quick Start"
  │ Line 25: "## Architecture:"
  │           (colon suffix inconsistent)
  │
  └─ Standardize header format throughout document.

---

Auto-fixable: 4 issues (run with --fix)
Manual review required: 6 issues

Run `/config-lint --fix` to apply automatic fixes.
```

## Options

| Option | Description |
|--------|-------------|
| `--fix` | Automatically fix auto-fixable issues |
| `--rules=LIST` | Check only specified rule categories |
| `--ignore=LIST` | Skip specified rules (e.g., `--ignore=FMT001,FMT002`) |
| `--severity=LEVEL` | Show only issues at or above level (error/warning/info) |
| `--format=FORMAT` | Output format: `text` (default), `json`, `sarif` |
| `--config=FILE` | Use custom lint configuration |
| `--strict` | Treat warnings as errors |

## Rule Categories

Use `--rules` to focus on specific areas:

```
/config-lint --rules=security        # Only security checks
/config-lint --rules=structure       # Only structure checks
/config-lint --rules=security,content  # Multiple categories
```

Available categories:
- `security` - SEC rules
- `structure` - STR rules
- `content` - CNT rules
- `format` - FMT rules
- `bestpractice` - BPR rules

## Custom Configuration

Create `.claude-lint.json` in project root:

```json
{
  "rules": {
    "SEC001": "warning",
    "FMT001": "off",
    "CNT003": {
      "severity": "warning",
      "maxLines": 150
    }
  },
  "ignore": [
    "FMT*"
  ],
  "requiredSections": [
    "Quick Start",
    "Critical Rules",
    "Project Overview"
  ]
}
```

## Anti-Pattern Examples

### Hardcoded Secrets (SEC002)
```markdown
# BAD
API_KEY=sk-1234567890abcdef

# GOOD
API_KEY=$OPENAI_API_KEY  # Set via environment
```

### Hardcoded Paths (SEC001)
```markdown
# BAD
Config file: /home/john/projects/myapp/config.yml

# GOOD
Config file: ./config.yml
Config file: $PROJECT_ROOT/config.yml
```

### Contradictory Rules (CNT001)
```markdown
# BAD
- Always use TypeScript
- JavaScript files are acceptable for scripts

# GOOD
- Always use TypeScript for source code
- JavaScript (.js) is acceptable only for config files and scripts
```

### Vague Instructions (CNT002)
```markdown
# BAD
- Be careful with the database

# GOOD
- Never run DELETE without WHERE clause
- Always backup before migrations
```

### Invalid Hierarchy (STR002)
```markdown
# BAD
# Main Title
### Skipped Level

# GOOD
# Main Title
## Section
### Subsection
```

## When to Use

Run `/config-lint` when:
- Before committing CLAUDE.md changes
- During code review for CLAUDE.md modifications
- Setting up CI/CD checks for configuration files
- After major edits to catch introduced issues
- Periodically as maintenance check

## Integration with CI/CD

Add to your CI pipeline:

```yaml
# GitHub Actions example
- name: Lint CLAUDE.md
  run: claude /config-lint --strict --format=sarif > lint-results.sarif

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: lint-results.sarif
```

## Tips

1. **Start with errors** - Fix errors before warnings
2. **Use --fix carefully** - Review auto-fixes before committing
3. **Configure per-project** - Different projects have different needs
4. **Integrate in CI** - Catch issues before they reach main
5. **Review periodically** - Run lint check monthly as maintenance

## Related Commands

| Command | Relationship |
|---------|--------------|
| `/config-analyze` | Deeper content analysis (complements lint) |
| `/config-optimize` | Applies fixes and improvements |
| `/config-diff` | Shows what changed (run lint before commit) |
