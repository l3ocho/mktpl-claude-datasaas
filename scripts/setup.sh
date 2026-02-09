#!/usr/bin/env bash
#
# setup.sh - Automated setup for Leo Claude Marketplace
#
# ============================================================================
# NOTE: For interactive setup, use the /initial-setup command in Claude Code
# instead of this script. The command provides a guided wizard experience.
#
# This script is intended for:
# - CI/CD pipelines
# - Automated deployments
# - Bulk machine provisioning
# - Fallback when Claude Code is not available
# ============================================================================
#
# Usage: ./scripts/setup.sh
#
# This script:
# 1. Creates Python virtual environments for MCP servers (shared at root)
# 2. Installs dependencies
# 3. Creates config file templates (if missing)
# 4. Validates existing configuration
# 5. Installs personal skill aliases to ~/.claude/skills/
# 6. Validates label reference file
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
# MCP servers are now shared at repository root (v3.0.0+)
setup_shared_mcp() {
    local server_name="$1"
    local server_path="$REPO_ROOT/mcp-servers/$server_name"

    log_info "Setting up $server_name MCP server (shared)..."

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

    # Install/update dependencies and local package
    if [[ -f "requirements.txt" ]]; then
        source .venv/bin/activate
        pip install -q --upgrade pip
        pip install -q -r requirements.txt
        # Install local package in editable mode (required for MCP server to work)
        if [[ -f "pyproject.toml" ]]; then
            pip install -q -e .
            log_success "$server_name package installed (editable mode)"
        fi
        deactivate
        log_success "$server_name dependencies installed"
    else
        log_error "$server_name requirements.txt not found"
    fi

    cd "$REPO_ROOT"
}

# --- Section 2: Verify MCP Configuration ---
verify_mcp_config() {
    log_info "Verifying MCP configuration..."

    local mcp_json="$REPO_ROOT/.mcp.json"
    if [[ -f "$mcp_json" ]]; then
        log_success ".mcp.json exists at repository root"
    else
        log_error ".mcp.json missing at repository root"
        log_todo "Create .mcp.json with MCP server configurations"
    fi
}

# --- Section 3: Config File Templates ---
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
# Note: GITEA_ORG is configured per-project in .env

GITEA_API_URL=https://gitea.example.com/api/v1
GITEA_API_TOKEN=your_gitea_token_here
EOF
        chmod 600 "$config_dir/gitea.env"
        log_success "gitea.env template created"
        log_todo "Edit ~/.config/claude/gitea.env with your Gitea credentials"
    fi

    # NetBox config
    if [[ -f "$config_dir/netbox.env" ]]; then
        log_skip "netbox.env already exists"
    else
        cat > "$config_dir/netbox.env" << 'EOF'
# NetBox API Configuration
# Update these values with your NetBox instance details

NETBOX_API_URL=https://netbox.example.com/api
NETBOX_API_TOKEN=your_netbox_token_here
EOF
        chmod 600 "$config_dir/netbox.env"
        log_success "netbox.env template created"
        log_todo "Edit ~/.config/claude/netbox.env with your NetBox credentials"
    fi

    # Git-flow config (optional)
    if [[ -f "$config_dir/git-flow.env" ]]; then
        log_skip "git-flow.env already exists"
    else
        cat > "$config_dir/git-flow.env" << 'EOF'
# Git-Flow Default Configuration (optional)

GIT_WORKFLOW_STYLE=feature-branch
GIT_DEFAULT_BASE=development
GIT_AUTO_DELETE_MERGED=true
GIT_AUTO_PUSH=false
GIT_PROTECTED_BRANCHES=main,master,development,staging,production
GIT_COMMIT_STYLE=conventional
GIT_CO_AUTHOR=true
EOF
        chmod 600 "$config_dir/git-flow.env"
        log_success "git-flow.env template created"
    fi

    # PostgreSQL config (for data-platform, optional)
    if [[ -f "$config_dir/postgres.env" ]]; then
        log_skip "postgres.env already exists"
    else
        cat > "$config_dir/postgres.env" << 'EOF'
# PostgreSQL Configuration (for data-platform plugin)
# Update with your PostgreSQL connection URL
# This is OPTIONAL - pandas tools work without it

POSTGRES_URL=postgresql://user:password@localhost:5432/database
EOF
        chmod 600 "$config_dir/postgres.env"
        log_success "postgres.env template created"
        log_todo "Edit ~/.config/claude/postgres.env with your PostgreSQL credentials (optional)"
    fi
}

# --- Section 4: Validate Configuration ---
validate_config() {
    local config_dir="$HOME/.config/claude"

    log_info "Validating configuration..."

    # Check Gitea config has real values
    if [[ -f "$config_dir/gitea.env" ]]; then
        source "$config_dir/gitea.env"
        if [[ "${GITEA_API_TOKEN:-}" == "your_gitea_token_here" ]] || [[ -z "${GITEA_API_TOKEN:-}" ]]; then
            log_todo "Update GITEA_API_TOKEN in ~/.config/claude/gitea.env"
        else
            log_success "Gitea configuration appears valid"
        fi
    fi

    # Check NetBox config has real values
    if [[ -f "$config_dir/netbox.env" ]]; then
        source "$config_dir/netbox.env"
        if [[ "${NETBOX_API_TOKEN:-}" == "your_netbox_token_here" ]] || [[ -z "${NETBOX_API_TOKEN:-}" ]]; then
            log_todo "Update NETBOX_API_TOKEN in ~/.config/claude/netbox.env"
        else
            log_success "NetBox configuration appears valid"
        fi
    fi
}

# --- Section 5: Skill Aliases ---
setup_skill_aliases() {
    log_info "Installing personal skill aliases..."

    local alias_script="$REPO_ROOT/scripts/install-skill-aliases.sh"

    if [[ -f "$alias_script" ]]; then
        if bash "$alias_script"; then
            log_success "Skill aliases installed to ~/.claude/skills/"
        else
            log_error "Failed to install skill aliases"
            log_todo "Run $alias_script manually to install skill aliases"
        fi
    else
        log_error "install-skill-aliases.sh not found at $alias_script"
    fi
}

# --- Section 6: Label Sync ---
# Note: This requires Gitea MCP to be functional
# For initial setup, we just validate the label reference file exists
setup_labels() {
    log_info "Checking label taxonomy..."

    local labels_file="$REPO_ROOT/plugins/projman/skills/label-taxonomy/labels-reference.md"

    if [[ -f "$labels_file" ]]; then
        log_success "Label reference file exists"
        log_info "Run '/labels sync' command after setup to sync with Gitea"
    else
        log_error "Label reference file not found at $labels_file"
        log_todo "Run '/labels sync' to create label reference from Gitea"
    fi
}

# --- Section 7: Final Report ---
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
    echo "  Leo Claude Marketplace Setup (v5.7.1)"
    echo "=============================================="
    echo ""

    # Shared MCP servers at repository root
    setup_shared_mcp "gitea"
    setup_shared_mcp "netbox"
    setup_shared_mcp "data-platform"
    setup_shared_mcp "viz-platform"
    setup_shared_mcp "contract-validator"

    # Verify MCP configuration at root
    verify_mcp_config

    # Configuration
    setup_config_templates
    validate_config

    # Skill aliases
    setup_skill_aliases

    # Labels
    setup_labels

    # Report
    print_report
}

main "$@"
