"""
Unit tests for Gitea API client.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from mcp_server.gitea_client import GiteaClient


@pytest.fixture
def mock_config():
    """Fixture providing mocked configuration"""
    with patch('mcp_server.gitea_client.GiteaConfig') as mock_cfg:
        mock_instance = mock_cfg.return_value
        mock_instance.load.return_value = {
            'api_url': 'https://test.com/api/v1',
            'api_token': 'test_token',
            'owner': 'test_owner',
            'repo': 'test_repo',
            'mode': 'project'
        }
        yield mock_cfg


@pytest.fixture
def gitea_client(mock_config):
    """Fixture providing GiteaClient instance with mocked config"""
    return GiteaClient()


def test_client_initialization(gitea_client):
    """Test client initializes with correct configuration"""
    assert gitea_client.base_url == 'https://test.com/api/v1'
    assert gitea_client.token == 'test_token'
    assert gitea_client.owner == 'test_owner'
    assert gitea_client.repo == 'test_repo'
    assert gitea_client.mode == 'project'
    assert 'Authorization' in gitea_client.session.headers
    assert gitea_client.session.headers['Authorization'] == 'token test_token'


def test_list_issues(gitea_client):
    """Test listing issues"""
    mock_response = Mock()
    mock_response.json.return_value = [
        {'number': 1, 'title': 'Test Issue 1'},
        {'number': 2, 'title': 'Test Issue 2'}
    ]
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'get', return_value=mock_response):
        issues = gitea_client.list_issues(state='open')

        assert len(issues) == 2
        assert issues[0]['title'] == 'Test Issue 1'
        gitea_client.session.get.assert_called_once()


def test_list_issues_with_labels(gitea_client):
    """Test listing issues with label filter"""
    mock_response = Mock()
    mock_response.json.return_value = [{'number': 1, 'title': 'Bug Issue'}]
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'get', return_value=mock_response):
        issues = gitea_client.list_issues(state='open', labels=['Type/Bug'])

        gitea_client.session.get.assert_called_once()
        call_args = gitea_client.session.get.call_args
        assert call_args[1]['params']['labels'] == 'Type/Bug'


def test_get_issue(gitea_client):
    """Test getting specific issue"""
    mock_response = Mock()
    mock_response.json.return_value = {'number': 1, 'title': 'Test Issue'}
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'get', return_value=mock_response):
        issue = gitea_client.get_issue(1)

        assert issue['number'] == 1
        assert issue['title'] == 'Test Issue'


def test_create_issue(gitea_client):
    """Test creating new issue"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'number': 1,
        'title': 'New Issue',
        'body': 'Issue body'
    }
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'post', return_value=mock_response):
        issue = gitea_client.create_issue(
            title='New Issue',
            body='Issue body',
            labels=['Type/Bug']
        )

        assert issue['title'] == 'New Issue'
        gitea_client.session.post.assert_called_once()


def test_update_issue(gitea_client):
    """Test updating existing issue"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'number': 1,
        'title': 'Updated Issue'
    }
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'patch', return_value=mock_response):
        issue = gitea_client.update_issue(
            issue_number=1,
            title='Updated Issue'
        )

        assert issue['title'] == 'Updated Issue'
        gitea_client.session.patch.assert_called_once()


def test_add_comment(gitea_client):
    """Test adding comment to issue"""
    mock_response = Mock()
    mock_response.json.return_value = {'body': 'Test comment'}
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'post', return_value=mock_response):
        comment = gitea_client.add_comment(1, 'Test comment')

        assert comment['body'] == 'Test comment'
        gitea_client.session.post.assert_called_once()


def test_get_labels(gitea_client):
    """Test getting repository labels"""
    mock_response = Mock()
    mock_response.json.return_value = [
        {'name': 'Type/Bug'},
        {'name': 'Priority/High'}
    ]
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'get', return_value=mock_response):
        labels = gitea_client.get_labels()

        assert len(labels) == 2
        assert labels[0]['name'] == 'Type/Bug'


def test_get_org_labels(gitea_client):
    """Test getting organization labels"""
    mock_response = Mock()
    mock_response.json.return_value = [
        {'name': 'Type/Bug'},
        {'name': 'Type/Feature'}
    ]
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'get', return_value=mock_response):
        labels = gitea_client.get_org_labels()

        assert len(labels) == 2


def test_list_repos(gitea_client):
    """Test listing organization repositories (PMO mode)"""
    mock_response = Mock()
    mock_response.json.return_value = [
        {'name': 'repo1'},
        {'name': 'repo2'}
    ]
    mock_response.raise_for_status = Mock()

    with patch.object(gitea_client.session, 'get', return_value=mock_response):
        repos = gitea_client.list_repos()

        assert len(repos) == 2
        assert repos[0]['name'] == 'repo1'


def test_aggregate_issues(gitea_client):
    """Test aggregating issues across repositories (PMO mode)"""
    # Mock list_repos
    gitea_client.list_repos = Mock(return_value=[
        {'name': 'repo1'},
        {'name': 'repo2'}
    ])

    # Mock list_issues
    gitea_client.list_issues = Mock(side_effect=[
        [{'number': 1, 'title': 'Issue 1'}],  # repo1
        [{'number': 2, 'title': 'Issue 2'}]   # repo2
    ])

    aggregated = gitea_client.aggregate_issues(state='open')

    assert 'repo1' in aggregated
    assert 'repo2' in aggregated
    assert len(aggregated['repo1']) == 1
    assert len(aggregated['repo2']) == 1


def test_no_repo_specified_error(gitea_client):
    """Test error when repository not specified"""
    # Create client without repo
    with patch('mcp_server.gitea_client.GiteaConfig') as mock_cfg:
        mock_instance = mock_cfg.return_value
        mock_instance.load.return_value = {
            'api_url': 'https://test.com/api/v1',
            'api_token': 'test_token',
            'owner': 'test_owner',
            'repo': None,  # No repo
            'mode': 'company'
        }
        client = GiteaClient()

        with pytest.raises(ValueError) as exc_info:
            client.list_issues()

        assert "Repository not specified" in str(exc_info.value)
