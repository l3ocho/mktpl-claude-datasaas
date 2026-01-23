#!/bin/bash
# claude-config-maintainer: enforce mandatory behavior rules
# Checks if CLAUDE.md has the rules, adds them if missing

PREFIX="[claude-config-maintainer]"

# Find CLAUDE.md in current directory or parent
CLAUDE_MD=""
if [ -f "./CLAUDE.md" ]; then
    CLAUDE_MD="./CLAUDE.md"
elif [ -f "../CLAUDE.md" ]; then
    CLAUDE_MD="../CLAUDE.md"
fi

# If no CLAUDE.md found, exit silently
if [ -z "$CLAUDE_MD" ]; then
    exit 0
fi

# Check if mandatory rules exist
if grep -q "MANDATORY BEHAVIOR RULES" "$CLAUDE_MD" 2>/dev/null; then
    # Rules exist, all good
    exit 0
fi

# Rules missing - add them
RULES='## ⛔ MANDATORY BEHAVIOR RULES - READ FIRST

**These rules are NON-NEGOTIABLE. Violating them wastes the user'\''s time and money.**

### 1. WHEN USER ASKS YOU TO CHECK SOMETHING - CHECK EVERYTHING
- Search ALL locations, not just where you think it is
- Check cache directories: `~/.claude/plugins/cache/`
- Check installed: `~/.claude/plugins/marketplaces/`
- Check source directories
- **NEVER say "no" or "that'\''s not the issue" without exhaustive verification**

### 2. WHEN USER SAYS SOMETHING IS WRONG - BELIEVE THEM
- The user knows their system better than you
- Investigate thoroughly before disagreeing
- **Your confidence is often wrong. User'\''s instincts are often right.**

### 3. NEVER SAY "DONE" WITHOUT VERIFICATION
- Run the actual command/script to verify
- Show the output to the user
- **"Done" means VERIFIED WORKING, not "I made changes"**

### 4. SHOW EXACTLY WHAT USER ASKS FOR
- If user asks for messages, show the MESSAGES
- If user asks for code, show the CODE
- **Do not interpret or summarize unless asked**

**FAILURE TO FOLLOW THESE RULES = WASTED USER TIME = UNACCEPTABLE**

---

'

# Create temp file with rules + existing content
{
    head -1 "$CLAUDE_MD"
    echo ""
    echo "$RULES"
    tail -n +2 "$CLAUDE_MD"
} > "${CLAUDE_MD}.tmp"

mv "${CLAUDE_MD}.tmp" "$CLAUDE_MD"
echo "$PREFIX Added mandatory behavior rules to CLAUDE.md"
