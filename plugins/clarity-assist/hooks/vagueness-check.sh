#!/bin/bash
# clarity-assist vagueness detection hook
# Analyzes user prompts for vagueness and suggests /clarity-assist when beneficial
# All output MUST have [clarity-assist] prefix
# This is a NON-BLOCKING hook - always exits 0

PREFIX="[clarity-assist]"

# Check if auto-suggest is enabled (default: true)
AUTO_SUGGEST="${CLARITY_ASSIST_AUTO_SUGGEST:-true}"
if [[ "$AUTO_SUGGEST" != "true" ]]; then
    exit 0
fi

# Threshold for vagueness score (default: 0.6)
THRESHOLD="${CLARITY_ASSIST_VAGUENESS_THRESHOLD:-0.6}"

# Read user prompt from stdin
PROMPT=""
if [[ -t 0 ]]; then
    # No stdin available
    exit 0
else
    PROMPT=$(cat)
fi

# Skip empty prompts
if [[ -z "$PROMPT" ]]; then
    exit 0
fi

# Skip if prompt is a command (starts with /)
if [[ "$PROMPT" =~ ^[[:space:]]*/[a-zA-Z] ]]; then
    exit 0
fi

# Skip if prompt mentions specific files or paths
if [[ "$PROMPT" =~ \.(py|js|ts|sh|md|json|yaml|yml|txt|css|html|go|rs|java|c|cpp|h)([[:space:]]|$|[^a-zA-Z]) ]] || \
   [[ "$PROMPT" =~ [/\\][a-zA-Z0-9_-]+[/\\] ]] || \
   [[ "$PROMPT" =~ (src|lib|test|docs|plugins|hooks|commands)/ ]]; then
    exit 0
fi

# Initialize vagueness score
SCORE=0

# Count words in the prompt
WORD_COUNT=$(echo "$PROMPT" | wc -w | tr -d ' ')

# ============================================================================
# Vagueness Signal Detection
# ============================================================================

# Signal 1: Very short prompts (< 10 words) are often vague
if [[ "$WORD_COUNT" -lt 10 ]]; then
    # But very short specific commands are OK
    if [[ "$WORD_COUNT" -lt 3 ]]; then
        # Extremely short - probably intentional or a command
        :
    else
        SCORE=$(echo "$SCORE + 0.3" | bc)
    fi
fi

# Signal 2: Vague action phrases (no specific outcome)
VAGUE_ACTIONS=(
    "help me"
    "help with"
    "do something"
    "work on"
    "look at"
    "check this"
    "fix it"
    "fix this"
    "make it better"
    "make this better"
    "improve it"
    "improve this"
    "update this"
    "update it"
    "change it"
    "change this"
    "can you"
    "could you"
    "would you"
    "please help"
)

PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

for phrase in "${VAGUE_ACTIONS[@]}"; do
    if [[ "$PROMPT_LOWER" == *"$phrase"* ]]; then
        SCORE=$(echo "$SCORE + 0.2" | bc)
        break
    fi
done

# Signal 3: Ambiguous scope indicators
AMBIGUOUS_SCOPE=(
    "somehow"
    "something"
    "somewhere"
    "anything"
    "whatever"
    "stuff"
    "things"
    "etc"
    "and so on"
)

for word in "${AMBIGUOUS_SCOPE[@]}"; do
    if [[ "$PROMPT_LOWER" == *"$word"* ]]; then
        SCORE=$(echo "$SCORE + 0.15" | bc)
        break
    fi
done

# Signal 4: Missing context indicators (no reference to what/where)
# Check if prompt lacks specificity markers
HAS_SPECIFICS=false

# Specific technical terms suggest clarity
SPECIFIC_MARKERS=(
    "function"
    "class"
    "method"
    "variable"
    "error"
    "bug"
    "test"
    "api"
    "endpoint"
    "database"
    "query"
    "component"
    "module"
    "service"
    "config"
    "install"
    "deploy"
    "build"
    "run"
    "execute"
    "create"
    "delete"
    "add"
    "remove"
    "implement"
    "refactor"
    "migrate"
    "upgrade"
    "debug"
    "log"
    "exception"
    "stack"
    "memory"
    "performance"
    "security"
    "auth"
    "token"
    "session"
    "route"
    "controller"
    "model"
    "view"
    "template"
    "schema"
    "migration"
    "commit"
    "branch"
    "merge"
    "pull"
    "push"
)

for marker in "${SPECIFIC_MARKERS[@]}"; do
    if [[ "$PROMPT_LOWER" == *"$marker"* ]]; then
        HAS_SPECIFICS=true
        break
    fi
done

if [[ "$HAS_SPECIFICS" == false ]] && [[ "$WORD_COUNT" -gt 3 ]]; then
    SCORE=$(echo "$SCORE + 0.2" | bc)
fi

# Signal 5: Question without context
if [[ "$PROMPT" =~ \?$ ]] && [[ "$WORD_COUNT" -lt 8 ]]; then
    # Short questions without specifics are often vague
    if [[ "$HAS_SPECIFICS" == false ]]; then
        SCORE=$(echo "$SCORE + 0.15" | bc)
    fi
fi

# Cap score at 1.0
if (( $(echo "$SCORE > 1.0" | bc -l) )); then
    SCORE="1.0"
fi

# ============================================================================
# Output suggestion if score exceeds threshold
# ============================================================================

# Compare score to threshold using bc
if (( $(echo "$SCORE >= $THRESHOLD" | bc -l) )); then
    # Format score as percentage for display
    SCORE_PCT=$(echo "$SCORE * 100" | bc | cut -d'.' -f1)

    # Gentle, non-blocking suggestion
    echo "$PREFIX Your prompt could benefit from more clarity."
    echo "$PREFIX Consider running /clarity-assist to refine your request."
    echo "$PREFIX (Vagueness score: ${SCORE_PCT}% - this is a suggestion, not a block)"
fi

# Always exit 0 - this hook is non-blocking
exit 0
