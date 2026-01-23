#!/bin/bash
# code-sentinel security check hook
# Checks for obvious security issues in code files, skips config/docs
# Command hook - guaranteed predictable behavior

# Read tool input from stdin
INPUT=$(cat)

# Extract file_path from JSON input
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

# If no file_path, exit silently
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# SKIP config/doc files entirely - exit silently
case "$FILE_PATH" in
    *.md|*.json|*.yml|*.yaml|*.txt|*.toml|*.ini|*.cfg|*.conf)
        exit 0
        ;;
    */docs/*|*/README*|*/CHANGELOG*|*/LICENSE*)
        exit 0
        ;;
    */.claude/*|*/.github/*|*/.vscode/*)
        exit 0
        ;;
esac

# For code files, extract content to check
# For Edit tool: check new_string
# For Write tool: check content
CONTENT=$(echo "$INPUT" | grep -o '"new_string"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"new_string"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
if [ -z "$CONTENT" ]; then
    CONTENT=$(echo "$INPUT" | grep -o '"content"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"content"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
fi

# If no content to check, exit silently
if [ -z "$CONTENT" ]; then
    exit 0
fi

# Check for hardcoded secrets patterns (obvious cases only)
if echo "$CONTENT" | grep -qiE '(api[_-]?key|api[_-]?secret|password|passwd|secret[_-]?key|auth[_-]?token)[[:space:]]*[=:][[:space:]]*["\x27][A-Za-z0-9+/=_-]{20,}["\x27]'; then
    echo "[code-sentinel] BLOCKED: Hardcoded secret detected"
    exit 1
fi

# Check for AWS keys pattern
if echo "$CONTENT" | grep -qE 'AKIA[A-Z0-9]{16}'; then
    echo "[code-sentinel] BLOCKED: AWS access key detected"
    exit 1
fi

# Check for private key headers
if echo "$CONTENT" | grep -qE '\-\-\-\-\-BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY\-\-\-\-\-'; then
    echo "[code-sentinel] BLOCKED: Private key detected"
    exit 1
fi

# All other cases: exit silently (allow the edit)
exit 0
