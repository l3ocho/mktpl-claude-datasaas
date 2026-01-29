#!/bin/bash
# doc-guardian notification hook
# Tracks documentation dependencies and queues updates
# This is a command hook - guaranteed not to block workflow
#
# IMPORTANT: Output is purely informational - uses passive language
# to avoid triggering Claude to seek user confirmation.
# Run /doc-sync to process the queue when ready.

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

# Debounce: skip notification if same type was logged in last 5 seconds
# This prevents 4+ rapid notifications during batch edits
DEBOUNCE_SECONDS=5
if [ -f "$QUEUE_FILE" ]; then
    LAST_ENTRY=$(tail -1 "$QUEUE_FILE" 2>/dev/null || true)
    LAST_TYPE=$(echo "$LAST_ENTRY" | cut -d'|' -f2 | tr -d ' ')
    LAST_TIME=$(echo "$LAST_ENTRY" | cut -d'|' -f1 | tr -d ' ')

    if [ "$LAST_TYPE" = "$MODIFIED_TYPE" ] && [ -n "$LAST_TIME" ]; then
        # Convert timestamps to seconds for comparison
        LAST_EPOCH=$(date -d "$LAST_TIME" +%s 2>/dev/null || echo "0")
        NOW_EPOCH=$(date +%s)
        DIFF=$((NOW_EPOCH - LAST_EPOCH))

        if [ "$DIFF" -lt "$DEBOUNCE_SECONDS" ]; then
            # Still add to queue, but skip notification
            {
                echo "$(date +%Y-%m-%dT%H:%M:%S) | $MODIFIED_TYPE | $FILE_PATH | $DEPENDENT_DOCS"
            } >> "$QUEUE_FILE" 2>/dev/null || true
            exit 0
        fi
    fi
fi

# Add to queue (create if doesn't exist, append if does)
{
    echo "$(date +%Y-%m-%dT%H:%M:%S) | $MODIFIED_TYPE | $FILE_PATH | $DEPENDENT_DOCS"
} >> "$QUEUE_FILE" 2>/dev/null || true

# Count pending updates
PENDING_COUNT=$(wc -l < "$QUEUE_FILE" 2>/dev/null | tr -d ' ' || echo "1")

# Output passive notification (no action implied)
# Uses "queued" instead of "update needed" to avoid triggering Claude to ask about it
echo "[doc-guardian] drift queued: $MODIFIED_TYPE → $DEPENDENT_DOCS ($PENDING_COUNT total)"

exit 0
