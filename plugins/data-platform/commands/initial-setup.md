# /initial-setup - Data Platform Setup Wizard

## Skills to Load
- skills/setup-workflow.md
- skills/visual-header.md

## Visual Output

Display header: `DATA-PLATFORM - Setup Wizard`

## Usage

```
/initial-setup
```

## Workflow

Execute `skills/setup-workflow.md` phases in order:

### Phase 1: Environment Validation
- Check Python 3.10+ installed
- Stop if version too old

### Phase 2: MCP Server Setup
- Locate MCP server (installed or source path)
- Check/create virtual environment
- Install dependencies if needed

### Phase 3: PostgreSQL Configuration (Optional)
- Ask user if they want PostgreSQL access
- If yes: create `~/.config/claude/postgres.env`
- Test connection and report status

### Phase 4: dbt Configuration (Optional)
- Ask user if they use dbt
- If yes: explain auto-detection via `dbt_project.yml`
- Check dbt CLI installation

### Phase 5: Validation
- Verify MCP server can be imported
- Display summary with component status
- Inform user to restart session

## Important Notes

- Uses Bash, Read, Write, AskUserQuestion tools (NOT MCP tools)
- MCP tools unavailable until session restart
- PostgreSQL and dbt are optional - pandas works without them
