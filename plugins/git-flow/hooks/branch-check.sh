#!/bin/bash
# git-flow branch name validation hook
# Validates branch names follow the convention: <type>/<description>
# Command hook - guaranteed predictable behavior

# Read tool input from stdin (JSON format)
INPUT=$(cat)

# Quick check - exit immediately if not a git command
if ! echo "$INPUT" | grep -q '"command".*git'; then
    exit 0
fi

# Extract command from JSON input
# The Bash tool sends {"command": "..."} format
COMMAND=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

# If no command found, exit silently (allow)
if [ -z "$COMMAND" ]; then
    exit 0
fi

# Check if this is a branch creation command
# Patterns: git checkout -b, git branch (without -d/-D), git switch -c/-C
IS_BRANCH_CREATE=false
BRANCH_NAME=""

# git checkout -b <branch>
if echo "$COMMAND" | grep -qE 'git\s+checkout\s+(-b|--branch)\s+'; then
    IS_BRANCH_CREATE=true
    BRANCH_NAME=$(echo "$COMMAND" | sed -n 's/.*git\s\+checkout\s\+\(-b\|--branch\)\s\+\([^ ]*\).*/\2/p')
fi

# git switch -c/-C <branch>
if echo "$COMMAND" | grep -qE 'git\s+switch\s+(-c|-C|--create|--force-create)\s+'; then
    IS_BRANCH_CREATE=true
    BRANCH_NAME=$(echo "$COMMAND" | sed -n 's/.*git\s\+switch\s\+\(-c\|-C\|--create\|--force-create\)\s\+\([^ ]*\).*/\2/p')
fi

# git branch <name> (without -d/-D/-m/-M which are delete/rename)
if echo "$COMMAND" | grep -qE 'git\s+branch\s+[^-]' && ! echo "$COMMAND" | grep -qE 'git\s+branch\s+(-d|-D|-m|-M|--delete|--move|--list|--show-current)'; then
    IS_BRANCH_CREATE=true
    BRANCH_NAME=$(echo "$COMMAND" | sed -n 's/.*git\s\+branch\s\+\([^ -][^ ]*\).*/\1/p')
fi

# If not a branch creation command, exit silently (allow)
if [ "$IS_BRANCH_CREATE" = false ]; then
    exit 0
fi

# If we couldn't extract the branch name, exit silently (allow)
if [ -z "$BRANCH_NAME" ]; then
    exit 0
fi

# Remove any quotes from branch name
BRANCH_NAME=$(echo "$BRANCH_NAME" | tr -d '"' | tr -d "'")

# Skip validation for special branches
case "$BRANCH_NAME" in
    main|master|develop|development|staging|release|hotfix)
        exit 0
        ;;
esac

# Allowed branch types
VALID_TYPES="feat|fix|chore|docs|refactor|test|perf|debug"

# Validate branch name format: <type>/<description>
# Description: lowercase letters, numbers, hyphens only, max 50 chars total
if ! echo "$BRANCH_NAME" | grep -qE "^($VALID_TYPES)/[a-z0-9][a-z0-9-]*$"; then
    echo ""
    echo "[git-flow] Branch name validation failed"
    echo ""
    echo "Branch: $BRANCH_NAME"
    echo ""
    echo "Expected format: <type>/<description>"
    echo ""
    echo "Valid types: feat, fix, chore, docs, refactor, test, perf, debug"
    echo ""
    echo "Description rules:"
    echo "  - Lowercase letters, numbers, and hyphens only"
    echo "  - Must start with letter or number"
    echo "  - No spaces or special characters"
    echo ""
    echo "Examples:"
    echo "  feat/add-user-auth"
    echo "  fix/login-timeout"
    echo "  chore/update-deps"
    echo "  docs/api-reference"
    echo ""
    exit 1
fi

# Check total length (max 50 chars)
if [ ${#BRANCH_NAME} -gt 50 ]; then
    echo ""
    echo "[git-flow] Branch name too long"
    echo ""
    echo "Branch: $BRANCH_NAME (${#BRANCH_NAME} chars)"
    echo "Maximum: 50 characters"
    echo ""
    exit 1
fi

# Valid branch name
exit 0
