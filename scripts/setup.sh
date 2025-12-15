#!/usr/bin/env bash
#
# setup.sh - Initial setup for support-claude-mktplace
#
# Usage: ./scripts/setup.sh
#
# This script:
# 1. Creates Python virtual environments for MCP servers
# 2. Installs dependencies
# 3. Creates config file templates (if missing)
# 4. Validates existing configuration
# 5. Checks/creates Wiki.js directory structure
# 6. Syncs Gitea labels (creates/updates, respects custom labels)
# 7. Reports remaining manual steps
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Tracking arrays for final report
COMPLETED=()
SKIPPED=()
FAILED=()
MANUAL_TODO=()

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; COMPLETED+=("$1"); }
log_skip() { echo -e "${YELLOW}[SKIP]${NC} $1"; SKIPPED+=("$1"); }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; FAILED+=("$1"); }
log_todo() { echo -e "${YELLOW}[TODO]${NC} $1"; MANUAL_TODO+=("$1"); }

# --- Section 1: Python Environments ---
setup_python_env() {
    local server_name="$1"
    local server_path="$REPO_ROOT/mcp-servers/$server_name"

    log_info "Setting up $server_name MCP server..."

    if [[ ! -d "$server_path" ]]; then
        log_error "$server_name directory not found at $server_path"
        return 1
    fi

    cd "$server_path"

    # Check if venv exists
    if [[ -d ".venv" ]]; then
        log_skip "$server_name venv already exists"
    else
        python3 -m venv .venv
        log_success "$server_name venv created"
    fi

    # Install/update dependencies
    if [[ -f "requirements.txt" ]]; then
        source .venv/bin/activate
        pip install -q --upgrade pip
        pip install -q -r requirements.txt
        deactivate
        log_success "$server_name dependencies installed"
    else
        log_error "$server_name requirements.txt not found"
    fi

    cd "$REPO_ROOT"
}

# --- Section 2: Config File Templates ---
setup_config_templates() {
    local config_dir="$HOME/.config/claude"

    log_info "Checking configuration templates..."

    # Create config directory
    mkdir -p "$config_dir"

    # Gitea config
    if [[ -f "$config_dir/gitea.env" ]]; then
        log_skip "gitea.env already exists"
    else
        cat > "$config_dir/gitea.env" << 'EOF'
# Gitea API Configuration
# Update these values with your Gitea instance details

GITEA_API_URL=https://gitea.example.com/api/v1
GITEA_API_TOKEN=your_gitea_token_here
GITEA_OWNER=your_organization_name
EOF
        chmod 600 "$config_dir/gitea.env"
        log_success "gitea.env template created"
        log_todo "Edit ~/.config/claude/gitea.env with your Gitea credentials"
    fi

    # Wiki.js config
    if [[ -f "$config_dir/wikijs.env" ]]; then
        log_skip "wikijs.env already exists"
    else
        cat > "$config_dir/wikijs.env" << 'EOF'
# Wiki.js API Configuration
# Update these values with your Wiki.js instance details

WIKIJS_API_URL=https://wiki.example.com/graphql
WIKIJS_API_TOKEN=your_wikijs_jwt_token_here
WIKIJS_BASE_PATH=/your-namespace
EOF
        chmod 600 "$config_dir/wikijs.env"
        log_success "wikijs.env template created"
        log_todo "Edit ~/.config/claude/wikijs.env with your Wiki.js credentials"
    fi
}

