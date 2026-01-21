"""
Unit tests for label tools with suggestion logic.
"""
import pytest
from unittest.mock import Mock, patch
from mcp_server.tools.labels import LabelTools


@pytest.fixture
def mock_gitea_client():
    """Fixture providing mocked Gitea client"""
    client = Mock()
    client.repo = 'test_org/test_repo'
    client.is_org_repo = Mock(return_value=True)
    return client


@pytest.fixture
def label_tools(mock_gitea_client):
    """Fixture providing LabelTools instance"""
    return LabelTools(mock_gitea_client)


@pytest.mark.asyncio
async def test_get_labels(label_tools):
    """Test getting all labels (org + repo)"""
    label_tools.gitea.get_org_labels = Mock(return_value=[
        {'name': 'Type/Bug'},
        {'name': 'Type/Feature'}
    ])
    label_tools.gitea.get_labels = Mock(return_value=[
        {'name': 'Component/Backend'},
        {'name': 'Component/Frontend'}
    ])

    result = await label_tools.get_labels()

    assert len(result['organization']) == 2
    assert len(result['repository']) == 2
    assert result['total_count'] == 4


# ========================================
# LABEL LOOKUP TESTS (NEW)
# ========================================

def test_build_label_lookup_slash_format():
    """Test building label lookup with slash format labels"""
    mock_client = Mock()
    mock_client.repo = 'test/repo'
    tools = LabelTools(mock_client)

    labels = ['Type/Bug', 'Type/Feature', 'Priority/High', 'Priority/Low']
    lookup = tools._build_label_lookup(labels)

    assert 'type' in lookup
    assert 'bug' in lookup['type']
    assert lookup['type']['bug'] == 'Type/Bug'
    assert lookup['type']['feature'] == 'Type/Feature'
    assert 'priority' in lookup
    assert lookup['priority']['high'] == 'Priority/High'


def test_build_label_lookup_colon_space_format():
    """Test building label lookup with colon-space format labels"""
    mock_client = Mock()
    mock_client.repo = 'test/repo'
    tools = LabelTools(mock_client)

    labels = ['Type: Bug', 'Type: Feature', 'Priority: High', 'Effort: M']
    lookup = tools._build_label_lookup(labels)

    assert 'type' in lookup
    assert 'bug' in lookup['type']
    assert lookup['type']['bug'] == 'Type: Bug'
    assert lookup['type']['feature'] == 'Type: Feature'
    assert 'priority' in lookup
    assert lookup['priority']['high'] == 'Priority: High'
    # Test singular "Effort" (not "Efforts")
    assert 'effort' in lookup
    assert lookup['effort']['m'] == 'Effort: M'


def test_build_label_lookup_efforts_normalization():
    """Test that 'Efforts' is normalized to 'effort' for matching"""
    mock_client = Mock()
    mock_client.repo = 'test/repo'
    tools = LabelTools(mock_client)

    labels = ['Efforts/XS', 'Efforts/S', 'Efforts/M']
    lookup = tools._build_label_lookup(labels)

    # 'Efforts' should be normalized to 'effort'
    assert 'effort' in lookup
    assert lookup['effort']['xs'] == 'Efforts/XS'


def test_find_label():
    """Test finding labels from lookup"""
    mock_client = Mock()
    mock_client.repo = 'test/repo'
    tools = LabelTools(mock_client)

    lookup = {
        'type': {'bug': 'Type: Bug', 'feature': 'Type: Feature'},
        'priority': {'high': 'Priority: High', 'low': 'Priority: Low'}
    }

    assert tools._find_label(lookup, 'type', 'bug') == 'Type: Bug'
    assert tools._find_label(lookup, 'priority', 'high') == 'Priority: High'
    assert tools._find_label(lookup, 'type', 'nonexistent') is None
    assert tools._find_label(lookup, 'nonexistent', 'bug') is None


# ========================================
# SUGGEST LABELS WITH DYNAMIC FORMAT TESTS
# ========================================

