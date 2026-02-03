# Changelog

All notable changes to the Gitea MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-02-03

### Added
- Pull request tools (7 tools):
  - `list_pull_requests` - List PRs from repository
  - `get_pull_request` - Get specific PR details
  - `get_pr_diff` - Get PR diff content
  - `get_pr_comments` - Get comments on a PR
  - `create_pr_review` - Create PR review (approve/request changes/comment)
  - `add_pr_comment` - Add comment to PR
  - `create_pull_request` - Create new pull request
- Label creation tools (3 tools):
  - `create_label` - Create repo-level label
  - `create_org_label` - Create organization-level label
  - `create_label_smart` - Auto-detect org vs repo for label creation
- Validation tools (2 tools):
  - `validate_repo_org` - Check if repo belongs to organization
  - `get_branch_protection` - Get branch protection rules

### Changed
- Total tools increased from 20 to 36
- Updated test suite to 64 tests (was 42)

### Fixed
- Test fixtures updated to use `owner/repo` format
- Fixed aggregate_issues tests to pass required `org` argument

## [1.2.0] - 2026-01-28

### Added
- Milestone management tools (5 tools):
  - `list_milestones` - List all milestones
  - `get_milestone` - Get specific milestone
  - `create_milestone` - Create new milestone
  - `update_milestone` - Update existing milestone
  - `delete_milestone` - Delete a milestone
- Issue dependency tools (4 tools):
  - `list_issue_dependencies` - List blocking issues
  - `create_issue_dependency` - Create dependency between issues
  - `remove_issue_dependency` - Remove dependency
  - `get_execution_order` - Calculate parallelizable execution order

## [1.1.0] - 2026-01-21

### Added
- Wiki and lessons learned tools (7 tools):
  - `list_wiki_pages` - List all wiki pages
  - `get_wiki_page` - Get specific wiki page content
  - `create_wiki_page` - Create new wiki page
  - `update_wiki_page` - Update existing wiki page
  - `create_lesson` - Create lessons learned entry
  - `search_lessons` - Search lessons by query/tags
  - `allocate_rfc_number` - Get next available RFC number
- Automatic git remote URL detection for repository configuration
- Support for SSH, HTTPS, and HTTP git URL formats

### Changed
- Configuration now uses `owner/repo` format exclusively
- Removed separate `GITEA_OWNER` configuration (now derived from repo path)

## [1.0.0] - 2025-01-06

### Added
- Initial release with 8 core tools:
  - `list_issues` - List issues from repository
  - `get_issue` - Get specific issue details
  - `create_issue` - Create new issue with labels
  - `update_issue` - Update existing issue
  - `add_comment` - Add comment to issue
  - `get_labels` - Get all labels (org + repo)
  - `suggest_labels` - Intelligent label suggestion
  - `aggregate_issues` - Cross-repository issue aggregation (PMO mode)
- Hybrid configuration system (system + project level)
- Branch-aware security model
- Mode detection (project vs company/PMO)
- 42 unit tests with mocks
- Comprehensive documentation

[Unreleased]: https://github.com/owner/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/owner/repo/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/owner/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/owner/repo/releases/tag/v1.0.0
