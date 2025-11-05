# Command Metadata Format

Comprehensive guide for command frontmatter in `.md` files.

## Basic Structure

```markdown
---
_type: command
_command: command-name
_description: Brief description of what the command does
_agent: agent-name (optional)
---

# Command content starts here
```

## Required Fields

### _type
- **Value**: Always `"command"`
- **Purpose**: Identifies file as a command

### _command
- **Format**: kebab-case
- **Pattern**: `^[a-z][a-z0-9-]*$`
- **Example**: `deploy-app`, `check-status`

### _description
- **Length**: 10-100 characters
- **Content**: User-facing command description
- **Shows in**: Command autocomplete

## Optional Fields

### _agent
- **Purpose**: Associates command with an agent
- **Value**: Name of agent in `agents/` directory
- **Example**: `_agent: deploy-specialist`

### _alias
- **Purpose**: Alternative command names
- **Format**: String or array
- **Example**: `_alias: ["dp", "deploy-production"]`

### _hidden
- **Purpose**: Hide from command list
- **Value**: `true` or `false`
- **Use case**: Internal/debug commands

### _require_confirmation
- **Purpose**: Prompt user before execution
- **Value**: `true` or `false`
- **Use case**: Destructive operations

### _tags
- **Purpose**: Categorize commands
- **Format**: Array of strings
- **Example**: `_tags: ["deployment", "production"]`

## Command Organization

### Single Commands
```
commands/
└── deploy-app.md
```

### Grouped Commands
```
commands/
├── deploy/
│   ├── staging.md
│   ├── production.md
│   └── rollback.md
├── database/
│   ├── backup.md
│   ├── restore.md
│   └── migrate.md
└── status.md
```

### Subcommand Syntax
- Directory structure creates subcommands
- Example: `/plugin-name deploy staging`
- Parent directory can have `_index.md` for group help

## Complete Examples

### Basic Command
```markdown
---
_type: command
_command: health-check
_description: Check system health status
---

# Health Check

Performs comprehensive system health verification.

## Usage
Run health check: `/deploy-tools health-check`

## Options
- `--verbose`: Detailed output
- `--service <name>`: Check specific service
```

### Command with Agent
```markdown
---
_type: command
_command: deploy-app
_description: Deploy application to cloud
_agent: deployment-specialist
_require_confirmation: true
_tags: ["deployment", "cloud", "production"]
---

# Deploy Application

Deploys application using specialized agent assistance.

## Prerequisites
- Valid AWS credentials
- Docker image built
- Deployment config ready
```

### Hidden Debug Command
```markdown
---
_type: command
_command: debug-manifest
_description: Validate plugin manifest (internal)
_hidden: true
_alias: "dbg-manifest"
---

# Debug Manifest

Internal command for manifest validation.
```

## Variable Interpolation

### Available Variables
- `${CLAUDE_PLUGIN_ROOT}`: Plugin directory path
- `${CLAUDE_WORKSPACE}`: Current workspace
- `${CLAUDE_USER}`: Current username

### Usage Example
```markdown
## Configuration

Load config from: `${CLAUDE_PLUGIN_ROOT}/config.json`
```

## Best Practices

### Naming Conventions
1. Use verb-noun pattern: `create-database`, `update-config`
2. Keep names short but descriptive
3. Avoid abbreviations unless common
4. Use consistent terminology

### Description Guidelines
1. Start with action verb
2. Be specific about what happens
3. Include object of action
4. Avoid technical jargon

Good examples:
- "Deploy application to staging"
- "Create new database backup"
- "Generate API documentation"

Bad examples:
- "Deployment" (not a complete sentence)
- "Does stuff with the app" (too vague)
- "Executes deployment pipeline workflow" (too technical)

### Documentation Structure
1. **Brief description** after frontmatter
2. **Usage** section with examples
3. **Options** if applicable
4. **Prerequisites** for complex commands
5. **Examples** showing real usage

### Error Handling
```markdown
## Troubleshooting

**Error: Missing credentials**
Solution: Run `aws configure` first

**Error: Port already in use**
Solution: Check running services with `lsof -i :3000`
```

## Security Patterns

### Input Validation
```markdown
## Security

This command validates:
- File paths (no directory traversal)
- Environment variables (alphanumeric only)
- URLs (HTTPS required)
```

### Confirmation Prompts
```markdown
---
_require_confirmation: true
---

## Confirmation

You will be prompted to confirm:
- Database deletion
- Production deployment
- Configuration overwrite
```

## Advanced Features

### Conditional Display
```markdown
## Platform-Specific

<!--- platform:macos --->
### macOS Instructions
Use Homebrew: `brew install tool`

<!--- platform:linux --->
### Linux Instructions
Use apt: `sudo apt-get install tool`
```

### Dynamic Content
```markdown
## Current Status

<!-- dynamic:start -->
Status will be inserted here
<!-- dynamic:end -->
```

### Command Chaining
```markdown
## Related Commands

After deployment, you might want to:
- `/deploy-tools check-status`
- `/deploy-tools view-logs`
- `/deploy-tools rollback` (if needed)
```