# CLAUDE.md Lint Rules

This skill defines all linting rules for validating CLAUDE.md files.

## Rule Categories

### Security Rules (SEC)

| Rule | Description | Severity | Auto-fix |
|------|-------------|----------|----------|
| SEC001 | Hardcoded absolute paths | Warning | Yes |
| SEC002 | Potential secrets/API keys | Error | No |
| SEC003 | Hardcoded IP addresses | Warning | No |
| SEC004 | Exposed credentials patterns | Error | No |
| SEC005 | Hardcoded URLs with tokens | Error | No |
| SEC006 | Environment variable values (not names) | Warning | No |

### Structure Rules (STR)

| Rule | Description | Severity | Auto-fix |
|------|-------------|----------|----------|
| STR001 | Missing required sections | Error | Yes |
| STR002 | Invalid header hierarchy (h3 before h2) | Warning | Yes |
| STR003 | Orphaned content before first header | Info | No |
| STR004 | Excessive nesting depth (>4 levels) | Warning | No |
| STR005 | Empty sections | Warning | Yes |
| STR006 | Missing section content | Warning | No |

### Content Rules (CNT)

| Rule | Description | Severity | Auto-fix |
|------|-------------|----------|----------|
| CNT001 | Contradictory instructions | Error | No |
| CNT002 | Vague or ambiguous rules | Warning | No |
| CNT003 | Overly long sections (>100 lines) | Info | No |
| CNT004 | Duplicate content | Warning | No |
| CNT005 | TODO/FIXME in production config | Warning | No |
| CNT006 | Outdated version references | Info | No |
| CNT007 | Broken internal links | Warning | No |

### Format Rules (FMT)

| Rule | Description | Severity | Auto-fix |
|------|-------------|----------|----------|
| FMT001 | Inconsistent header styles | Info | Yes |
| FMT002 | Inconsistent list markers | Info | Yes |
| FMT003 | Missing code block language | Info | Yes |
| FMT004 | Trailing whitespace | Info | Yes |
| FMT005 | Missing blank lines around headers | Info | Yes |
| FMT006 | Inconsistent indentation | Info | Yes |

### Best Practice Rules (BPR)

| Rule | Description | Severity | Auto-fix |
|------|-------------|----------|----------|
| BPR001 | No Quick Start section | Warning | No |
| BPR002 | No Critical Rules section | Warning | No |
| BPR003 | Instructions without examples | Info | No |
| BPR004 | Commands without explanation | Info | No |
| BPR005 | Rules without rationale | Info | No |
| BPR006 | Missing plugin integration docs | Info | No |

## Anti-Pattern Examples

### SEC002: Hardcoded Secrets
```markdown
# BAD
API_KEY=sk-1234567890abcdef

# GOOD
API_KEY=$OPENAI_API_KEY  # Set via environment
```

### SEC001: Hardcoded Paths
```markdown
# BAD
Config file: /home/john/projects/myapp/config.yml

# GOOD
Config file: ./config.yml
Config file: $PROJECT_ROOT/config.yml
```

### CNT001: Contradictory Rules
```markdown
# BAD
- Always use TypeScript
- JavaScript files are acceptable for scripts

# GOOD
- Always use TypeScript for source code
- JavaScript (.js) is acceptable only for config files and scripts
```

### CNT002: Vague Instructions
```markdown
# BAD
- Be careful with the database

# GOOD
- Never run DELETE without WHERE clause
- Always backup before migrations
```

### STR002: Invalid Hierarchy
```markdown
# BAD
# Main Title
### Skipped Level

# GOOD
# Main Title
## Section
### Subsection
```

## Output Format

```
[SEVERITY] RULE_ID: Description (line N)
  | Context line showing issue
  |          ^^^^^^ indicator
  +-- Explanation of problem

  Suggested fix:
  - old line
  + new line
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| Error | Must fix | Blocks commit |
| Warning | Should fix | Review recommended |
| Info | Consider fixing | Optional improvement |