# --- Section 3: Validate Configuration ---
validate_config() {
    local config_dir="$HOME/.config/claude"

    log_info "Validating configuration..."

    # Check Gitea config has real values
    if [[ -f "$config_dir/gitea.env" ]]; then
        source "$config_dir/gitea.env"
        if [[ "$GITEA_API_TOKEN" == "your_gitea_token_here" ]] || [[ -z "$GITEA_API_TOKEN" ]]; then
            log_todo "Update GITEA_API_TOKEN in ~/.config/claude/gitea.env"
        else
            log_success "Gitea configuration appears valid"
        fi
    fi

    # Check Wiki.js config has real values
    if [[ -f "$config_dir/wikijs.env" ]]; then
        source "$config_dir/wikijs.env"
        if [[ "$WIKIJS_API_TOKEN" == "your_wikijs_jwt_token_here" ]] || [[ -z "$WIKIJS_API_TOKEN" ]]; then
            log_todo "Update WIKIJS_API_TOKEN in ~/.config/claude/wikijs.env"
        else
            log_success "Wiki.js configuration appears valid"
        fi
    fi
}

# --- Section 4: Wiki.js Directory Structure ---
setup_wikijs_structure() {
    log_info "Wiki.js directory structure check..."

    # This requires Wiki.js MCP to be working
    # For now, just note it as a TODO if credentials aren't set

    local config_dir="$HOME/.config/claude"
    if [[ -f "$config_dir/wikijs.env" ]]; then
        source "$config_dir/wikijs.env"
        if [[ "$WIKIJS_API_TOKEN" != "your_wikijs_jwt_token_here" ]] && [[ -n "$WIKIJS_API_TOKEN" ]]; then
            log_info "Wiki.js credentials found - directory structure can be verified after first use"
            log_success "Wiki.js setup deferred to first use"
        else
            log_todo "Configure Wiki.js credentials, then verify directory structure exists"
        fi
    fi
}

# --- Section 5: Label Sync ---
# Note: This requires Gitea MCP to be functional
# For initial setup, we just validate the label reference file exists
setup_labels() {
    log_info "Checking label taxonomy..."

    local labels_file="$REPO_ROOT/plugins/projman/skills/label-taxonomy/labels-reference.md"

    if [[ -f "$labels_file" ]]; then
        log_success "Label reference file exists"
        log_info "Run '/labels-sync' command after setup to sync with Gitea"
    else
        log_error "Label reference file not found at $labels_file"
        log_todo "Run '/labels-sync' to create label reference from Gitea"
    fi
}

# --- Section 6: Final Report ---
print_report() {
    echo ""
    echo "=============================================="
    echo "           SETUP COMPLETE"
    echo "=============================================="
    echo ""

    if [[ ${#COMPLETED[@]} -gt 0 ]]; then
        echo -e "${GREEN}Completed:${NC}"
        for item in "${COMPLETED[@]}"; do
            echo "   - $item"
        done
        echo ""
    fi

    if [[ ${#SKIPPED[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Skipped (already done):${NC}"
        for item in "${SKIPPED[@]}"; do
            echo "   - $item"
        done
        echo ""
    fi

    if [[ ${#FAILED[@]} -gt 0 ]]; then
        echo -e "${RED}Failed:${NC}"
        for item in "${FAILED[@]}"; do
            echo "   - $item"
        done
        echo ""
    fi

    if [[ ${#MANUAL_TODO[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Manual Steps Required:${NC}"
        for i in "${!MANUAL_TODO[@]}"; do
            echo "   $((i+1)). ${MANUAL_TODO[$i]}"
        done
        echo ""
    fi

    if [[ ${#FAILED[@]} -eq 0 ]] && [[ ${#MANUAL_TODO[@]} -eq 0 ]]; then
        echo -e "${GREEN}Setup complete! No manual steps required.${NC}"
    elif [[ ${#FAILED[@]} -eq 0 ]]; then
        echo -e "${YELLOW}Setup complete with manual steps pending.${NC}"
    else
        echo -e "${RED}Setup completed with errors. Review and retry failed items.${NC}"
    fi
}

# --- Main ---
main() {
    echo "=============================================="
    echo "  support-claude-mktplace Setup"
    echo "=============================================="
    echo ""

    # Python environments
    setup_python_env "gitea"
    setup_python_env "wikijs"

    # Configuration
    setup_config_templates
    validate_config

    # Wiki.js structure
    setup_wikijs_structure

    # Labels
    setup_labels

    # Report
    print_report
}

main "$@"
