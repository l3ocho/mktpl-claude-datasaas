#!/bin/bash
# project-hygiene cleanup hook
# Runs after file edits to clean up temp files
# All output MUST have [project-hygiene] prefix

set -euo pipefail

PREFIX="[project-hygiene]"

# Read tool input from stdin (discard - we don't need it for cleanup)
cat > /dev/null

PROJECT_ROOT="${PROJECT_ROOT:-.}"
DELETED_COUNT=0

# Silently delete temp files
for pattern in "*.tmp" "*.bak" "*.swp" "*~" ".DS_Store"; do
    while IFS= read -r -d '' file; do
        rm -f "$file" 2>/dev/null && ((DELETED_COUNT++)) || true
    done < <(find "$PROJECT_ROOT" -name "$pattern" -type f -print0 2>/dev/null || true)
done

# Only output if we deleted something
if [[ $DELETED_COUNT -gt 0 ]]; then
    echo "$PREFIX Cleaned $DELETED_COUNT temp files"
fi

exit 0
