#!/bin/bash
# project-hygiene cleanup hook
# Runs after task completion to clean up temp files and manage orphans

set -euo pipefail

# Configuration
PROJECT_ROOT="${PROJECT_ROOT:-.}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"
CONFIG_FILE="${PROJECT_ROOT}/.hygiene.json"
LOG_DIR="${PROJECT_ROOT}/.dev/logs"
SCRATCH_DIR="${PROJECT_ROOT}/.dev/scratch"
LOG_FILE="${LOG_DIR}/hygiene-$(date +%Y%m%d-%H%M%S).log"

# Default allowed root files (can be overridden by .hygiene.json)
DEFAULT_ALLOWED_ROOT=(
    ".git"
    ".gitignore"
    ".gitattributes"
    ".editorconfig"
    ".env"
    ".env.example"
    ".env.local"
    ".nvmrc"
    ".node-version"
    ".python-version"
    ".ruby-version"
    ".tool-versions"
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "CONTRIBUTING.md"
    "CLAUDE.md"
    "package.json"
    "package-lock.json"
    "yarn.lock"
    "pnpm-lock.yaml"
    "Makefile"
    "Dockerfile"
    "docker-compose.yml"
    "docker-compose.yaml"
    "Cargo.toml"
    "Cargo.lock"
    "go.mod"
    "go.sum"
    "requirements.txt"
    "setup.py"
    "pyproject.toml"
    "poetry.lock"
    "Gemfile"
    "Gemfile.lock"
    "tsconfig.json"
    "jsconfig.json"
    ".eslintrc*"
    ".prettierrc*"
    "vite.config.*"
    "webpack.config.*"
    "rollup.config.*"
    ".hygiene.json"
)

# Temp file patterns to delete
TEMP_PATTERNS=(
    "*.tmp"
    "*.bak"
    "*.swp"
    "*.swo"
    "*~"
    ".DS_Store"
    "Thumbs.db"
    "*.log"
    "*.orig"
    "*.pyc"
    "*.pyo"
)

# Directory patterns to delete
TEMP_DIRS=(
    "__pycache__"
    ".pytest_cache"
    ".mypy_cache"
    ".ruff_cache"
    "node_modules/.cache"
    ".next/cache"
    ".nuxt/.cache"
    ".turbo"
    "*.egg-info"
    ".eggs"
    "dist"
    "build"
)

# Orphan patterns to identify
ORPHAN_PATTERNS=(
    "test_*.py"
    "debug_*"
    "*_backup.*"
    "*_old.*"
    "*_bak.*"
    "*.backup"
    "temp_*"
    "tmp_*"
)

# Initialize
DELETED_COUNT=0
WARNED_COUNT=0
ORPHAN_COUNT=0
MOVE_ORPHANS=false

# Logging function
log() {
    local msg="[$(date +%H:%M:%S)] $1"
    echo "$msg"
    if [[ -f "$LOG_FILE" ]]; then
        echo "$msg" >> "$LOG_FILE"
    fi
}

log_action() {
    local action="$1"
    local target="$2"
    log "  $action: $target"
}

# Load project-local config if exists
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        log "Loading config from $CONFIG_FILE"

        # Check if move_orphans is enabled
        if command -v jq &>/dev/null; then
            MOVE_ORPHANS=$(jq -r '.move_orphans // false' "$CONFIG_FILE" 2>/dev/null || echo "false")

            # Load additional allowed root files
            local extra_allowed
            extra_allowed=$(jq -r '.allowed_root_files // [] | .[]' "$CONFIG_FILE" 2>/dev/null || true)
            if [[ -n "$extra_allowed" ]]; then
                while IFS= read -r file; do
                    DEFAULT_ALLOWED_ROOT+=("$file")
                done <<< "$extra_allowed"
            fi

            # Load additional temp patterns
            local extra_temp
            extra_temp=$(jq -r '.temp_patterns // [] | .[]' "$CONFIG_FILE" 2>/dev/null || true)
            if [[ -n "$extra_temp" ]]; then
                while IFS= read -r pattern; do
                    TEMP_PATTERNS+=("$pattern")
                done <<< "$extra_temp"
            fi

            # Load ignore patterns (files to never touch)
            IGNORE_PATTERNS=()
            local ignore
            ignore=$(jq -r '.ignore_patterns // [] | .[]' "$CONFIG_FILE" 2>/dev/null || true)
            if [[ -n "$ignore" ]]; then
                while IFS= read -r pattern; do
                    IGNORE_PATTERNS+=("$pattern")
                done <<< "$ignore"
            fi
        else
            log "Warning: jq not installed, using default config"
        fi
    fi
}

# Check if file should be ignored
should_ignore() {
    local file="$1"
    local basename
    basename=$(basename "$file")

    for pattern in "${IGNORE_PATTERNS[@]:-}"; do
        if [[ "$basename" == $pattern ]] || [[ "$file" == $pattern ]]; then
            return 0
        fi
    done
    return 1
}

