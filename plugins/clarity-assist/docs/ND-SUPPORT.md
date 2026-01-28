# Neurodivergent Support in clarity-assist

This document describes how clarity-assist is designed to support users with neurodivergent traits, including ADHD, autism, anxiety, and other conditions that affect executive function, sensory processing, or cognitive style.

## Overview

### Purpose

clarity-assist exists to help all users transform vague or incomplete requests into clear, actionable specifications. For neurodivergent users specifically, it addresses common challenges:

- **Executive function difficulties** - Breaking down complex tasks, getting started, managing scope
- **Working memory limitations** - Keeping track of context across long conversations
- **Decision fatigue** - Facing too many open-ended choices
- **Processing style differences** - Preferring structured, predictable interactions
- **Anxiety around uncertainty** - Needing clear expectations and explicit confirmation

### Philosophy

Our design philosophy centers on three principles:

1. **Reduce cognitive load** - Never force the user to hold too much in their head at once
2. **Provide structure** - Use consistent, predictable patterns for all interactions
3. **Respect different communication styles** - Accommodate rather than assume one "right" way to think

## Features for ND Users

### 1. Reduced Cognitive Load

**Prompt Simplification**
- The 4-D methodology (Deconstruct, Diagnose, Develop, Deliver) breaks down complex requests into manageable phases
- Users never need to specify everything upfront - clarification happens incrementally

**Task Breakdown**
- Large requests are decomposed into explicit components
- Dependencies and relationships are surfaced rather than left implicit
- Scope boundaries are clearly defined (in-scope vs. out-of-scope)

### 2. Structured Output

**Consistent Formatting**
- Every clarification session produces the same structured specification:
  - Summary (1-2 sentences)
  - Scope (In/Out)
  - Requirements table (numbered, prioritized)
  - Assumptions list
- This predictability reduces the mental effort of parsing responses

**Predictable Patterns**
- Questions always follow the same format
- Progress summaries appear at regular intervals
- Escalation (simple to complex) is always offered, never forced

**Bulleted Lists Over Prose**
- Requirements are presented as scannable lists, not paragraphs
- Options are numbered for easy reference
- Key information is highlighted with bold labels

### 3. Customizable Verbosity

**Detail Levels**
- `/clarify` - Full methodology for complex requests (more thorough, more questions)
- `/quick-clarify` - Rapid mode for simple disambiguation (fewer questions, faster)

**User Control**
- Users can always say "that's enough detail" to end questioning early
- The plugin offers to break sessions into smaller parts
- "Good enough for now" is explicitly validated as an acceptable outcome

### 4. Vagueness Detection

The `UserPromptSubmit` hook automatically detects prompts that might benefit from clarification and gently suggests using `/clarify`.

**Detection Signals**
- Short prompts (< 10 words) without specific technical terms
- Vague action phrases: "help me", "fix this", "make it better"
- Ambiguous scope words: "somehow", "something", "stuff", "etc."
- Open questions without context

**Non-Blocking Approach**
- The hook never prevents you from proceeding
- It provides a suggestion with a vagueness score (percentage)
- You can disable auto-suggestions entirely via environment variable

### 5. Focus Aids

**Task Prioritization**
- Requirements are tagged as Must/Should/Could/Won't (MoSCoW)
- Critical items are separated from nice-to-haves
- Scope creep is explicitly called out and deferred

**Context Switching Warnings**
- When questions touch multiple areas, the plugin acknowledges the complexity
- Offers to focus on one aspect at a time
- Summarizes frequently to rebuild context after interruptions

## How It Works

### The UserPromptSubmit Hook

When you submit a prompt, the vagueness detection hook (`hooks/vagueness-check.sh`) runs automatically:

```
User submits prompt
       |
       v
Hook reads prompt from stdin
       |
       v
Skip if: empty, starts with /, or contains file paths
       |
       v
Calculate vagueness score (0.0 - 1.0)
  - Short prompts: +0.3
  - Vague action phrases: +0.2
  - Ambiguous scope words: +0.15
  - Missing technical specifics: +0.2
  - Short questions without context: +0.15
       |
       v
If score >= threshold (default 0.6):
  - Output gentle suggestion with [clarity-assist] prefix
  - Show vagueness percentage
       |
       v
Exit 0 (always non-blocking)
```

### Example Hook Output

```
[clarity-assist] Your prompt could benefit from more clarity.
[clarity-assist] Consider running /clarity-assist to refine your request.
[clarity-assist] (Vagueness score: 65% - this is a suggestion, not a block)
```

### The 4-D Methodology

| Phase | What Happens | ND Benefit |
|-------|--------------|------------|
| **Deconstruct** | Break request into components | Shows the full picture without overwhelming |
| **Diagnose** | Identify gaps and conflicts | Surfaces hidden assumptions |
| **Develop** | Ask structured questions | Option-based, chunked, contextual |
| **Deliver** | Produce specification | Consistent, scannable format |

## Usage Examples

### Before: Vague Request

