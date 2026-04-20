#!/bin/bash
# git-guardrails: branch-name validation hook
# Enforces <type>/<description> convention on branch creation.

INPUT=$(cat)

if ! echo "$INPUT" | grep -q '"command".*git'; then
    exit 0
fi

COMMAND=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

if [ -z "$COMMAND" ]; then
    exit 0
fi

IS_BRANCH_CREATE=false
BRANCH_NAME=""

if echo "$COMMAND" | grep -qE 'git\s+checkout\s+(-b|--branch)\s+'; then
    IS_BRANCH_CREATE=true
    BRANCH_NAME=$(echo "$COMMAND" | sed -n 's/.*git\s\+checkout\s\+\(-b\|--branch\)\s\+\([^ ]*\).*/\2/p')
fi

if echo "$COMMAND" | grep -qE 'git\s+switch\s+(-c|-C|--create|--force-create)\s+'; then
    IS_BRANCH_CREATE=true
    BRANCH_NAME=$(echo "$COMMAND" | sed -n 's/.*git\s\+switch\s\+\(-c\|-C\|--create\|--force-create\)\s\+\([^ ]*\).*/\2/p')
fi

if echo "$COMMAND" | grep -qE 'git\s+branch\s+[^-]' && ! echo "$COMMAND" | grep -qE 'git\s+branch\s+(-d|-D|-m|-M|--delete|--move|--list|--show-current)'; then
    IS_BRANCH_CREATE=true
    BRANCH_NAME=$(echo "$COMMAND" | sed -n 's/.*git\s\+branch\s\+\([^ -][^ ]*\).*/\1/p')
fi

if [ "$IS_BRANCH_CREATE" = false ]; then
    exit 0
fi

if [ -z "$BRANCH_NAME" ]; then
    exit 0
fi

BRANCH_NAME=$(echo "$BRANCH_NAME" | tr -d '"' | tr -d "'")

case "$BRANCH_NAME" in
    main|master|develop|development|staging|release|hotfix)
        exit 0
        ;;
esac

# Allow claude/* branches used by Claude Code on the web
if echo "$BRANCH_NAME" | grep -qE '^claude/[a-zA-Z0-9_-]+$'; then
    exit 0
fi

VALID_TYPES="feat|fix|chore|docs|refactor|test|perf|debug"

if ! echo "$BRANCH_NAME" | grep -qE "^($VALID_TYPES)/[a-z0-9][a-z0-9-]*$"; then
    echo ""
    echo "[git-guardrails] Branch name validation failed"
    echo ""
    echo "Branch: $BRANCH_NAME"
    echo ""
    echo "Expected format: <type>/<description>"
    echo ""
    echo "Valid types: feat, fix, chore, docs, refactor, test, perf, debug"
    echo "(claude/* prefix is also allowed for Claude Code web sessions.)"
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
    echo ""
    exit 1
fi

if [ ${#BRANCH_NAME} -gt 50 ]; then
    echo ""
    echo "[git-guardrails] Branch name too long"
    echo ""
    echo "Branch: $BRANCH_NAME (${#BRANCH_NAME} chars)"
    echo "Maximum: 50 characters"
    echo ""
    exit 1
fi

exit 0
