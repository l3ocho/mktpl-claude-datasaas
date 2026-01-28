# Confidence Scoring for PR Review

## Purpose

Confidence scoring ensures that review findings are calibrated and actionable. By filtering out low-confidence findings, we reduce noise and focus reviewer attention on real issues.

## Score Ranges

| Range | Label | Meaning | Action |
|-------|-------|---------|--------|
| 0.9 - 1.0 | HIGH | Definite issue | Must address |
| 0.7 - 0.89 | MEDIUM | Likely issue | Should address |
| 0.5 - 0.69 | LOW | Possible concern | Consider addressing |
| < 0.5 | SUPPRESSED | Uncertain | Don't report |

## Scoring Factors

### Positive Factors (Increase Confidence)

| Factor | Impact |
|--------|--------|
| Clear data flow from source to sink | +0.3 |
| Pattern matches known vulnerability | +0.2 |
| No intervening validation visible | +0.2 |
| Matches OWASP Top 10 | +0.15 |
| Found in security-sensitive context | +0.1 |

### Negative Factors (Decrease Confidence)

| Factor | Impact |
|--------|--------|
| Validation might exist elsewhere | -0.2 |
| Depends on runtime configuration | -0.15 |
| Pattern is common but often safe | -0.15 |
| Requires multiple conditions to exploit | -0.1 |
| Theoretical impact only | -0.1 |

## Calibration Guidelines

### Security Issues

Base confidence by pattern:
- SQL string concatenation with user input: 0.95
- Hardcoded credentials: 0.9
- Missing auth check: 0.8
- Generic error exposure: 0.6
- Missing rate limiting: 0.5

### Performance Issues

Base confidence by pattern:
- Clear N+1 in loop: 0.9
- SELECT * on large table: 0.7
- Missing index on filtered column: 0.6
- Suboptimal algorithm: 0.5

### Maintainability Issues

Base confidence by pattern:
- Function >100 lines: 0.8
- Deep nesting >4 levels: 0.75
- Duplicate code blocks: 0.7
- Unclear naming: 0.6
- Minor style issues: 0.3 (suppress)

### Test Coverage

Base confidence by pattern:
- No test file for new module: 0.9
- Security function untested: 0.85
- Edge case not covered: 0.6
- Simple getter untested: 0.3 (suppress)

## Threshold Configuration

The default threshold is 0.7 (showing MEDIUM and HIGH confidence findings). This can be adjusted:

```bash
PR_REVIEW_CONFIDENCE_THRESHOLD=0.9  # Only definite issues (HIGH)
PR_REVIEW_CONFIDENCE_THRESHOLD=0.7  # Likely issues and above (MEDIUM+HIGH) - default
PR_REVIEW_CONFIDENCE_THRESHOLD=0.5  # Include possible concerns (LOW+)
PR_REVIEW_CONFIDENCE_THRESHOLD=0.3  # Include more speculative
```

## Example Scoring

### High Confidence (0.95)

```javascript
// Clear SQL injection
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
```

- User input (req.params.id): +0.3
- Direct to SQL query: +0.3
- No visible validation: +0.2
- Matches OWASP Top 10: +0.15
- **Total: 0.95**

### Medium Confidence (0.72)

```javascript
// Possible performance issue
users.forEach(async (user) => {
  const orders = await db.orders.find({ userId: user.id });
});
```

- Loop with query: +0.3
- Pattern matches N+1: +0.2
- But might be small dataset: -0.15
- Could have caching: -0.1
- **Total: 0.72**

### Low Confidence (0.55)

```javascript
// Maybe too complex?
function processOrder(order, user, items, discounts, shipping) {
  // 60 lines of logic
}
```

- Function is long: +0.2
- Many parameters: +0.15
- But might be intentional: -0.1
- Could be refactored later: -0.1
- **Total: 0.55**

### Suppressed (0.35)

```javascript
// Minor style preference
const x = foo ? bar : baz;
```

- Ternary could be if/else: +0.1
- Very common pattern: -0.2
- No real impact: -0.1
- Style preference: -0.1
- **Total: 0.35** (suppressed)
