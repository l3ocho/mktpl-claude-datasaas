#!/usr/bin/env python3
"""
Integration test script for Wiki.js MCP Server.
Tests against real Wiki.js instance.

Usage:
    python test_integration.py
"""
import asyncio
import sys
from mcp_server.config import WikiJSConfig
from mcp_server.wikijs_client import WikiJSClient


async def test_connection():
    """Test basic connection to Wiki.js"""
    print("🔌 Testing Wiki.js connection...")

    try:
        config_loader = WikiJSConfig()
        config = config_loader.load()

        print(f"✓ Configuration loaded")
        print(f"  - API URL: {config['api_url']}")
        print(f"  - Base Path: {config['base_path']}")
        print(f"  - Mode: {config['mode']}")
        if config.get('project'):
            print(f"  - Project: {config['project']}")

        client = WikiJSClient(
            api_url=config['api_url'],
            api_token=config['api_token'],
            base_path=config['base_path'],
            project=config.get('project')
        )

        print("✓ Client initialized")
        return client

    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        return None


async def test_list_pages(client):
    """Test listing pages"""
    print("\n📄 Testing list_pages...")

    try:
        pages = await client.list_pages("")
        print(f"✓ Found {len(pages)} pages")

        if pages:
            print(f"  Sample pages:")
            for page in pages[:5]:
                print(f"    - {page.get('title')} ({page.get('path')})")

        return True
    except Exception as e:
        print(f"✗ List pages failed: {e}")
        return False


async def test_search_pages(client):
    """Test searching pages"""
    print("\n🔍 Testing search_pages...")

    try:
        results = await client.search_pages("test", limit=5)
        print(f"✓ Search returned {len(results)} results")

        if results:
            print(f"  Sample results:")
            for result in results[:3]:
                print(f"    - {result.get('title')}")

        return True
    except Exception as e:
        print(f"✗ Search failed: {e}")
        return False


async def test_create_page(client):
    """Test creating a page"""
    print("\n➕ Testing create_page...")

    # Use timestamp to create unique page path
    import time
    timestamp = int(time.time())
    page_path = f"testing/integration-test-{timestamp}"

    try:
        page = await client.create_page(
            path=page_path,
            title=f"Integration Test Page - {timestamp}",
            content="# Integration Test\n\nThis page was created by the Wiki.js MCP Server integration test.",
            description="Automated test page",
            tags=["test", "integration", "mcp"],
            is_published=False  # Don't publish test page
        )

        print(f"✓ Page created successfully")
        print(f"  - ID: {page.get('id')}")
        print(f"  - Path: {page.get('path')}")
        print(f"  - Title: {page.get('title')}")

        return page_path  # Return path for testing get_page

    except Exception as e:
        import traceback
        print(f"✗ Create page failed: {e}")
        print(f"  Error details: {traceback.format_exc()}")
        return None


async def test_get_page(client, page_path):
    """Test getting a specific page"""
    print("\n📖 Testing get_page...")

    try:
        page = await client.get_page(page_path)

        if page:
            print(f"✓ Page retrieved successfully")
            print(f"  - Title: {page.get('title')}")
            print(f"  - Tags: {', '.join(page.get('tags', []))}")
            print(f"  - Published: {page.get('isPublished')}")
            return True
        else:
            print(f"✗ Page not found: {page_path}")
            return False

    except Exception as e:
        print(f"✗ Get page failed: {e}")
        return False


async def main():
    """Run all integration tests"""
    print("=" * 60)
    print("Wiki.js MCP Server - Integration Tests")
    print("=" * 60)

    # Test connection
    client = await test_connection()
    if not client:
        print("\n❌ Integration tests failed: Cannot connect to Wiki.js")
        sys.exit(1)

    # Run tests
    results = []

    results.append(await test_list_pages(client))
    results.append(await test_search_pages(client))

    page_path = await test_create_page(client)
    if page_path:
        results.append(True)
        # Test getting the created page
        results.append(await test_get_page(client, page_path))
    else:
        results.append(False)
        results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"✓ Passed: {passed}/{total}")
    print(f"✗ Failed: {total - passed}/{total}")

    if passed == total:
        print("\n✅ All integration tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some integration tests failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
