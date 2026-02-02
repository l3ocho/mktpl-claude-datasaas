## CLAUDE.md Maintenance (claude-config-maintainer)

This project uses the **claude-config-maintainer** plugin to analyze and optimize CLAUDE.md and settings.local.json configuration files.

### Available Commands

| Command | Description |
|---------|-------------|
| `/config-analyze` | Analyze CLAUDE.md for optimization opportunities with 100-point scoring |
| `/config-optimize` | Automatically optimize CLAUDE.md structure and content |
| `/config-init` | Initialize a new CLAUDE.md file for a project |
| `/config-diff` | Track CLAUDE.md changes over time with behavioral impact analysis |
| `/config-lint` | Lint CLAUDE.md for anti-patterns and best practices (31 rules) |
| `/config-audit-settings` | Audit settings.local.json permissions with 100-point scoring |
| `/config-optimize-settings` | Optimize permission patterns and apply named profiles |
| `/config-permissions-map` | Visual map of review layers and permission coverage |

### CLAUDE.md Scoring System

The analysis uses a 100-point scoring system across four categories:

| Category | Points | What It Measures |
|----------|--------|------------------|
| Structure | 25 | Organization, headers, navigation, grouping |
| Clarity | 25 | Instructions, examples, language, detail level |
| Completeness | 25 | Overview, quick start, critical rules, workflows |
| Conciseness | 25 | Efficiency, no repetition, appropriate length |

### Settings Scoring System

The settings audit uses a 100-point scoring system across four categories:

| Category | Points | What It Measures |
|----------|--------|------------------|
| Redundancy | 25 | No duplicates, no subset patterns, efficient rules |
| Coverage | 25 | Common tools allowed, MCP servers covered |
| Safety Alignment | 25 | Deny rules for secrets/destructive ops, review layers verified |
| Profile Fit | 25 | Alignment with recommended profile for review layer count |

### Permission Profiles

| Profile | Use Case |
|---------|----------|
| `conservative` | New users, minimal auto-allow, prompts for most writes |
| `reviewed` | Projects with 2+ review layers (code-sentinel, doc-guardian, PR review) |
| `autonomous` | Trusted CI/sandboxed environments only |

### Usage Guidelines

- Run `/config-analyze` periodically to assess CLAUDE.md quality
- Run `/config-audit-settings` to check permission efficiency
- Target a score of **70+/100** for effective Claude Code operation
- Address HIGH priority issues first when optimizing
- Use `/config-init` when setting up new projects to start with best practices
- Use `/config-permissions-map` to visualize review layer coverage
- Re-analyze after making changes to verify improvements
