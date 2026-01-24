#!/bin/bash
# release.sh - Create a new release with version consistency
#
# Usage: ./scripts/release.sh X.Y.Z
#
# This script ensures all version references are updated consistently:
# 1. CHANGELOG.md - [Unreleased] becomes [X.Y.Z] - YYYY-MM-DD
# 2. README.md - Title updated to vX.Y.Z
# 3. marketplace.json - version field updated
# 4. Git commit and tag created
#
# Prerequisites:
# - Clean working directory (no uncommitted changes)
# - [Unreleased] section in CHANGELOG.md with content
# - On development branch

set -e

VERSION=$1
DATE=$(date +%Y-%m-%d)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() { echo -e "${RED}ERROR: $1${NC}" >&2; exit 1; }
warn() { echo -e "${YELLOW}WARNING: $1${NC}"; }
success() { echo -e "${GREEN}$1${NC}"; }
info() { echo -e "$1"; }

# Validate arguments
if [ -z "$VERSION" ]; then
    echo "Usage: ./scripts/release.sh X.Y.Z"
    echo ""
    echo "Example: ./scripts/release.sh 3.2.0"
    echo ""
    echo "This will:"
    echo "  1. Update CHANGELOG.md [Unreleased] -> [X.Y.Z] - $(date +%Y-%m-%d)"
    echo "  2. Update README.md title to vX.Y.Z"
    echo "  3. Update marketplace.json version to X.Y.Z"
    echo "  4. Commit with message 'chore: release vX.Y.Z'"
    echo "  5. Create git tag vX.Y.Z"
    exit 1
fi

# Validate version format
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    error "Invalid version format. Use X.Y.Z (e.g., 3.2.0)"
fi

# Check we're in the right directory
if [ ! -f "CHANGELOG.md" ] || [ ! -f "README.md" ] || [ ! -f ".claude-plugin/marketplace.json" ]; then
    error "Must run from repository root (CHANGELOG.md, README.md, .claude-plugin/marketplace.json must exist)"
fi

# Check for clean working directory
if [ -n "$(git status --porcelain)" ]; then
    warn "Working directory has uncommitted changes"
    echo ""
    git status --short
    echo ""
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check current branch
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "development" ] && [ "$BRANCH" != "main" ]; then
    warn "Not on development or main branch (current: $BRANCH)"
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check [Unreleased] section has content
if ! grep -q "## \[Unreleased\]" CHANGELOG.md; then
    error "CHANGELOG.md missing [Unreleased] section"
fi

# Check if tag already exists
if git tag -l | grep -q "^v$VERSION$"; then
    error "Tag v$VERSION already exists"
fi

info ""
info "=== Release v$VERSION ==="
info ""

# Show what will change
info "Changes to be made:"
info "  CHANGELOG.md: [Unreleased] -> [$VERSION] - $DATE"
info "  README.md: title -> v$VERSION"
info "  marketplace.json: version -> $VERSION"
info "  Git: commit + tag v$VERSION"
info ""

# Preview CHANGELOG [Unreleased] content
info "Current [Unreleased] content:"
info "---"
sed -n '/^## \[Unreleased\]/,/^## \[/p' CHANGELOG.md | head -30
info "---"
info ""

read -p "Proceed with release? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    info "Aborted"
    exit 0
fi

info ""
info "Updating files..."

# 1. Update CHANGELOG.md
# Replace [Unreleased] with [X.Y.Z] - DATE and add new [Unreleased] section
sed -i "s/^## \[Unreleased\]$/## [Unreleased]\n\n*Changes staged for the next release*\n\n---\n\n## [$VERSION] - $DATE/" CHANGELOG.md

# Remove the placeholder text if it exists after the new [Unreleased]
sed -i '/^\*Changes staged for the next release\*$/d' CHANGELOG.md

# Clean up any double blank lines
sed -i '/^$/N;/^\n$/d' CHANGELOG.md

success "  CHANGELOG.md updated"

# 2. Update README.md title
sed -i "s/^# Leo Claude Marketplace - v[0-9]\+\.[0-9]\+\.[0-9]\+$/# Leo Claude Marketplace - v$VERSION/" README.md
success "  README.md updated"

# 3. Update marketplace.json version
sed -i "s/\"version\": \"[0-9]\+\.[0-9]\+\.[0-9]\+\"/\"version\": \"$VERSION\"/" .claude-plugin/marketplace.json
success "  marketplace.json updated"

info ""
info "Files updated. Review changes:"
info ""
git diff --stat
info ""
git diff CHANGELOG.md | head -40
info ""

read -p "Commit and tag? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    warn "Changes made but not committed. Run 'git checkout -- .' to revert."
    exit 0
fi

# Commit
git add CHANGELOG.md README.md .claude-plugin/marketplace.json
git commit -m "chore: release v$VERSION"
success "  Committed"

# Tag
git tag "v$VERSION"
success "  Tagged v$VERSION"

info ""
success "=== Release v$VERSION created ==="
info ""
info "Next steps:"
info "  1. Review the commit: git show HEAD"
info "  2. Push to remote: git push && git push --tags"
info "  3. Merge to main if on development branch"
info ""