def _create_tools_with_labels(labels):
    """Helper to create LabelTools with mocked labels"""
    import asyncio
    mock_client = Mock()
    mock_client.repo = 'test/repo'
    mock_client.is_org_repo = Mock(return_value=False)
    mock_client.get_labels = Mock(return_value=[{'name': l} for l in labels])
    return LabelTools(mock_client)


@pytest.mark.asyncio
async def test_suggest_labels_with_slash_format():
    """Test label suggestion with slash format labels"""
    labels = [
        'Type/Bug', 'Type/Feature', 'Type/Refactor',
        'Priority/Critical', 'Priority/High', 'Priority/Medium', 'Priority/Low',
        'Complexity/Simple', 'Complexity/Medium', 'Complexity/Complex',
        'Component/Auth'
    ]
    tools = _create_tools_with_labels(labels)

    context = "Fix critical bug in login authentication"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Bug' in suggestions
    assert 'Priority/Critical' in suggestions
    assert 'Component/Auth' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_with_colon_space_format():
    """Test label suggestion with colon-space format labels"""
    labels = [
        'Type: Bug', 'Type: Feature', 'Type: Refactor',
        'Priority: Critical', 'Priority: High', 'Priority: Medium', 'Priority: Low',
        'Complexity: Simple', 'Complexity: Medium', 'Complexity: Complex',
        'Effort: XS', 'Effort: S', 'Effort: M', 'Effort: L', 'Effort: XL'
    ]
    tools = _create_tools_with_labels(labels)

    context = "Fix critical bug for tiny 1 hour fix"
    suggestions = await tools.suggest_labels(context)

    # Should return colon-space format labels
    assert 'Type: Bug' in suggestions
    assert 'Priority: Critical' in suggestions
    assert 'Effort: XS' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_bug():
    """Test label suggestion for bug context"""
    labels = [
        'Type/Bug', 'Type/Feature',
        'Priority/Critical', 'Priority/High', 'Priority/Medium', 'Priority/Low',
        'Complexity/Simple', 'Complexity/Medium', 'Complexity/Complex',
        'Component/Auth'
    ]
    tools = _create_tools_with_labels(labels)

    context = "Fix critical bug in login authentication"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Bug' in suggestions
    assert 'Priority/Critical' in suggestions
    assert 'Component/Auth' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_feature():
    """Test label suggestion for feature context"""
    labels = ['Type/Feature', 'Priority/Medium', 'Complexity/Medium']
    tools = _create_tools_with_labels(labels)

    context = "Add new feature to implement user dashboard"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Feature' in suggestions
    assert any('Priority' in label for label in suggestions)


