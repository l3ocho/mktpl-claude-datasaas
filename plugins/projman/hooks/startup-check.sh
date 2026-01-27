#!/bin/bash
# projman startup check hook
# Checks for common issues AND suggests sprint planning proactively
# All output MUST have [projman] prefix

PREFIX="[projman]"

# Calculate paths
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"
# Marketplace root is 2 levels up from plugin root (plugins/projman -> .)
MARKETPLACE_ROOT="$(dirname "$(dirname "$PLUGIN_ROOT")")"
VENV_REPAIR_SCRIPT="$MARKETPLACE_ROOT/scripts/venv-repair.sh"
PLUGIN_CACHE="$HOME/.claude/plugins/cache/leo-claude-mktplace"

# ============================================================================
# Clear stale plugin cache (MUST run before MCP servers load)
# ============================================================================
# The cache at ~/.claude/plugins/cache/ holds versioned .mcp.json files.
# After marketplace updates, cached configs may point to old paths.
# Clearing forces Claude to read fresh configs from installed marketplace.

if [[ -d "$PLUGIN_CACHE" ]]; then
    rm -rf "$PLUGIN_CACHE"
    # Don't output anything - this should be silent and automatic
fi

# ============================================================================
# Auto-repair MCP venvs (runs before other checks)
# ============================================================================

if [[ -x "$VENV_REPAIR_SCRIPT" ]]; then
    # Run venv repair - this creates symlinks to cached venvs
    # Only outputs messages if something needed fixing
    "$VENV_REPAIR_SCRIPT" 2>/dev/null || {
        echo "$PREFIX MCP venv setup failed - run: cd $MARKETPLACE_ROOT && ./scripts/setup-venvs.sh"
        exit 0
    }
else
    # Fallback: just check if venv exists
    VENV_PATH="$PLUGIN_ROOT/mcp-servers/gitea/.venv/bin/python"
    if [[ ! -f "$VENV_PATH" ]]; then
        echo "$PREFIX MCP venvs missing - run setup.sh from installed marketplace"
        exit 0
    fi
fi

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
        OPEN_ISSUES=$(curl -s -m 5 \
            -H "Authorization: token $GITEA_API_TOKEN" \
            "${GITEA_API_URL}/repos/${GITEA_REPO}/issues?state=open&milestone=none&limit=1" 2>/dev/null | \
            grep -c '"number"' || echo "0")

        if [[ "$OPEN_ISSUES" -gt 0 ]]; then
            # Count total unplanned issues
            TOTAL_UNPLANNED=$(curl -s -m 5 \
                -H "Authorization: token $GITEA_API_TOKEN" \
                "${GITEA_API_URL}/repos/${GITEA_REPO}/issues?state=open&milestone=none" 2>/dev/null | \
                grep -c '"number"' || echo "?")
            echo "$PREFIX ${TOTAL_UNPLANNED} open issues without milestone - consider /sprint-plan"
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
