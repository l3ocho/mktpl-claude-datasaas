# Claude Config Maintainer

A Claude Code plugin for creating and maintaining optimized CLAUDE.md configuration files.

## Overview

CLAUDE.md files provide instructions to Claude Code when working with a project. This plugin helps you:

- **Analyze** existing CLAUDE.md files for improvement opportunities
- **Optimize** structure, clarity, and conciseness
- **Initialize** new CLAUDE.md files with project-specific content

## Installation

This plugin is part of the Leo Claude Marketplace. Install the marketplace and the plugin will be available.

## Commands

### `/config-analyze`
Analyze your CLAUDE.md and get a detailed report with scores and recommendations.

```
/config-analyze
```

### `/config-optimize`
Automatically optimize your CLAUDE.md based on best practices.

```
/config-optimize
```

### `/config-init`
Create a new CLAUDE.md tailored to your project.

```
/config-init
```

## Best Practices

A good CLAUDE.md should be:

- **Clear** - Easy to understand at a glance
- **Concise** - No unnecessary content
- **Complete** - All essential information included
- **Current** - Up to date with the project

### Recommended Structure

```markdown
# CLAUDE.md

## Project Overview
What does this project do?

## Quick Start
Essential build/test/run commands.

## Critical Rules
What must Claude NEVER do?

## Architecture (optional)
Key technical decisions.

## Common Operations (optional)
Frequent tasks and workflows.
```

### Length Guidelines

| Project Size | Recommended Lines |
|-------------|------------------|
| Small | 50-100 |
| Medium | 100-200 |
| Large | 200-400 |

## Scoring System

The analyzer scores CLAUDE.md files on:

- **Structure** (25 pts) - Organization and navigation
- **Clarity** (25 pts) - Clear, unambiguous instructions
- **Completeness** (25 pts) - Essential sections present
- **Conciseness** (25 pts) - Efficient information density

Target score: **70+** for effective Claude Code usage.

## Tips

1. Run `/config-analyze` periodically to maintain quality
2. Update CLAUDE.md when adding major features
3. Keep critical rules prominent and clear
4. Include examples where they add clarity
5. Remove generic advice that applies to all projects

## Contributing

This plugin is part of the personal-projects/leo-claude-mktplace repository.