```
User: Make the app faster
```

This triggers vagueness detection because:
- Short (4 words)
- Vague action ("make")
- No specific technical context
- No measurable outcome

### After: Clarified with /clarify

```
User: /clarify Make the app faster

Claude: Let me help clarify what kind of performance improvements you're looking for.

**What type of slowness are you experiencing?**
1. Initial page load takes too long
2. Interactions feel sluggish (clicking, typing)
3. API calls are slow
4. All of the above
5. Other

[I'm asking because each has very different solutions]
```

```
User: 1

Claude: Initial page load - got it.

**What's an acceptable load time for you?**
1. Under 1 second (aggressive)
2. Under 2 seconds (standard)
3. Under 3 seconds (relaxed)
4. I don't have a specific target

[This helps me know whether to suggest quick wins or a major optimization effort]
```

After 2-3 more questions, the user receives:

```markdown
## Clarified Request

### Summary
Optimize initial page load time to under 2 seconds by addressing bundle size and initial render blocking resources.

### Scope
**In Scope:**
- Bundle analysis and splitting
- Lazy loading non-critical components
- Image optimization
- CSS/JS minification check

**Out of Scope:**
- Backend API optimization
- Database query performance
- CDN setup

### Requirements
| # | Requirement | Priority | Notes |
|---|-------------|----------|-------|
| 1 | Page loads in < 2s on 4G | Must | Measured via Lighthouse |
| 2 | Largest contentful paint < 1.5s | Should | Core Web Vital |
| 3 | No layout shift after load | Should | CLS < 0.1 |

### Assumptions
- Current load time is > 3 seconds (based on "too long" description)
- Target browsers: modern evergreen (Chrome, Firefox, Safari)
- Build tooling already configured (webpack/vite)
```

### Common Patterns Detected

| Pattern | Example | What It Triggers |
|---------|---------|------------------|
| Missing context | "Fix the bug" | "Which bug? In which file or feature?" |
| Ambiguous scope | "Update the user stuff" | "What specifically needs updating?" |
| Unclear goals | "Make it better" | "Better in what way? Faster? Cleaner? More features?" |
| Implicit knowledge | "Do it like last time" | "I don't have context from previous sessions" |
| Conflicting requests | "Keep it simple but add everything" | "Which matters more: simplicity or completeness?" |

### Quick-Clarify Example

For simpler requests that just need minor disambiguation:

```
User: /quick-clarify Add a delete button to the user list

Claude: I'll add a delete button to each row in the user list.

**Should deletion require confirmation?**
1. Yes - show confirmation dialog (Recommended)
2. No - delete immediately
3. Soft delete - mark as deleted but keep data

[Asking because accidental deletions can be problematic]
```

```
User: 1

Claude: Got it. I'll implement a delete button with confirmation dialog. Starting now.
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLARITY_ASSIST_AUTO_SUGGEST` | `true` | Enable/disable automatic vagueness detection |
| `CLARITY_ASSIST_VAGUENESS_THRESHOLD` | `0.6` | Score threshold to trigger suggestion (0.0-1.0) |

### Disabling Auto-Suggestions

If you find the vagueness detection unhelpful, disable it in your shell profile or `.env`:

```bash
export CLARITY_ASSIST_AUTO_SUGGEST=false
```

### Adjusting Sensitivity

To make detection more or less sensitive:

```bash
# More sensitive (suggests more often)
export CLARITY_ASSIST_VAGUENESS_THRESHOLD=0.4

# Less sensitive (only very vague prompts)
export CLARITY_ASSIST_VAGUENESS_THRESHOLD=0.8
```

## Tips for ND Users

### If You're Feeling Overwhelmed

- Use `/quick-clarify` instead of `/clarify` for faster interactions
- Say "let's focus on just one thing" to narrow scope
- Ask to "pause and summarize" at any point
- It's OK to say "I don't know" - the plugin will offer concrete alternatives

### If You Have Executive Function Challenges

- Start with `/clarify` even for tasks you think are simple - it helps with planning
- The structured specification can serve as a checklist
- Use the scope boundaries to prevent scope creep

### If You Prefer Detailed Structure

- The 4-D methodology provides a predictable framework
- All output follows consistent formatting
- Questions always offer numbered options

### If You Have Anxiety About Getting It Right

- The plugin validates "good enough for now" as acceptable
- You can always revisit and change earlier answers
- Assumptions are explicitly listed - nothing is hidden

## Accessibility Notes

- All output uses standard markdown that works with screen readers
- No time pressure - take as long as you need between responses
- Questions are designed to be answerable without deep context retrieval
- Visual patterns (bold, bullets, tables) create scannable structure

## Feedback

If you have suggestions for improving neurodivergent support in clarity-assist, please open an issue at:

https://gitea.hotserv.cloud/personal-projects/leo-claude-mktplace/issues

Include the label `clarity-assist` and describe:
- What challenge you faced
- What would have helped
- Any specific accommodations you'd like to see
