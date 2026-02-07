## Project Cleanup (project-hygiene)

This project uses the **project-hygiene** plugin for file organization and cleanup checks.

### How It Works

Run `/hygiene check` to scan for common project cleanliness issues:

1. **Temp file detection** — finds `*.tmp`, `*.bak`, `*.swp`, `*~` files
2. **Misplaced files** — files outside their expected directories
3. **Empty directories** — directories with no files
4. **Large files** — files exceeding reasonable size thresholds
5. **Debug artifacts** — leftover debug logs, console.log, print statements

### Usage

```
/hygiene check              # Run all checks
/hygiene check --fix        # Auto-fix safe issues (delete temp files, remove empty dirs)
```

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

### Notes

- This was previously a PostToolUse hook (automatic). Since v8.1.0 (Decision #29), it runs manually via `/hygiene check`.
- Add `/hygiene check` as an explicit step in your prompt files where project cleanliness matters.
