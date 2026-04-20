#!/bin/bash
# Install personal skill aliases so you can type /sprint instead of /projman:sprint etc.
# Run after installing the marketplace. Safe to re-run.

SKILLS_DIR="$HOME/.claude/skills"

echo "Installing skill aliases to $SKILLS_DIR..."

mkdir -p "$SKILLS_DIR"

# Map short-name → plugin
declare -A ALIASES=(
    [doc]="doc-guardian"
    [sprint]="projman"
    [adr]="projman"
    [project]="projman"
    [labels]="projman"
    [rfc]="projman"
    [projman]="projman"
    [data]="data-platform"
    [design]="dmc-design"
)

count=0
for skill in "${!ALIASES[@]}"; do
    plugin="${ALIASES[$skill]}"
    mkdir -p "$SKILLS_DIR/$skill"
    cat > "$SKILLS_DIR/$skill/SKILL.md" <<EOF
---
name: $skill
description: Routes to $plugin plugin
---

Invoke \`/$plugin:$skill \$ARGUMENTS\`
EOF
    echo "  ✓ $skill → $plugin"
    count=$((count + 1))
done

echo ""
echo "✓ Installed $count skill aliases"
echo ""
echo "Restart Claude Code for changes to take effect."
