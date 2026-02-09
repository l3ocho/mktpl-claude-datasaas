#!/bin/bash
# Install personal skill aliases for dispatch routing
# Run this after installing the marketplace on a new machine

SKILLS_DIR="$HOME/.claude/skills"

echo "Installing skill aliases to $SKILLS_DIR..."

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Create all skill aliases
for skill in doc sprint pr sentinel cv data viz cmdb api db-migrate react test seed release deploy debug-mcp gitflow hygiene labels adr project projman claude-config clarity; do
    case $skill in
        doc) plugin="doc-guardian" ;;
        sprint|adr|project|labels|projman) plugin="projman" ;;
        pr) plugin="pr-review" ;;
        sentinel) plugin="code-sentinel" ;;
        cv) plugin="contract-validator" ;;
        data) plugin="data-platform" ;;
        viz) plugin="viz-platform" ;;
        cmdb) plugin="cmdb-assistant" ;;
        api) plugin="saas-api-platform" ;;
        db-migrate) plugin="saas-db-migrate" ;;
        react) plugin="saas-react-platform" ;;
        test) plugin="saas-test-pilot" ;;
        seed) plugin="data-seed" ;;
        release) plugin="ops-release-manager" ;;
        deploy) plugin="ops-deploy-pipeline" ;;
        debug-mcp) plugin="debug-mcp" ;;
        gitflow) plugin="git-flow" ;;
        hygiene) plugin="project-hygiene" ;;
        claude-config) plugin="claude-config-maintainer" ;;
        clarity) plugin="clarity-assist" ;;
    esac

    mkdir -p "$SKILLS_DIR/$skill"
    cat > "$SKILLS_DIR/$skill/SKILL.md" <<EOF
---
name: $skill
description: Routes to $plugin plugin
---

Invoke \`/$plugin:$skill \$ARGUMENTS\`
EOF
    echo "  ✓ $skill → $plugin"
done

echo ""
echo "✓ Installed 24 skill aliases"
echo ""
echo "Restart Claude Code for changes to take effect."
