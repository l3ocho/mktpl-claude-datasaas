#!/bin/bash
# git-guardrails: commit-message validation hook
# Enforces Conventional Commits format on `git commit -m`.

INPUT=$(cat)

if ! echo "$INPUT" | grep -q '"command".*git.*commit'; then
    exit 0
fi

COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null)

if [ -z "$COMMAND" ]; then
    exit 0
fi

if ! echo "$COMMAND" | grep -qE 'git\s+commit.*-m'; then
    exit 0
fi

COMMIT_MSG=$(echo "$COMMAND" | sed -n 's/.*-m[[:space:]]*"\([^"]*\)".*/\1/p')
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG=$(echo "$COMMAND" | sed -n "s/.*-m[[:space:]]*'\\([^']*\\)'.*/\\1/p")
fi
if [ -z "$COMMIT_MSG" ]; then
    if echo "$COMMAND" | grep -qE -- '-m[[:space:]]+"\$\(cat <<'; then
        # HEREDOC — too complex to parse here; allow through.
        exit 0
    fi
fi

if [ -z "$COMMIT_MSG" ]; then
    exit 0
fi

VALID_TYPES="feat|fix|docs|style|refactor|perf|test|chore|build|ci"

if echo "$COMMIT_MSG" | grep -qE "^($VALID_TYPES)(\([a-zA-Z0-9_-]+\))?!?:[[:space:]]+.+"; then
    exit 0
fi

echo "[git-guardrails] WARNING: Commit message does not follow Conventional Commits"
echo ""
echo "Expected format: <type>(<scope>): <description>"
echo "  or:            <type>: <description>"
echo "  breaking:      <type>!: <description>"
echo ""
echo "Valid types: feat, fix, docs, style, refactor, perf, test, chore, build, ci"
echo ""
echo "Examples:"
echo "  feat(auth): add password reset"
echo "  fix: resolve login timeout"
echo "  docs(readme): update install steps"
echo "  feat!: drop support for node 16"
echo ""
echo "Your message: $COMMIT_MSG"
echo ""

exit 1
