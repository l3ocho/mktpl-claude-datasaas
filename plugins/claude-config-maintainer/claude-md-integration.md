## CLAUDE.md Maintenance (claude-config-maintainer)

This project uses the **claude-config-maintainer** plugin to analyze and optimize CLAUDE.md configuration files.

### Available Commands

| Command | Description |
|---------|-------------|
| `/config-analyze` | Analyze CLAUDE.md for optimization opportunities with 100-point scoring |
| `/config-optimize` | Automatically optimize CLAUDE.md structure and content |
| `/config-init` | Initialize a new CLAUDE.md file for a project |

### Scoring System

The analysis uses a 100-point scoring system across four categories:

| Category | Points | What It Measures |
|----------|--------|------------------|
| Structure | 25 | Organization, headers, navigation, grouping |
| Clarity | 25 | Instructions, examples, language, detail level |
| Completeness | 25 | Overview, quick start, critical rules, workflows |
| Conciseness | 25 | Efficiency, no repetition, appropriate length |

### Usage Guidelines

- Run `/config-analyze` periodically to assess CLAUDE.md quality
- Target a score of **70+/100** for effective Claude Code operation
- Address HIGH priority issues first when optimizing
- Use `/config-init` when setting up new projects to start with best practices
- Re-analyze after making changes to verify improvements
