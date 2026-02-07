---
name: test run
description: Run tests with formatted output, filtering, and failure analysis
---

# /test run

Execute tests with structured output and intelligent failure analysis.

## Visual Output

```
+----------------------------------------------------------------------+
|  TEST-PILOT - Run Tests                                               |
+----------------------------------------------------------------------+
```

## Usage

```
/test run [<target>] [--type=unit|integration|e2e|all] [--verbose] [--failfast]
```

**Target:** File, directory, test name pattern, or marker/tag
**Type:** Test category to run (defaults to unit)
**Verbose:** Show full output including passing tests
**Failfast:** Stop on first failure

## Skills to Load

- skills/framework-detection.md

## Process

1. **Detect Test Runner**
   - Identify framework from project configuration
   - Build appropriate command:
     - pytest: `pytest <target> -v --tb=short`
     - Jest: `npx jest <target> --verbose`
     - Vitest: `npx vitest run <target>`
   - Apply type filter if specified (markers, tags, directories)

2. **Execute Tests**
   - Run the test command
   - Capture stdout, stderr, and exit code
   - Parse test results into structured data

3. **Format Results**
   - Group by status: passed, failed, skipped, errors
   - Show failure details with:
     - Test name and location
     - Assertion message
     - Relevant code snippet
     - Suggested fix if pattern is recognizable

4. **Analyze Failures**
   - Common patterns:
     - Import errors: missing dependency or wrong path
     - Assertion errors: expected vs actual mismatch
     - Timeout errors: slow operation or missing mock
     - Setup errors: missing fixture or database state
   - Suggest corrective action for each failure type

5. **Summary**
   - Total/passed/failed/skipped counts
   - Duration
   - Coverage delta if coverage is enabled

## Output Format

```
## Test Results

### Summary: 45 passed, 2 failed, 1 skipped (12.3s)

### Failures

1. FAIL test_user_login_with_expired_token (tests/test_auth.py:67)
   AssertionError: Expected 401, got 200
   Cause: Token expiry check not applied before validation
   Fix: Verify token_service.is_expired() is called in login handler

2. FAIL test_export_csv_large_dataset (tests/test_export.py:134)
   TimeoutError: Operation timed out after 30s
   Cause: No pagination in export query
   Fix: Add batch processing or mock the database call

### Skipped
- test_redis_cache_eviction — requires Redis (marker: @needs_redis)
```
