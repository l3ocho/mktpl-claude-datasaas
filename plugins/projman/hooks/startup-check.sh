#!/bin/bash
# projman startup check hook
# Checks for common issues AND suggests sprint planning proactively
# All output MUST have [projman] prefix

PREFIX="[projman]"

# Calculate paths
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"

# Check git remote vs .env config (only if .env exists)
if [[ -f ".env" ]]; then
    CONFIGURED_REPO=$(grep -E "^GITEA_REPO=" .env 2>/dev/null | cut -d'=' -f2 | tr -d '"' || true)
    if [[ -n "$CONFIGURED_REPO" ]]; then
        CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/.*[:/]\([^/]*\/[^.]*\).*/\1/' || true)
        if [[ -n "$CURRENT_REMOTE" && "$CONFIGURED_REPO" != "$CURRENT_REMOTE" ]]; then
            echo "$PREFIX Git remote mismatch - run /project-sync"
            exit 0
        fi
    fi
fi

# Check for open issues (suggests sprint planning)
# Only if .env exists with valid GITEA config
if [[ -f ".env" ]]; then
    GITEA_API_URL=$(grep -E "^GITEA_API_URL=" ~/.config/claude/gitea.env 2>/dev/null | cut -d'=' -f2 | tr -d '"' || true)
    GITEA_API_TOKEN=$(grep -E "^GITEA_API_TOKEN=" ~/.config/claude/gitea.env 2>/dev/null | cut -d'=' -f2 | tr -d '"' || true)
    GITEA_REPO=$(grep -E "^GITEA_REPO=" .env 2>/dev/null | cut -d'=' -f2 | tr -d '"' || true)

    if [[ -n "$GITEA_API_URL" && -n "$GITEA_API_TOKEN" && -n "$GITEA_REPO" ]]; then
        # Quick check for open issues without milestone (unplanned work)
        # Note: grep -c returns 0 on no match but exits non-zero, causing || to also fire
        # Use subshell to ensure single value
        OPEN_ISSUES=$(curl -s -m 5 \
            -H "Authorization: token $GITEA_API_TOKEN" \
            "${GITEA_API_URL}/repos/${GITEA_REPO}/issues?state=open&milestone=none&limit=1" 2>/dev/null | \
            grep -c '"number"' 2>/dev/null) || OPEN_ISSUES=0

        if [[ "$OPEN_ISSUES" -gt 0 ]]; then
            # Count total unplanned issues
            TOTAL_UNPLANNED=$(curl -s -m 5 \
                -H "Authorization: token $GITEA_API_TOKEN" \
                "${GITEA_API_URL}/repos/${GITEA_REPO}/issues?state=open&milestone=none" 2>/dev/null | \
                grep -c '"number"' 2>/dev/null) || TOTAL_UNPLANNED="?"
            echo "$PREFIX ${TOTAL_UNPLANNED} open issues without milestone - consider /sprint-plan"
        fi
    fi
fi

# ============================================================================
# Check version consistency across files (early drift detection)
# ============================================================================
# Versions must stay in sync across: README.md, marketplace.json, CHANGELOG.md
# Drift here causes confusion and release issues

if [[ -f "README.md" && -f ".claude-plugin/marketplace.json" && -f "CHANGELOG.md" ]]; then
    VERSION_README=$(grep -oE "^# .* - v[0-9]+\.[0-9]+\.[0-9]+" README.md 2>/dev/null | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" || echo "")
    # Extract metadata.version specifically (appears after "metadata" in marketplace.json)
    VERSION_MARKETPLACE=$(sed -n '/"metadata"/,/}/p' .claude-plugin/marketplace.json 2>/dev/null | grep -oE '"version"[[:space:]]*:[[:space:]]*"[0-9]+\.[0-9]+\.[0-9]+"' | head -1 | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" || echo "")
    VERSION_CHANGELOG=$(grep -oE "^## \[[0-9]+\.[0-9]+\.[0-9]+\]" CHANGELOG.md 2>/dev/null | head -1 | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" || echo "")

    if [[ -n "$VERSION_README" && -n "$VERSION_MARKETPLACE" && -n "$VERSION_CHANGELOG" ]]; then
        if [[ "$VERSION_README" != "$VERSION_MARKETPLACE" ]] || [[ "$VERSION_README" != "$VERSION_CHANGELOG" ]]; then
            echo "$PREFIX Version mismatch detected:"
            echo "$PREFIX   README.md:        v$VERSION_README"
            echo "$PREFIX   marketplace.json: v$VERSION_MARKETPLACE"
            echo "$PREFIX   CHANGELOG.md:     v$VERSION_CHANGELOG"
            echo "$PREFIX Run /suggest-version to analyze and fix"
        fi
    fi
fi

# Check for CHANGELOG.md [Unreleased] content (version management)
if [[ -f "CHANGELOG.md" ]]; then
    # Check if there's content under [Unreleased] that hasn't been released
    UNRELEASED_CONTENT=$(sed -n '/## \[Unreleased\]/,/## \[/p' CHANGELOG.md 2>/dev/null | grep -E '^### (Added|Changed|Fixed|Removed|Deprecated)' | head -1 || true)
    if [[ -n "$UNRELEASED_CONTENT" ]]; then
        UNRELEASED_LINES=$(sed -n '/## \[Unreleased\]/,/## \[/p' CHANGELOG.md 2>/dev/null | grep -E '^- ' | wc -l | tr -d ' ')
        if [[ "$UNRELEASED_LINES" -gt 0 ]]; then
            echo "$PREFIX ${UNRELEASED_LINES} unreleased changes in CHANGELOG - consider version bump"
        fi
    fi
fi

exit 0
