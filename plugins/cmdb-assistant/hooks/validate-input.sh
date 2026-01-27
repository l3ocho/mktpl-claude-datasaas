#!/bin/bash
# cmdb-assistant PreToolUse validation hook
# Validates input parameters for create/update operations
# NON-BLOCKING: Warns but allows operation to proceed (always exits 0)

set -euo pipefail

PREFIX="[cmdb-assistant]"

# Read tool input from stdin
INPUT=$(cat)

# Extract tool name from the input
# Format varies, try to find tool_name or name field
TOOL_NAME=""
if echo "$INPUT" | grep -q '"tool_name"'; then
    TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/' || true)
elif echo "$INPUT" | grep -q '"name"'; then
    TOOL_NAME=$(echo "$INPUT" | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/' || true)
fi

# If we can't determine the tool, exit silently
if [[ -z "$TOOL_NAME" ]]; then
    exit 0
fi

# VM creation/update validation
if echo "$TOOL_NAME" | grep -qE "virt_create_vm|virt_create_virtual_machine|virt_update_vm|virt_update_virtual_machine"; then
    WARNINGS=()

    # Check for missing site
    if ! echo "$INPUT" | grep -qE '"site"[[:space:]]*:[[:space:]]*[0-9]'; then
        WARNINGS+=("no site assigned")
    fi

    # Check for missing tenant
    if ! echo "$INPUT" | grep -qE '"tenant"[[:space:]]*:[[:space:]]*[0-9]'; then
        WARNINGS+=("no tenant assigned")
    fi

    # Check for missing platform
    if ! echo "$INPUT" | grep -qE '"platform"[[:space:]]*:[[:space:]]*[0-9]'; then
        WARNINGS+=("no platform assigned")
    fi

    if [[ ${#WARNINGS[@]} -gt 0 ]]; then
        echo "$PREFIX VM best practice: $(IFS=', '; echo "${WARNINGS[*]}") - consider assigning for data quality"
    fi
fi

# Device creation/update validation
if echo "$TOOL_NAME" | grep -qE "dcim_create_device|dcim_update_device"; then
    WARNINGS=()

    # Check for missing platform
    if ! echo "$INPUT" | grep -qE '"platform"[[:space:]]*:[[:space:]]*[0-9]'; then
        WARNINGS+=("no platform assigned")
    fi

    # Check for missing tenant
    if ! echo "$INPUT" | grep -qE '"tenant"[[:space:]]*:[[:space:]]*[0-9]'; then
        WARNINGS+=("no tenant assigned")
    fi

    if [[ ${#WARNINGS[@]} -gt 0 ]]; then
        echo "$PREFIX Device best practice: $(IFS=', '; echo "${WARNINGS[*]}") - consider assigning"
    fi
fi

# Cluster creation validation
if echo "$TOOL_NAME" | grep -qE "virt_create_cluster"; then
    # Check for missing site scope
    if ! echo "$INPUT" | grep -qE '"site"[[:space:]]*:[[:space:]]*[0-9]'; then
        echo "$PREFIX Cluster best practice: no site scope - clusters should be scoped to a site"
    fi
fi

# Always allow operation (non-blocking)
exit 0
