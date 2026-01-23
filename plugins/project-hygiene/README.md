# project-hygiene

Post-task cleanup hook plugin for Claude Code. Automatically cleans up temporary files, warns about unexpected files in the project root, and manages orphaned supporting files after task completion.

## Features

- **Delete temp files**: Removes `*.tmp`, `*.bak`, `__pycache__`, `.pytest_cache`, and other common temporary patterns
- **Root file warnings**: Alerts when unexpected files appear in project root
- **Orphan detection**: Identifies `test_*`, `debug_*`, `*_backup.*` and similar files that may have been left behind
- **Cleanup logging**: Records all actions to `.dev/logs/`
- **Configurable**: Project-local `.hygiene.json` for custom rules

## Installation

Add to your Claude Code configuration or install from the marketplace:

```bash
claude plugin install project-hygiene
```

## How It Works

The plugin registers a `PostToolUse` hook (on Write and Edit tools) that runs after Claude modifies files. It:

1. Scans for and deletes known temporary file patterns
2. Removes temporary directories (`__pycache__`, `.pytest_cache`, etc.)
3. Checks for unexpected files in project root and warns
4. Identifies orphaned supporting files (test files, debug scripts, backups)
5. Optionally moves orphans to `.dev/scratch/` for review
6. Logs all actions to `.dev/logs/hygiene-TIMESTAMP.log`

## Configuration

Create `.hygiene.json` in your project root to customize behavior:

```json
{
  "move_orphans": true,
  "allowed_root_files": [
    "custom-config.yaml",
    "my-script.sh"
  ],
  "temp_patterns": [
    "*.cache",
    "*.pid"
  ],
  "ignore_patterns": [
    "important_test_*.py",
    "keep_this_backup.*"
  ]
}
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `move_orphans` | boolean | `false` | Move orphaned files to `.dev/scratch/` instead of just warning |
| `allowed_root_files` | array | (see below) | Additional files allowed in project root |
| `temp_patterns` | array | `[]` | Additional temp file patterns to delete |
| `ignore_patterns` | array | `[]` | Files to never touch during cleanup |

### Default Allowed Root Files

The plugin recognizes common project files in root:
- Git files: `.git`, `.gitignore`, `.gitattributes`
- Config: `.editorconfig`, `.env*`, `.nvmrc`, etc.
- Documentation: `README.md`, `LICENSE`, `CHANGELOG.md`, `CLAUDE.md`
- Package managers: `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, etc.
- Build configs: `Makefile`, `Dockerfile`, `docker-compose.yml`, `tsconfig.json`, etc.

### Default Temp Patterns

Automatically cleaned:
- `*.tmp`, `*.bak`, `*.swp`, `*.swo`, `*~`
- `.DS_Store`, `Thumbs.db`
- `*.log`, `*.orig`, `*.pyc`, `*.pyo`

### Default Temp Directories

Automatically removed:
- `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`
- `node_modules/.cache`, `.next/cache`, `.nuxt/.cache`, `.turbo`
- `*.egg-info`, `.eggs`

### Orphan Patterns

Files flagged as orphans:
- `test_*.py` (standalone test files)
- `debug_*` (debug scripts)
- `*_backup.*`, `*_old.*`, `*_bak.*`, `*.backup`
- `temp_*`, `tmp_*`

## Output

After each task, you'll see output like:

```
[14:32:15] Starting project hygiene cleanup...

[14:32:15] Cleaning temp files...
[14:32:15]   DELETED: ./src/__pycache__/utils.cpython-311.pyc
[14:32:15]   DELETED: ./temp.bak

[14:32:15] Cleaning temp directories...
[14:32:15]   DELETED DIR: ./src/__pycache__

[14:32:15] Checking root files...
[14:32:15]   WARNING: Unexpected root file: random_notes.txt

[14:32:15] Checking for orphaned files...
[14:32:15]   ORPHAN: ./test_scratch.py
[14:32:15]   ORPHAN: ./debug_api.py

=== Cleanup Summary ===
  Deleted: 3 items
  Warnings: 1 unexpected root files
  Orphans: 2 files
  Log file: .dev/logs/hygiene-20250110-143215.log
```

## Directory Structure

```
.dev/
├── logs/
│   └── hygiene-YYYYMMDD-HHMMSS.log
└── scratch/        # (if move_orphans enabled)
    └── debug_api.py
```

## Requirements

- Bash 4.0+
- Optional: `jq` for JSON config parsing (falls back to defaults if not installed)