@pytest.mark.asyncio
async def test_suggest_labels_refactor():
    """Test label suggestion for refactor context"""
    labels = ['Type/Refactor', 'Priority/Medium', 'Complexity/Medium', 'Component/Backend']
    tools = _create_tools_with_labels(labels)

    context = "Refactor architecture to extract service layer"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Refactor' in suggestions
    assert 'Component/Backend' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_documentation():
    """Test label suggestion for documentation context"""
    labels = ['Type/Documentation', 'Priority/Medium', 'Complexity/Medium', 'Component/API', 'Component/Docs']
    tools = _create_tools_with_labels(labels)

    context = "Update documentation for API endpoints"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Documentation' in suggestions
    assert 'Component/API' in suggestions or 'Component/Docs' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_priority():
    """Test priority detection in suggestions"""
    labels = ['Type/Feature', 'Priority/Critical', 'Priority/High', 'Priority/Medium', 'Priority/Low', 'Complexity/Medium']
    tools = _create_tools_with_labels(labels)

    # Critical priority
    context = "Urgent blocker in production"
    suggestions = await tools.suggest_labels(context)
    assert 'Priority/Critical' in suggestions

    # High priority
    context = "Important feature needed asap"
    suggestions = await tools.suggest_labels(context)
    assert 'Priority/High' in suggestions

    # Low priority
    context = "Nice-to-have optional improvement"
    suggestions = await tools.suggest_labels(context)
    assert 'Priority/Low' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_complexity():
    """Test complexity detection in suggestions"""
    labels = ['Type/Feature', 'Priority/Medium', 'Complexity/Simple', 'Complexity/Medium', 'Complexity/Complex']
    tools = _create_tools_with_labels(labels)

    # Simple complexity
    context = "Simple quick fix for typo"
    suggestions = await tools.suggest_labels(context)
    assert 'Complexity/Simple' in suggestions

    # Complex complexity
    context = "Complex challenging architecture redesign"
    suggestions = await tools.suggest_labels(context)
    assert 'Complexity/Complex' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_efforts():
    """Test efforts detection in suggestions"""
    labels = ['Type/Feature', 'Priority/Medium', 'Complexity/Medium', 'Efforts/XS', 'Efforts/S', 'Efforts/M', 'Efforts/L', 'Efforts/XL']
    tools = _create_tools_with_labels(labels)

    # XS effort
    context = "Tiny fix that takes 1 hour"
    suggestions = await tools.suggest_labels(context)
    assert 'Efforts/XS' in suggestions

    # L effort
    context = "Large feature taking 1 week"
    suggestions = await tools.suggest_labels(context)
    assert 'Efforts/L' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_components():
    """Test component detection in suggestions"""
    labels = ['Type/Feature', 'Priority/Medium', 'Complexity/Medium', 'Component/Backend', 'Component/Frontend', 'Component/API', 'Component/Database']
    tools = _create_tools_with_labels(labels)

    # Backend component
    context = "Update backend API service"
    suggestions = await tools.suggest_labels(context)
    assert 'Component/Backend' in suggestions
    assert 'Component/API' in suggestions

    # Frontend component
    context = "Fix frontend UI component"
    suggestions = await tools.suggest_labels(context)
    assert 'Component/Frontend' in suggestions

    # Database component
    context = "Add database migration for schema"
    suggestions = await tools.suggest_labels(context)
    assert 'Component/Database' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_tech_stack():
    """Test tech stack detection in suggestions"""
    labels = ['Type/Feature', 'Priority/Medium', 'Complexity/Medium', 'Tech/Python', 'Tech/FastAPI', 'Tech/Docker', 'Tech/PostgreSQL']
    tools = _create_tools_with_labels(labels)

    # Python
    context = "Update Python FastAPI endpoint"
    suggestions = await tools.suggest_labels(context)
    assert 'Tech/Python' in suggestions
    assert 'Tech/FastAPI' in suggestions

    # Docker
    context = "Fix Dockerfile configuration"
    suggestions = await tools.suggest_labels(context)
    assert 'Tech/Docker' in suggestions

    # PostgreSQL
    context = "Optimize PostgreSQL query"
    suggestions = await tools.suggest_labels(context)
    assert 'Tech/PostgreSQL' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_source():
    """Test source detection in suggestions"""
    labels = ['Type/Feature', 'Priority/Medium', 'Complexity/Medium', 'Source/Development', 'Source/Staging', 'Source/Production']
    tools = _create_tools_with_labels(labels)

    # Development
    context = "Issue found in development environment"
    suggestions = await tools.suggest_labels(context)
    assert 'Source/Development' in suggestions

    # Production
    context = "Critical production issue"
    suggestions = await tools.suggest_labels(context)
    assert 'Source/Production' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_risk():
    """Test risk detection in suggestions"""
    labels = ['Type/Feature', 'Priority/Medium', 'Complexity/Medium', 'Risk/High', 'Risk/Low']
    tools = _create_tools_with_labels(labels)

    # High risk
    context = "Breaking change to major API"
    suggestions = await tools.suggest_labels(context)
    assert 'Risk/High' in suggestions

    # Low risk
    context = "Safe minor update with low risk"
    suggestions = await tools.suggest_labels(context)
    assert 'Risk/Low' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_multiple_categories():
    """Test that suggestions span multiple categories"""
    labels = [
        'Type/Bug', 'Type/Feature',
        'Priority/Critical', 'Priority/Medium',
        'Complexity/Complex', 'Complexity/Medium',
        'Component/Backend', 'Component/API', 'Component/Auth',
        'Tech/FastAPI', 'Tech/PostgreSQL',
        'Source/Production'
    ]
    tools = _create_tools_with_labels(labels)

    context = """
    Urgent critical bug in production backend API service.
    Need to fix broken authentication endpoint.
    This is a complex issue requiring FastAPI and PostgreSQL expertise.
    """

    suggestions = await tools.suggest_labels(context)

    # Should have Type
    assert any('Type/' in label for label in suggestions)

    # Should have Priority
    assert any('Priority/' in label for label in suggestions)

    # Should have Component
    assert any('Component/' in label for label in suggestions)

    # Should have Tech
    assert any('Tech/' in label for label in suggestions)

    # Should have Source
    assert any('Source/' in label for label in suggestions)