# Check if file is in allowed root list
is_allowed_root() {
    local file="$1"
    local basename
    basename=$(basename "$file")

    for allowed in "${DEFAULT_ALLOWED_ROOT[@]}"; do
        # Support wildcards in allowed patterns
        if [[ "$basename" == $allowed ]]; then
            return 0
        fi
    done
    return 1
}

# Check if file matches orphan pattern
is_orphan() {
    local file="$1"
    local basename
    basename=$(basename "$file")

    for pattern in "${ORPHAN_PATTERNS[@]}"; do
        if [[ "$basename" == $pattern ]]; then
            return 0
        fi
    done
    return 1
}

# Setup directories
setup_dirs() {
    mkdir -p "$LOG_DIR"
    if [[ "$MOVE_ORPHANS" == "true" ]]; then
        mkdir -p "$SCRATCH_DIR"
    fi

    # Start log file
    echo "=== Project Hygiene Cleanup ===" > "$LOG_FILE"
    echo "Started: $(date)" >> "$LOG_FILE"
    echo "Project: $PROJECT_ROOT" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

# Delete temp files
cleanup_temp_files() {
    log "Cleaning temp files..."

    for pattern in "${TEMP_PATTERNS[@]}"; do
        while IFS= read -r -d '' file; do
            if should_ignore "$file"; then
                continue
            fi
            rm -f "$file"
            log_action "DELETED" "$file"
            ((DELETED_COUNT++))
        done < <(find "$PROJECT_ROOT" -name "$pattern" -type f -print0 2>/dev/null || true)
    done
}

# Delete temp directories
cleanup_temp_dirs() {
    log "Cleaning temp directories..."

    for pattern in "${TEMP_DIRS[@]}"; do
        while IFS= read -r -d '' dir; do
            if should_ignore "$dir"; then
                continue
            fi
            rm -rf "$dir"
            log_action "DELETED DIR" "$dir"
            ((DELETED_COUNT++))
        done < <(find "$PROJECT_ROOT" -name "$pattern" -type d -print0 2>/dev/null || true)
    done
}

# Warn about unexpected root files
check_root_files() {
    log "Checking root files..."

    local unexpected_files=()

    while IFS= read -r -d '' file; do
        local basename
        basename=$(basename "$file")

        # Skip directories
        [[ -d "$file" ]] && continue

        # Skip if in allowed list
        is_allowed_root "$basename" && continue

        # Skip if should be ignored
        should_ignore "$basename" && continue

        unexpected_files+=("$basename")
        log_action "WARNING" "Unexpected root file: $basename"
        ((WARNED_COUNT++))
    done < <(find "$PROJECT_ROOT" -maxdepth 1 -print0 2>/dev/null || true)

    if [[ ${#unexpected_files[@]} -gt 0 ]]; then
        log ""
        log "⚠️  Unexpected files in project root:"
        for f in "${unexpected_files[@]}"; do
            log "    - $f"
        done
    fi
}

# Identify and handle orphaned files
handle_orphans() {
    log "Checking for orphaned files..."

    local orphan_files=()

    for pattern in "${ORPHAN_PATTERNS[@]}"; do
        while IFS= read -r -d '' file; do
            if should_ignore "$file"; then
                continue
            fi

            orphan_files+=("$file")

            if [[ "$MOVE_ORPHANS" == "true" ]]; then
                local dest="${SCRATCH_DIR}/$(basename "$file")"
                # Handle duplicates
                if [[ -f "$dest" ]]; then
                    dest="${SCRATCH_DIR}/$(date +%Y%m%d%H%M%S)_$(basename "$file")"
                fi
                mv "$file" "$dest"
                log_action "MOVED" "$file -> $dest"
            else
                log_action "ORPHAN" "$file"
            fi
            ((ORPHAN_COUNT++))
        done < <(find "$PROJECT_ROOT" -name "$pattern" -type f -print0 2>/dev/null || true)
    done

    if [[ ${#orphan_files[@]} -gt 0 && "$MOVE_ORPHANS" != "true" ]]; then
        log ""
        log "📦 Orphaned files found (enable move_orphans in .hygiene.json to auto-move):"
        for f in "${orphan_files[@]}"; do
            log "    - $f"
        done
    fi
}

# Summary
print_summary() {
    log ""
    log "=== Cleanup Summary ==="
    log "  Deleted: $DELETED_COUNT items"
    log "  Warnings: $WARNED_COUNT unexpected root files"
    log "  Orphans: $ORPHAN_COUNT files"
    if [[ "$MOVE_ORPHANS" == "true" ]]; then
        log "  Orphans moved to: $SCRATCH_DIR"
    fi
    log "  Log file: $LOG_FILE"
    log ""
}

# Main
main() {
    cd "$PROJECT_ROOT" || exit 1

    load_config
    setup_dirs

    log "Starting project hygiene cleanup..."
    log ""

    cleanup_temp_files
    cleanup_temp_dirs
    check_root_files
    handle_orphans

    print_summary

    # Exit with warning code if issues found
    if [[ $WARNED_COUNT -gt 0 || $ORPHAN_COUNT -gt 0 ]]; then
        exit 0  # Still success, but logged warnings
    fi
}

main "$@"
