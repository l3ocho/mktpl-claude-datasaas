#!/bin/bash
# git-flow commit message validation hook
# Validates git commit messages follow conventional commit format
# PreToolUse hook for Bash commands - type: command

# Read tool input from stdin
INPUT=$(cat)

# Use Python to properly parse JSON and extract the command
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null)

# If no command or python failed, allow through
if [ -z "$COMMAND" ]; then
    exit 0
fi

# Check if it is a git commit command with -m flag
if ! echo "$COMMAND" | grep -qE 'git\s+commit.*-m'; then
    # Not a git commit with -m, allow through
    exit 0
fi

# Extract commit message - handle various quoting styles
# Try double quotes first
COMMIT_MSG=$(echo "$COMMAND" | sed -n 's/.*-m[[:space:]]*"\([^"]*\)".*/\1/p')
# If empty, try single quotes
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG=$(echo "$COMMAND" | sed -n "s/.*-m[[:space:]]*'\\([^']*\\)'.*/\\1/p")
fi
# If still empty, try HEREDOC pattern
if [ -z "$COMMIT_MSG" ]; then
    if echo "$COMMAND" | grep -qE -- '-m[[:space:]]+"\$\(cat <<'; then
        # HEREDOC pattern - too complex to parse, allow through
        exit 0
    fi
fi

# If no message extracted, allow through
if [ -z "$COMMIT_MSG" ]; then
    exit 0
fi

# Validate conventional commit format
# Format: <type>(<scope>): <description>
# or: <type>: <description>
# Valid types: feat, fix, docs, style, refactor, perf, test, chore, build, ci

VALID_TYPES="feat|fix|docs|style|refactor|perf|test|chore|build|ci"

# Check if message matches conventional commit format
if echo "$COMMIT_MSG" | grep -qE "^($VALID_TYPES)(\([a-zA-Z0-9_-]+\))?:[[:space:]]+.+"; then
    # Valid format
    exit 0
fi

# Invalid format - output warning
echo "[git-flow] WARNING: Commit message does not follow conventional commit format"
echo ""
echo "Expected format: <type>(<scope>): <description>"
echo "  or: <type>: <description>"
echo ""
echo "Valid types: feat, fix, docs, style, refactor, perf, test, chore, build, ci"
echo ""
echo "Examples:"
echo "  feat(auth): add password reset functionality"
echo "  fix: resolve login timeout issue"
echo "  docs(readme): update installation instructions"
echo ""
echo "Your message: $COMMIT_MSG"
echo ""
echo "To proceed anyway, use /commit command which auto-generates valid messages."

# Exit with non-zero to block
exit 1
