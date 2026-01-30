# CLAUDE.md Optimization Patterns

This skill defines patterns for optimizing CLAUDE.md files.

## Optimization Categories

### Restructure
- Reorder sections by importance (Quick Start near top)
- Group related content together
- Improve header hierarchy
- Add navigation aids (TOC for long files)

### Condense
- Remove redundant explanations
- Convert verbose text to bullet points
- Eliminate duplicate content
- Shorten overly detailed sections

### Enhance
- Add missing essential sections
- **Add Pre-Change Protocol if missing (HIGH PRIORITY)**
- Improve unclear instructions
- Add helpful examples
- Highlight critical rules

### Format
- Standardize header styles (no trailing colons)
- Fix code block formatting (add language tags)
- Align list formatting (consistent markers)
- Improve table layouts

## Scoring Criteria

### Structure (25 points)
- Logical section ordering
- Clear header hierarchy
- Easy navigation
- Appropriate grouping

### Clarity (25 points)
- Clear instructions
- Good examples
- Unambiguous language
- Appropriate detail level

### Completeness (25 points)
- Project overview present
- Quick start commands documented
- Critical rules highlighted
- Key workflows covered
- Pre-Change Protocol present (MANDATORY)

### Conciseness (25 points)
- No unnecessary repetition
- Efficient information density
- Appropriate length for project size
- No generic filler content

## Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Maintenance only |
| 70-89 | Good | Minor improvements |
| 50-69 | Needs Work | Optimization recommended |
| Below 50 | Poor | Major restructuring needed |

## Common Optimizations

### Verbose to Concise
```markdown
# Before (34 lines)
## Running Tests
To run the tests, you first need to make sure you have all the
dependencies installed. The dependencies are listed in requirements.txt.
Once you have installed the dependencies, you can run the tests using
pytest. Pytest will automatically discover all test files...

# After (8 lines)
## Running Tests
```bash
pip install -r requirements.txt  # Install dependencies
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest tests/unit/               # Run specific directory
```
```

### Duplicate Removal
- Keep first occurrence
- Add cross-reference if needed: "See [Section Name] above"

### Header Standardization
```markdown
# Before
## Quick Start:
## Architecture
## Testing:

# After
## Quick Start
## Architecture
## Testing
```

### Code Block Enhancement
```markdown
# Before
```
npm install
npm test
```

# After
```bash
npm install  # Install dependencies
npm test     # Run test suite
```
```

## Safety Features

### Backup Creation
- Always backup before changes
- Store in `.claude/backups/CLAUDE.md.TIMESTAMP`
- Easy restoration if needed

### Preview Mode
- Show all changes before applying
- Use diff format for easy review
- Allow approve/reject per change

### Selective Application
- Can apply individual changes
- Skip specific optimizations
- Iterative refinement supported
