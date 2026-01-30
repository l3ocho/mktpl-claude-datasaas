#!/bin/bash
# cmdb-assistant SessionStart hook
# Tests NetBox API connectivity and checks for data quality issues
# All output MUST have [cmdb-assistant] prefix
# Non-blocking: always exits 0

set -euo pipefail

PREFIX="[cmdb-assistant]"

# Load NetBox configuration
NETBOX_CONFIG="$HOME/.config/claude/netbox.env"

if [[ ! -f "$NETBOX_CONFIG" ]]; then
    echo "$PREFIX NetBox not configured - run /cmdb-assistant:initial-setup"
    exit 0
fi

# Source config
source "$NETBOX_CONFIG"

# Validate required variables
if [[ -z "${NETBOX_API_URL:-}" ]] || [[ -z "${NETBOX_API_TOKEN:-}" ]]; then
    echo "$PREFIX Missing NETBOX_API_URL or NETBOX_API_TOKEN in config"
    exit 0
fi

# Helper function to make authenticated API calls
# Token passed via curl config to avoid exposure in process listings
netbox_curl() {
    local url="$1"
    curl -s -K - <<EOF 2>/dev/null
-H "Authorization: Token ${NETBOX_API_TOKEN}"
-H "Accept: application/json"
url = "${url}"
EOF
}

# Quick API connectivity test (5s timeout)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -m 5 -K - <<EOF 2>/dev/null || echo "000"
-H "Authorization: Token ${NETBOX_API_TOKEN}"
-H "Accept: application/json"
url = "${NETBOX_API_URL}/"
EOF
)

if [[ "$HTTP_CODE" == "000" ]]; then
    echo "$PREFIX NetBox API unreachable (timeout/connection error)"
    exit 0
elif [[ "$HTTP_CODE" != "200" ]]; then
    echo "$PREFIX NetBox API returned HTTP $HTTP_CODE - check credentials"
    exit 0
fi

# Check for VMs without site assignment (data quality)
VMS_RESPONSE=$(curl -s -m 5 -K - <<EOF 2>/dev/null || echo '{"count":0}'
-H "Authorization: Token ${NETBOX_API_TOKEN}"
-H "Accept: application/json"
url = "${NETBOX_API_URL}/virtualization/virtual-machines/?site__isnull=true&limit=1"
EOF
)

VMS_NO_SITE=$(echo "$VMS_RESPONSE" | grep -o '"count":[0-9]*' | cut -d: -f2 || echo "0")

if [[ "$VMS_NO_SITE" -gt 0 ]]; then
    echo "$PREFIX $VMS_NO_SITE VMs without site assignment - run /cmdb-audit for details"
fi

# Check for devices without platform
DEVICES_RESPONSE=$(curl -s -m 5 -K - <<EOF 2>/dev/null || echo '{"count":0}'
-H "Authorization: Token ${NETBOX_API_TOKEN}"
-H "Accept: application/json"
url = "${NETBOX_API_URL}/dcim/devices/?platform__isnull=true&limit=1"
EOF
)

DEVICES_NO_PLATFORM=$(echo "$DEVICES_RESPONSE" | grep -o '"count":[0-9]*' | cut -d: -f2 || echo "0")

if [[ "$DEVICES_NO_PLATFORM" -gt 0 ]]; then
    echo "$PREFIX $DEVICES_NO_PLATFORM devices without platform - consider updating"
fi

exit 0
