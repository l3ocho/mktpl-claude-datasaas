#!/bin/bash
# data-platform schema diff detection hook
# Warns about potentially breaking schema changes
# This is a command hook - non-blocking, warnings only

PREFIX="[data-platform]"

# Check if warnings are enabled (default: true)
if [[ "${DATA_PLATFORM_SCHEMA_WARN:-true}" != "true" ]]; then
    exit 0
fi

# Read tool input from stdin (JSON with file_path)
INPUT=$(cat)

# Extract file_path from JSON input
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')

# If no file_path found, exit silently
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Check if file is a schema-related file
is_schema_file() {
    local file="$1"

    # Check file extension
    case "$file" in
        *.sql) return 0 ;;
        */migrations/*.py) return 0 ;;
        */migrations/*.sql) return 0 ;;
        */models/*.py) return 0 ;;
        */models/*.sql) return 0 ;;
        *schema.prisma) return 0 ;;
        *schema.graphql) return 0 ;;
        */dbt/models/*.sql) return 0 ;;
        */dbt/models/*.yml) return 0 ;;
        */alembic/versions/*.py) return 0 ;;
    esac

    # Check directory patterns
    if echo "$file" | grep -qE "(migrations?|schemas?|models)/"; then
        return 0
    fi

    return 1
}

# Exit if not a schema file
if ! is_schema_file "$FILE_PATH"; then
    exit 0
fi

# Read the file content (if it exists and is readable)
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

FILE_CONTENT=$(cat "$FILE_PATH" 2>/dev/null || echo "")

if [[ -z "$FILE_CONTENT" ]]; then
    exit 0
fi

# Detect breaking changes
BREAKING_CHANGES=()

# Check for DROP COLUMN
if echo "$FILE_CONTENT" | grep -qiE "DROP[[:space:]]+COLUMN"; then
    BREAKING_CHANGES+=("DROP COLUMN detected - may break existing queries")
fi

# Check for DROP TABLE
if echo "$FILE_CONTENT" | grep -qiE "DROP[[:space:]]+TABLE"; then
    BREAKING_CHANGES+=("DROP TABLE detected - data loss risk")
fi

# Check for DROP INDEX
if echo "$FILE_CONTENT" | grep -qiE "DROP[[:space:]]+INDEX"; then
    BREAKING_CHANGES+=("DROP INDEX detected - may impact query performance")
fi

# Check for ALTER TYPE / MODIFY COLUMN type changes
if echo "$FILE_CONTENT" | grep -qiE "ALTER[[:space:]]+.*(TYPE|COLUMN.*TYPE)"; then
    BREAKING_CHANGES+=("Column type change detected - may cause data truncation")
fi

if echo "$FILE_CONTENT" | grep -qiE "MODIFY[[:space:]]+COLUMN"; then
    BREAKING_CHANGES+=("MODIFY COLUMN detected - verify data compatibility")
fi

# Check for adding NOT NULL to existing column
if echo "$FILE_CONTENT" | grep -qiE "ALTER[[:space:]]+.*SET[[:space:]]+NOT[[:space:]]+NULL"; then
    BREAKING_CHANGES+=("Adding NOT NULL constraint - existing NULL values will fail")
fi

if echo "$FILE_CONTENT" | grep -qiE "ADD[[:space:]]+.*NOT[[:space:]]+NULL[^[:space:]]*[[:space:]]+DEFAULT"; then
    # Adding NOT NULL with DEFAULT is usually safe - don't warn
    :
elif echo "$FILE_CONTENT" | grep -qiE "ADD[[:space:]]+.*NOT[[:space:]]+NULL"; then
    BREAKING_CHANGES+=("Adding NOT NULL column without DEFAULT - INSERT may fail")
fi

# Check for RENAME TABLE/COLUMN
if echo "$FILE_CONTENT" | grep -qiE "RENAME[[:space:]]+(TABLE|COLUMN|TO)"; then
    BREAKING_CHANGES+=("RENAME detected - update all references")
fi

# Check for removing from Django/SQLAlchemy models (Python files)
if [[ "$FILE_PATH" == *.py ]]; then
    if echo "$FILE_CONTENT" | grep -qE "^-[[:space:]]*[a-z_]+[[:space:]]*=.*Field\("; then
        BREAKING_CHANGES+=("Model field removal detected in Python ORM")
    fi
fi

# Check for Prisma schema changes
if [[ "$FILE_PATH" == *schema.prisma ]]; then
    if echo "$FILE_CONTENT" | grep -qE "@relation.*onDelete.*Cascade"; then
        BREAKING_CHANGES+=("Cascade delete detected - verify data safety")
    fi
fi

# Output warnings if any breaking changes detected
if [[ ${#BREAKING_CHANGES[@]} -gt 0 ]]; then
    echo ""
    echo "$PREFIX WARNING: Potential breaking schema changes in $(basename "$FILE_PATH")"
    echo "$PREFIX ============================================"
    for change in "${BREAKING_CHANGES[@]}"; do
        echo "$PREFIX   - $change"
    done
    echo "$PREFIX ============================================"
    echo "$PREFIX Review before deploying to production"
    echo ""
fi

# Always exit 0 - non-blocking
exit 0
