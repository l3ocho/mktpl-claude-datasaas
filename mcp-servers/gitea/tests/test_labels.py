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
    client.repo = 'test_repo'
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


@pytest.mark.asyncio
async def test_suggest_labels_bug():
    """Test label suggestion for bug context"""
    tools = LabelTools(Mock())

    context = "Fix critical bug in login authentication"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Bug' in suggestions
    assert 'Priority/Critical' in suggestions
    assert 'Component/Auth' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_feature():
    """Test label suggestion for feature context"""
    tools = LabelTools(Mock())

    context = "Add new feature to implement user dashboard"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Feature' in suggestions
    assert any('Priority' in label for label in suggestions)


@pytest.mark.asyncio
async def test_suggest_labels_refactor():
    """Test label suggestion for refactor context"""
    tools = LabelTools(Mock())

    context = "Refactor architecture to extract service layer"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Refactor' in suggestions
    assert 'Component/Backend' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_documentation():
    """Test label suggestion for documentation context"""
    tools = LabelTools(Mock())

    context = "Update documentation for API endpoints"
    suggestions = await tools.suggest_labels(context)

    assert 'Type/Documentation' in suggestions
    assert 'Component/API' in suggestions or 'Component/Docs' in suggestions


@pytest.mark.asyncio
async def test_suggest_labels_priority():
    """Test priority detection in suggestions"""
    tools = LabelTools(Mock())

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
    tools = LabelTools(Mock())

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
    tools = LabelTools(Mock())

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
    tools = LabelTools(Mock())

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
    tools = LabelTools(Mock())

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
    tools = LabelTools(Mock())

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
    tools = LabelTools(Mock())

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
    tools = LabelTools(Mock())

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
