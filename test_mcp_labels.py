#!/usr/bin/env python3
"""
Test MCP Server Label Fetching
Verifies that the Gitea MCP server can fetch all 43 labels (27 org + 16 repo)
"""
import sys
import os
import asyncio

# Add mcp-servers/gitea to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp-servers', 'gitea'))

from mcp_server.gitea_client import GiteaClient
from mcp_server.tools.labels import LabelTools

async def test_label_fetching():
    """Test that MCP server can fetch all labels"""
    print("="*60)
    print("Testing MCP Server Label Fetching")
    print("="*60)

    # Initialize client (loads from ~/.config/claude/gitea.env and .env)
    print("\n1. Initializing Gitea client...")
    print("   Loading configuration from:")
    print("   - System: ~/.config/claude/gitea.env")
    print("   - Project: .env")

    client = GiteaClient()
    print(f"   ✅ Client initialized")
    print(f"   - API URL: {client.base_url}")
    print(f"   - Owner: {client.owner}")
    print(f"   - Repo: {client.repo}")
    print(f"   - Mode: {client.mode}")

    # Initialize label tools
    print("\n2. Initializing label tools...")
    label_tools = LabelTools(client)
    print("   ✅ Label tools initialized")

    # Fetch all labels
    print("\n3. Fetching labels from Gitea...")
    result = await label_tools.get_labels()

    org_labels = result['organization']
    repo_labels = result['repository']
    total_count = result['total_count']

    print(f"   ✅ Labels fetched successfully")
    print(f"   - Organization labels: {len(org_labels)}")
    print(f"   - Repository labels: {len(repo_labels)}")
    print(f"   - Total: {total_count}")

    # Verify counts
    print("\n4. Verifying label counts...")
    expected_org = 27
    expected_repo = 16
    expected_total = 43

    all_passed = True

    if len(org_labels) == expected_org:
        print(f"   ✅ Organization labels: {len(org_labels)} (expected: {expected_org})")
    else:
        print(f"   ❌ Organization labels: {len(org_labels)} (expected: {expected_org})")
        all_passed = False

    if len(repo_labels) == expected_repo:
        print(f"   ✅ Repository labels: {len(repo_labels)} (expected: {expected_repo})")
    else:
        print(f"   ❌ Repository labels: {len(repo_labels)} (expected: {expected_repo})")
        all_passed = False

    if total_count == expected_total:
        print(f"   ✅ Total labels: {total_count} (expected: {expected_total})")
    else:
        print(f"   ❌ Total labels: {total_count} (expected: {expected_total})")
        all_passed = False

    # Show label breakdown
    print("\n5. Label Breakdown:")

    # Categorize org labels
    org_categories = {}
    for label in org_labels:
        category = label['name'].split('/')[0]
        if category not in org_categories:
            org_categories[category] = []
        org_categories[category].append(label['name'])

    print("\n   Organization Labels by Category:")
    for category, labels in sorted(org_categories.items()):
        print(f"   - {category}: {len(labels)} labels")
        for label in sorted(labels):
            print(f"      • {label}")

    # Categorize repo labels
    repo_categories = {}
    for label in repo_labels:
        category = label['name'].split('/')[0]
        if category not in repo_categories:
            repo_categories[category] = []
        repo_categories[category].append(label['name'])

    print("\n   Repository Labels by Category:")
    for category, labels in sorted(repo_categories.items()):
        print(f"   - {category}: {len(labels)} labels")
        for label in sorted(labels):
            print(f"      • {label}")

    # Test label suggestion
    print("\n6. Testing Label Suggestion:")
    test_contexts = [
        "Fix critical bug in authentication service causing login failures",
        "Add new feature to export reports to PDF format",
        "Refactor backend API to extract authentication service"
    ]

    for context in test_contexts:
        suggested = await label_tools.suggest_labels(context)
        print(f"\n   Context: \"{context}\"")
        print(f"   Suggested labels: {', '.join(suggested)}")

    # Final result
    print("\n" + "="*60)
    if all_passed:
        print("✅ SUCCESS: MCP Server can fetch all 43 labels correctly!")
        print("="*60)
        return 0
    else:
        print("❌ FAILED: Label count mismatch detected")
        print("="*60)
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_label_fetching())
    sys.exit(exit_code)