@pytest.mark.asyncio
async def test_suggest_labels_empty_repo():
    """Test suggestions when no repo specified and no labels available"""
    mock_client = Mock()
    mock_client.repo = None
    tools = LabelTools(mock_client)

    context = "Fix a bug"
    suggestions = await tools.suggest_labels(context)

    # Should return empty list when no repo
    assert suggestions == []


@pytest.mark.asyncio
async def test_suggest_labels_no_matching_labels():
    """Test suggestions return empty when no matching labels exist"""
    labels = ['Custom/Label', 'Other/Thing']  # No standard labels
    tools = _create_tools_with_labels(labels)

    context = "Fix a bug"
    suggestions = await tools.suggest_labels(context)

    # Should return empty list since no Type/Bug or similar exists
    assert len(suggestions) == 0


@pytest.mark.asyncio
async def test_get_labels_org_owned_repo():
    """Test getting labels for organization-owned repository"""
    mock_client = Mock()
    mock_client.repo = 'myorg/myrepo'
    mock_client.is_org_repo = Mock(return_value=True)
    mock_client.get_org_labels = Mock(return_value=[
        {'name': 'Type/Bug', 'id': 1},
        {'name': 'Type/Feature', 'id': 2}
    ])
    mock_client.get_labels = Mock(return_value=[
        {'name': 'Component/Backend', 'id': 3}
    ])

    tools = LabelTools(mock_client)
    result = await tools.get_labels()

    # Should fetch both org and repo labels
    mock_client.is_org_repo.assert_called_once_with('myorg/myrepo')
    mock_client.get_org_labels.assert_called_once_with('myorg')
    mock_client.get_labels.assert_called_once_with('myorg/myrepo')

    assert len(result['organization']) == 2
    assert len(result['repository']) == 1
    assert result['total_count'] == 3


@pytest.mark.asyncio
async def test_get_labels_user_owned_repo():
    """Test getting labels for user-owned repository (no org labels)"""
    mock_client = Mock()
    mock_client.repo = 'lmiranda/personal-portfolio'
    mock_client.is_org_repo = Mock(return_value=False)
    mock_client.get_labels = Mock(return_value=[
        {'name': 'bug', 'id': 1},
        {'name': 'enhancement', 'id': 2}
    ])

    tools = LabelTools(mock_client)
    result = await tools.get_labels()

    # Should check if org repo
    mock_client.is_org_repo.assert_called_once_with('lmiranda/personal-portfolio')

    # Should NOT call get_org_labels for user-owned repos
    mock_client.get_org_labels.assert_not_called()

    # Should still get repo labels
    mock_client.get_labels.assert_called_once_with('lmiranda/personal-portfolio')

    assert len(result['organization']) == 0
    assert len(result['repository']) == 2
    assert result['total_count'] == 2
