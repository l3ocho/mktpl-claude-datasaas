#!/bin/bash
# contract-validator breaking change detection hook
# Warns when plugin interface changes might break consumers
# This is a PostToolUse hook - non-blocking, warnings only

PREFIX="[contract-validator]"

# Check if warnings are enabled (default: true)
if [[ "${CONTRACT_VALIDATOR_BREAKING_WARN:-true}" != "true" ]]; then
    exit 0
fi

# Read tool input from stdin
INPUT=$(cat)

# Extract file_path from JSON input
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

# If no file_path found, exit silently
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Check if file is a plugin interface file
is_interface_file() {
    local file="$1"

    case "$file" in
        */plugin.json) return 0 ;;
        */.claude-plugin/plugin.json) return 0 ;;
        */hooks.json) return 0 ;;
        */hooks/hooks.json) return 0 ;;
        */.mcp.json) return 0 ;;
        */agents/*.md) return 0 ;;
        */commands/*.md) return 0 ;;
        */skills/*.md) return 0 ;;
    esac

    return 1
}

# Exit if not an interface file
if ! is_interface_file "$FILE_PATH"; then
    exit 0
fi

# Check if file exists and is in a git repo
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Get the directory containing the file
FILE_DIR=$(dirname "$FILE_PATH")
FILE_NAME=$(basename "$FILE_PATH")

# Try to get the previous version from git
cd "$FILE_DIR" 2>/dev/null || exit 0

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    exit 0
fi

# Get previous version (HEAD version before current changes)
PREV_CONTENT=$(git show HEAD:"$FILE_PATH" 2>/dev/null || echo "")

# If no previous version, this is a new file - no breaking changes possible
if [ -z "$PREV_CONTENT" ]; then
    exit 0
fi

# Read current content
CURR_CONTENT=$(cat "$FILE_PATH" 2>/dev/null || echo "")

if [ -z "$CURR_CONTENT" ]; then
    exit 0
fi

BREAKING_CHANGES=()

# Detect breaking changes based on file type
case "$FILE_PATH" in
    */plugin.json|*/.claude-plugin/plugin.json)
        # Check for removed or renamed fields in plugin.json

        # Check if name changed
        PREV_NAME=$(echo "$PREV_CONTENT" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1)
        CURR_NAME=$(echo "$CURR_CONTENT" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1)
        if [ -n "$PREV_NAME" ] && [ "$PREV_NAME" != "$CURR_NAME" ]; then
            BREAKING_CHANGES+=("Plugin name changed - consumers may need updates")
        fi

        # Check if version had major bump (semantic versioning)
        PREV_VER=$(echo "$PREV_CONTENT" | grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([0-9]*\)\..*/\1/')
        CURR_VER=$(echo "$CURR_CONTENT" | grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([0-9]*\)\..*/\1/')
        if [ -n "$PREV_VER" ] && [ -n "$CURR_VER" ] && [ "$CURR_VER" -gt "$PREV_VER" ] 2>/dev/null; then
            BREAKING_CHANGES+=("Major version bump detected - verify breaking changes documented")
        fi
        ;;

    */hooks.json|*/hooks/hooks.json)
        # Check for removed hook events
        PREV_EVENTS=$(echo "$PREV_CONTENT" | grep -oE '"(PreToolUse|PostToolUse|UserPromptSubmit|SessionStart|SessionEnd|Notification|Stop|SubagentStop|PreCompact)"' | sort -u)
        CURR_EVENTS=$(echo "$CURR_CONTENT" | grep -oE '"(PreToolUse|PostToolUse|UserPromptSubmit|SessionStart|SessionEnd|Notification|Stop|SubagentStop|PreCompact)"' | sort -u)

        # Find removed events
        REMOVED_EVENTS=$(comm -23 <(echo "$PREV_EVENTS") <(echo "$CURR_EVENTS") 2>/dev/null)
        if [ -n "$REMOVED_EVENTS" ]; then
            BREAKING_CHANGES+=("Hook events removed: $(echo $REMOVED_EVENTS | tr '\n' ' ')")
        fi

        # Check for changed matchers
        PREV_MATCHERS=$(echo "$PREV_CONTENT" | grep -o '"matcher"[[:space:]]*:[[:space:]]*"[^"]*"' | sort -u)
        CURR_MATCHERS=$(echo "$CURR_CONTENT" | grep -o '"matcher"[[:space:]]*:[[:space:]]*"[^"]*"' | sort -u)
        if [ "$PREV_MATCHERS" != "$CURR_MATCHERS" ]; then
            BREAKING_CHANGES+=("Hook matchers changed - verify tool coverage")
        fi
        ;;

    */.mcp.json)
        # Check for removed MCP servers
        PREV_SERVERS=$(echo "$PREV_CONTENT" | grep -o '"[^"]*"[[:space:]]*:' | grep -v "mcpServers" | sort -u)
        CURR_SERVERS=$(echo "$CURR_CONTENT" | grep -o '"[^"]*"[[:space:]]*:' | grep -v "mcpServers" | sort -u)

        REMOVED_SERVERS=$(comm -23 <(echo "$PREV_SERVERS") <(echo "$CURR_SERVERS") 2>/dev/null)
        if [ -n "$REMOVED_SERVERS" ]; then
            BREAKING_CHANGES+=("MCP servers removed - tools may be unavailable")
        fi
        ;;

    */agents/*.md)
        # Check if agent file was significantly reduced (might indicate removal of capabilities)
        PREV_LINES=$(echo "$PREV_CONTENT" | wc -l)
        CURR_LINES=$(echo "$CURR_CONTENT" | wc -l)

        # If more than 50% reduction, warn
        if [ "$PREV_LINES" -gt 10 ] && [ "$CURR_LINES" -lt $((PREV_LINES / 2)) ]; then
            BREAKING_CHANGES+=("Agent definition significantly reduced - capabilities may be removed")
        fi

        # Check if agent name/description changed in frontmatter
        PREV_DESC=$(echo "$PREV_CONTENT" | head -20 | grep -i "description" | head -1)
        CURR_DESC=$(echo "$CURR_CONTENT" | head -20 | grep -i "description" | head -1)
        if [ -n "$PREV_DESC" ] && [ "$PREV_DESC" != "$CURR_DESC" ]; then
            BREAKING_CHANGES+=("Agent description changed - verify consumer expectations")
        fi
        ;;

    */commands/*.md|*/skills/*.md)
        # Check if command/skill was significantly changed
        PREV_LINES=$(echo "$PREV_CONTENT" | wc -l)
        CURR_LINES=$(echo "$CURR_CONTENT" | wc -l)

        if [ "$PREV_LINES" -gt 10 ] && [ "$CURR_LINES" -lt $((PREV_LINES / 2)) ]; then
            BREAKING_CHANGES+=("Command/skill significantly reduced - behavior may change")
        fi
        ;;
esac

# Output warnings if any breaking changes detected
if [[ ${#BREAKING_CHANGES[@]} -gt 0 ]]; then
    echo ""
    echo "$PREFIX WARNING: Potential breaking changes in $(basename "$FILE_PATH")"
    echo "$PREFIX ============================================"
    for change in "${BREAKING_CHANGES[@]}"; do
        echo "$PREFIX   - $change"
    done
    echo "$PREFIX ============================================"
    echo "$PREFIX Consider updating CHANGELOG and notifying consumers"
    echo ""
fi

# Always exit 0 - non-blocking
exit 0
