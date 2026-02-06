---
name: test e2e
description: Generate end-to-end test scenarios with page object models and user flows
---

# /test e2e

Generate end-to-end test scenarios for web applications or API workflows.

## Visual Output

```
+----------------------------------------------------------------------+
|  TEST-PILOT - E2E Tests                                               |
+----------------------------------------------------------------------+
```

## Usage

```
/test e2e <target> [--framework=playwright|cypress] [--flow=<user-flow>]
```

**Target:** Application area, URL path, or feature name
**Framework:** E2E framework (auto-detected if not specified)
**Flow:** Specific user flow to test (e.g., "login", "checkout", "signup")

## Skills to Load

- skills/test-patterns.md

## Process

1. **Analyze Application**
   - Detect E2E framework from config files
   - Identify routes/pages from router configuration
   - Map user-facing features and critical paths
   - Detect authentication requirements

2. **Design Test Scenarios**
   - Map user journeys (happy path first)
   - Identify critical business flows:
     - Authentication (login, logout, password reset)
     - Data creation (forms, uploads, submissions)
     - Navigation (routing, deep links, breadcrumbs)
     - Error states (404, network failures, validation)
   - Define preconditions and test data needs

3. **Generate Page Objects**
   - Create page object classes for each page/component
   - Encapsulate selectors and interactions
   - Keep assertions in test files, not page objects
   - Use data-testid attributes where possible

4. **Write Test Files**
   - One test file per user flow or feature area
   - Include setup (authentication, test data) and teardown (cleanup)
   - Use descriptive test names that read as user stories
   - Add retry logic for flaky network operations
   - Include screenshot capture on failure

5. **Verify**
   - Check selectors reference valid elements
   - Confirm test data setup is complete
   - Validate timeout values are reasonable

## Output Format

```
## E2E Tests: Login Flow

### Page Objects Created
- pages/LoginPage.ts — login form interactions
- pages/DashboardPage.ts — post-login verification

### Test Scenarios (5)
1. test_successful_login_redirects_to_dashboard
2. test_invalid_credentials_shows_error
3. test_empty_form_shows_validation
4. test_remember_me_persists_session
5. test_locked_account_shows_message

### Test Data Requirements
- Valid user credentials (use test seed)
- Locked account fixture
```
