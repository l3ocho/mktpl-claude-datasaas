## Project Cleanup (project-hygiene)

This project uses the **project-hygiene** plugin for automated post-task cleanup.

### How It Works

The plugin automatically runs after file Write or Edit operations to:

1. **Delete temporary files** - Removes `*.tmp`, `*.bak`, `__pycache__/`, `.pytest_cache/`, etc.
2. **Warn about unexpected root files** - Alerts when files are created outside expected locations
3. **Identify orphaned files** - Detects supporting files that may no longer be needed

### Configuration

The plugin can be configured via `.hygiene.json` in the project root:

```json
{
  "temp_patterns": ["*.tmp", "*.bak", "*.swp"],
  "ignore_dirs": ["node_modules", ".git", ".venv"],
  "allowed_root_files": ["CLAUDE.md", "README.md", "LICENSE"],
  "warn_on_root_files": true
}
```

### Hook Events

The plugin registers on the following events:
- `PostToolUse` (matcher: `Write|Edit`) - Runs cleanup after file modifications

### Usage Guidelines

- Let the hook run automatically - no manual intervention needed
- Review warnings about unexpected root files
- Configure `.hygiene.json` to customize cleanup behavior for your project
- Check cleanup output if files seem to disappear unexpectedly
