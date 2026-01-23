#!/bin/bash
# doc-guardian notification hook
# Outputs a single notification for config file changes, nothing otherwise
# This is a command hook - guaranteed not to block workflow

# Read tool input from stdin (JSON with file_path)
INPUT=$(cat)

# Extract file_path from JSON input
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

# If no file_path found, exit silently
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Check if file is in a config directory (commands/, agents/, skills/, hooks/)
if echo "$FILE_PATH" | grep -qE '/(commands|agents|skills|hooks)/'; then
    echo "[doc-guardian] Config file modified. Run /doc-sync when ready."
fi

# Exit silently for all other files (no output = no blocking)
exit 0
