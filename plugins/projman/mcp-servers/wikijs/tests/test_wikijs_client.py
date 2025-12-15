"""
Tests for Wiki.js GraphQL client.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from mcp_server.wikijs_client import WikiJSClient


@pytest.fixture
def client():
    """Create WikiJSClient instance for testing"""
    return WikiJSClient(
        api_url="http://wiki.test.com/graphql",
        api_token="test_token_123",
        base_path="/test-company",
        project="projects/test-project"
    )


@pytest.fixture
def company_client():
    """Create WikiJSClient in company mode"""
    return WikiJSClient(
        api_url="http://wiki.test.com/graphql",
        api_token="test_token_123",
        base_path="/test-company",
        project=None  # Company mode
    )


def test_client_initialization(client):
    """Test client initializes with correct settings"""
    assert client.api_url == "http://wiki.test.com/graphql"
    assert client.api_token == "test_token_123"
    assert client.base_path == "/test-company"
    assert client.project == "projects/test-project"
    assert client.mode == 'project'


def test_company_mode_initialization(company_client):
    """Test client initializes in company mode"""
    assert company_client.mode == 'company'
    assert company_client.project is None


def test_get_full_path_project_mode(client):
    """Test path construction in project mode"""
    path = client._get_full_path("documentation/api")
    assert path == "/test-company/projects/test-project/documentation/api"


def test_get_full_path_company_mode(company_client):
    """Test path construction in company mode"""
    path = company_client._get_full_path("shared/architecture")
    assert path == "/test-company/shared/architecture"


@pytest.mark.asyncio
async def test_search_pages(client):
    """Test searching pages"""
    mock_response = {
        'data': {
            'pages': {
                'search': {
                    'results': [
                        {
                            'id': 1,
                            'path': '/test-company/projects/test-project/doc1',
                            'title': 'Document 1',
                            'tags': ['api', 'documentation']
                        },
                        {
                            'id': 2,
                            'path': '/test-company/projects/test-project/doc2',
                            'title': 'Document 2',
                            'tags': ['guide', 'tutorial']
                        }
                    ]
                }
            }
        }
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        results = await client.search_pages("documentation")

        assert len(results) == 2
        assert results[0]['title'] == 'Document 1'


@pytest.mark.asyncio
async def test_get_page(client):
    """Test getting a specific page"""
    mock_response = {
        'data': {
            'pages': {
                'single': {
                    'id': 1,
                    'path': '/test-company/projects/test-project/doc1',
                    'title': 'Document 1',
                    'content': '# Test Content',
                    'tags': ['api'],
                    'isPublished': True
                }
            }
        }
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        page = await client.get_page("doc1")

        assert page is not None
        assert page['title'] == 'Document 1'
        assert page['content'] == '# Test Content'


@pytest.mark.asyncio
async def test_create_page(client):
    """Test creating a new page"""
    mock_response = {
        'data': {
            'pages': {
                'create': {
                    'responseResult': {
                        'succeeded': True,
                        'errorCode': None,
                        'message': 'Page created successfully'
                    },
                    'page': {
                        'id': 1,
                        'path': '/test-company/projects/test-project/new-doc',
                        'title': 'New Document'
                    }
                }
            }
        }
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        page = await client.create_page(
            path="new-doc",
            title="New Document",
            content="# Content",
            tags=["test"]
        )

        assert page['id'] == 1
        assert page['title'] == 'New Document'


@pytest.mark.asyncio
async def test_update_page(client):
    """Test updating a page"""
    mock_response = {
        'data': {
            'pages': {
                'update': {
                    'responseResult': {
                        'succeeded': True,
                        'message': 'Page updated'
                    },
                    'page': {
                        'id': 1,
                        'path': '/test-company/projects/test-project/doc1',
                        'title': 'Updated Title'
                    }
                }
            }
        }
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        page = await client.update_page(
            page_id=1,
            title="Updated Title"
        )

        assert page['title'] == 'Updated Title'


@pytest.mark.asyncio
async def test_list_pages(client):
    """Test listing pages"""
    mock_response = {
        'data': {
            'pages': {
                'list': [
                    {'id': 1, 'path': '/test-company/projects/test-project/doc1', 'title': 'Doc 1'},
                    {'id': 2, 'path': '/test-company/projects/test-project/doc2', 'title': 'Doc 2'},
                    {'id': 3, 'path': '/test-company/other-project/doc3', 'title': 'Doc 3'}
                ]
            }
        }
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        # List all pages in current project
        pages = await client.list_pages("")

        # Should only return pages from test-project
        assert len(pages) == 2


@pytest.mark.asyncio
async def test_create_lesson(client):
    """Test creating a lesson learned"""
    mock_response = {
        'data': {
            'pages': {
                'create': {
                    'responseResult': {
                        'succeeded': True,
                        'message': 'Lesson created'
                    },
                    'page': {
                        'id': 1,
                        'path': '/test-company/projects/test-project/lessons-learned/sprints/test-lesson',
                        'title': 'Test Lesson'
                    }
                }
            }
        }
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        lesson = await client.create_lesson(
            title="Test Lesson",
            content="# Lesson Content",
            tags=["testing", "sprint-16"],
            category="sprints"
        )

        assert lesson['id'] == 1
        assert 'lessons-learned' in lesson['path']


@pytest.mark.asyncio
async def test_search_lessons(client):
    """Test searching lessons learned"""
    mock_response = {
        'data': {
            'pages': {
                'search': {
                    'results': [
                        {
                            'id': 1,
                            'path': '/test-company/projects/test-project/lessons-learned/sprints/lesson1',
                            'title': 'Lesson 1',
                            'tags': ['testing']
                        },
                        {
                            'id': 2,
                            'path': '/test-company/projects/test-project/documentation/doc1',
                            'title': 'Doc 1',
                            'tags': ['guide']
                        }
                    ]
                }
            }
        }
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        lessons = await client.search_lessons(query="testing")

        # Should only return lessons-learned pages
        assert len(lessons) == 1
        assert 'lessons-learned' in lessons[0]['path']


@pytest.mark.asyncio
async def test_graphql_error_handling(client):
    """Test handling of GraphQL errors"""
    mock_response = {
        'errors': [
            {'message': 'Page not found'},
            {'message': 'Invalid query'}
        ]
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_instance.post = AsyncMock(return_value=MagicMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        ))
        mock_client.return_value = mock_instance

        with pytest.raises(ValueError, match="GraphQL errors"):
            await client.search_pages("test")
