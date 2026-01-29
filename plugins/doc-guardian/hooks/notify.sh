#!/bin/bash
# doc-guardian notification hook
# Tracks documentation dependencies and queues updates
#
# SILENT BY DEFAULT - No output to avoid interrupting Claude's workflow.
# Changes are queued to .doc-guardian-queue for later processing.
# Run /doc-sync or /doc-audit to see and process pending updates.
#
# Set DOC_GUARDIAN_VERBOSE=1 to enable notification output.

# Read tool input from stdin (JSON with file_path)
INPUT=$(cat)

# Extract file_path from JSON input
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

# If no file_path found, exit silently
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Define documentation dependency mappings
# When these directories change, these docs need updating
declare -A DOC_DEPS
DOC_DEPS["commands"]="docs/COMMANDS-CHEATSHEET.md README.md"
DOC_DEPS["agents"]="README.md CLAUDE.md"
DOC_DEPS["hooks"]="docs/COMMANDS-CHEATSHEET.md README.md"
DOC_DEPS["skills"]="README.md"
DOC_DEPS[".claude-plugin"]="CLAUDE.md .claude-plugin/marketplace.json"
DOC_DEPS["mcp-servers"]="docs/COMMANDS-CHEATSHEET.md CLAUDE.md"

# Check which config directory was modified
MODIFIED_TYPE=""
for dir in commands agents hooks skills .claude-plugin mcp-servers; do
    if echo "$FILE_PATH" | grep -qE "/${dir}/|^${dir}/"; then
        MODIFIED_TYPE="$dir"
        break
    fi
done

# Exit silently if not a tracked config directory
if [ -z "$MODIFIED_TYPE" ]; then
    exit 0
fi

# Get the dependent docs
DEPENDENT_DOCS="${DOC_DEPS[$MODIFIED_TYPE]}"

# Queue file for tracking pending updates
QUEUE_FILE="${CLAUDE_PROJECT_ROOT:-.}/.doc-guardian-queue"

# Add to queue (always, for deduplication we check file+type combo)
# Format: timestamp | type | file_path | dependent_docs
QUEUE_ENTRY="$(date +%Y-%m-%dT%H:%M:%S) | $MODIFIED_TYPE | $FILE_PATH | $DEPENDENT_DOCS"

# Check if this exact file+type combo already exists in queue (dedup)
if [ -f "$QUEUE_FILE" ]; then
    if grep -qF "| $MODIFIED_TYPE | $FILE_PATH |" "$QUEUE_FILE" 2>/dev/null; then
        # Already queued, skip silently
        exit 0
    fi
fi

# Add to queue
echo "$QUEUE_ENTRY" >> "$QUEUE_FILE" 2>/dev/null || true

# SILENT by default - only output if DOC_GUARDIAN_VERBOSE is set
# This prevents Claude from stopping to ask about documentation updates
if [ "${DOC_GUARDIAN_VERBOSE:-0}" = "1" ]; then
    PENDING_COUNT=$(wc -l < "$QUEUE_FILE" 2>/dev/null | tr -d ' ' || echo "1")
    echo "[doc-guardian] queued: $MODIFIED_TYPE ($PENDING_COUNT pending)"
fi

exit 0
