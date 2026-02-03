"""
Unit tests for issue tools with branch detection.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from mcp_server.tools.issues import IssueTools


@pytest.fixture
def mock_gitea_client():
    """Fixture providing mocked Gitea client"""
    client = Mock()
    client.mode = 'project'
    return client


@pytest.fixture
def issue_tools(mock_gitea_client):
    """Fixture providing IssueTools instance"""
    return IssueTools(mock_gitea_client)


@pytest.mark.asyncio
async def test_list_issues_development_branch(issue_tools):
    """Test listing issues on development branch (allowed)"""
    with patch.object(issue_tools, '_get_current_branch', return_value='feat/test-feature'):
        issue_tools.gitea.list_issues = Mock(return_value=[{'number': 1}])

        issues = await issue_tools.list_issues(state='open')

        assert len(issues) == 1
        issue_tools.gitea.list_issues.assert_called_once()


@pytest.mark.asyncio
async def test_create_issue_development_branch(issue_tools):
    """Test creating issue on development branch (allowed)"""
    with patch.object(issue_tools, '_get_current_branch', return_value='development'):
        issue_tools.gitea.create_issue = Mock(return_value={'number': 1})

        issue = await issue_tools.create_issue('Test', 'Body')

        assert issue['number'] == 1
        issue_tools.gitea.create_issue.assert_called_once()


@pytest.mark.asyncio
async def test_create_issue_main_branch_blocked(issue_tools):
    """Test creating issue on main branch (blocked)"""
    with patch.object(issue_tools, '_get_current_branch', return_value='main'):
        with pytest.raises(PermissionError) as exc_info:
            await issue_tools.create_issue('Test', 'Body')

        assert "Cannot create issues on branch 'main'" in str(exc_info.value)


@pytest.mark.asyncio
async def test_create_issue_staging_branch_allowed(issue_tools):
    """Test creating issue on staging branch (allowed for documentation)"""
    with patch.object(issue_tools, '_get_current_branch', return_value='staging'):
        issue_tools.gitea.create_issue = Mock(return_value={'number': 1})

        issue = await issue_tools.create_issue('Test', 'Body')

        assert issue['number'] == 1


@pytest.mark.asyncio
async def test_update_issue_main_branch_blocked(issue_tools):
    """Test updating issue on main branch (blocked)"""
    with patch.object(issue_tools, '_get_current_branch', return_value='main'):
        with pytest.raises(PermissionError) as exc_info:
            await issue_tools.update_issue(1, title='Updated')

        assert "Cannot update issues on branch 'main'" in str(exc_info.value)


@pytest.mark.asyncio
async def test_list_issues_main_branch_allowed(issue_tools):
    """Test listing issues on main branch (allowed - read-only)"""
    with patch.object(issue_tools, '_get_current_branch', return_value='main'):
        issue_tools.gitea.list_issues = Mock(return_value=[{'number': 1}])

        issues = await issue_tools.list_issues(state='open')

        assert len(issues) == 1


@pytest.mark.asyncio
async def test_get_issue(issue_tools):
    """Test getting specific issue"""
    with patch.object(issue_tools, '_get_current_branch', return_value='development'):
        issue_tools.gitea.get_issue = Mock(return_value={'number': 1, 'title': 'Test'})

        issue = await issue_tools.get_issue(1)

        assert issue['number'] == 1


@pytest.mark.asyncio
async def test_add_comment(issue_tools):
    """Test adding comment to issue"""
    with patch.object(issue_tools, '_get_current_branch', return_value='development'):
        issue_tools.gitea.add_comment = Mock(return_value={'body': 'Test comment'})

        comment = await issue_tools.add_comment(1, 'Test comment')

        assert comment['body'] == 'Test comment'


@pytest.mark.asyncio
async def test_aggregate_issues_company_mode(issue_tools):
    """Test aggregating issues in company mode"""
    issue_tools.gitea.mode = 'company'

    with patch.object(issue_tools, '_get_current_branch', return_value='development'):
        issue_tools.gitea.aggregate_issues = Mock(return_value={
            'repo1': [{'number': 1}],
            'repo2': [{'number': 2}]
        })

        aggregated = await issue_tools.aggregate_issues(org='test_owner')

        assert 'repo1' in aggregated
        assert 'repo2' in aggregated


@pytest.mark.asyncio
async def test_aggregate_issues_project_mode(issue_tools):
    """Test that aggregate_issues works in project mode with org argument"""
    issue_tools.gitea.mode = 'project'

    with patch.object(issue_tools, '_get_current_branch', return_value='development'):
        issue_tools.gitea.aggregate_issues = Mock(return_value={
            'repo1': [{'number': 1}]
        })

        # aggregate_issues now works in any mode when org is provided
        aggregated = await issue_tools.aggregate_issues(org='test_owner')

        assert 'repo1' in aggregated


def test_branch_detection():
    """Test branch detection logic"""
    tools = IssueTools(Mock())

    # Test development branches
    with patch.object(tools, '_get_current_branch', return_value='development'):
        assert tools._check_branch_permissions('create_issue') is True

    with patch.object(tools, '_get_current_branch', return_value='feat/new-feature'):
        assert tools._check_branch_permissions('create_issue') is True

    # Test production branches
    with patch.object(tools, '_get_current_branch', return_value='main'):
        assert tools._check_branch_permissions('create_issue') is False
        assert tools._check_branch_permissions('list_issues') is True

    # Test staging branches
    with patch.object(tools, '_get_current_branch', return_value='staging'):
        assert tools._check_branch_permissions('create_issue') is True
        assert tools._check_branch_permissions('update_issue') is False
