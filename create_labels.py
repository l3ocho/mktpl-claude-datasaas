#!/usr/bin/env python3
"""
Batch create Gitea labels via API for bandit organization
Creates 28 organization labels + 16 repository labels = 44 total
"""
import requests
import sys

import os

GITEA_URL = os.getenv("GITEA_API_URL", "").rstrip("/api/v1")
TOKEN = os.getenv("GITEA_API_TOKEN", "")
ORG = "bandit"
REPO = "support-claude-mktplace"

headers = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}

# Organization labels (28 total)
org_labels = [
    # Agent (2)
    {"name": "Agent/Human", "color": "0052CC", "description": "Work performed by human developers"},
    {"name": "Agent/Claude", "color": "6554C0", "description": "Work performed by Claude Code or AI assistants"},

    # Complexity (3)
    {"name": "Complexity/Simple", "color": "C2E0C6", "description": "Straightforward tasks requiring minimal analysis"},
    {"name": "Complexity/Medium", "color": "FFF4CE", "description": "Moderate complexity with some architectural decisions"},
    {"name": "Complexity/Complex", "color": "FFBDAD", "description": "High complexity requiring significant planning"},

    # Efforts (5)
    {"name": "Efforts/XS", "color": "C2E0C6", "description": "Extra small effort (< 2 hours)"},
    {"name": "Efforts/S", "color": "D4F1D4", "description": "Small effort (2-4 hours)"},
    {"name": "Efforts/M", "color": "FFF4CE", "description": "Medium effort (4-8 hours / 1 day)"},
    {"name": "Efforts/L", "color": "FFE0B2", "description": "Large effort (1-3 days)"},
    {"name": "Efforts/XL", "color": "FFBDAD", "description": "Extra large effort (> 3 days)"},

    # Priority (4)
    {"name": "Priority/Low", "color": "D4E157", "description": "Nice to have, can wait"},
    {"name": "Priority/Medium", "color": "FFEB3B", "description": "Should be done this sprint"},
    {"name": "Priority/High", "color": "FF9800", "description": "Important, do soon"},
    {"name": "Priority/Critical", "color": "F44336", "description": "Urgent, blocking other work"},

    # Risk (3)
    {"name": "Risk/Low", "color": "C2E0C6", "description": "Low risk of issues or impact"},
    {"name": "Risk/Medium", "color": "FFF4CE", "description": "Moderate risk, proceed with caution"},
    {"name": "Risk/High", "color": "FFBDAD", "description": "High risk, needs careful planning and testing"},

    # Source (4)
    {"name": "Source/Development", "color": "7CB342", "description": "Issue discovered during development"},
    {"name": "Source/Staging", "color": "FFB300", "description": "Issue found in staging environment"},
    {"name": "Source/Production", "color": "E53935", "description": "Issue found in production"},
    {"name": "Source/Customer", "color": "AB47BC", "description": "Issue reported by customer"},

    # Type (6)
    {"name": "Type/Bug", "color": "D73A4A", "description": "Bug fixes and error corrections"},
    {"name": "Type/Feature", "color": "0075CA", "description": "New features and enhancements"},
    {"name": "Type/Refactor", "color": "FBCA04", "description": "Code restructuring and architectural changes"},
    {"name": "Type/Documentation", "color": "0E8A16", "description": "Documentation updates and improvements"},
    {"name": "Type/Test", "color": "1D76DB", "description": "Testing-related work (unit, integration, e2e)"},
    {"name": "Type/Chore", "color": "FEF2C0", "description": "Maintenance, tooling, dependencies, build tasks"},
]

# Repository labels (16 total)
repo_labels = [
    # Component (9)
    {"name": "Component/Backend", "color": "5319E7", "description": "Backend service code and business logic"},
    {"name": "Component/Frontend", "color": "1D76DB", "description": "User interface and client-side code"},
    {"name": "Component/API", "color": "0366D6", "description": "API endpoints, contracts, and integration"},
    {"name": "Component/Database", "color": "006B75", "description": "Database schemas, migrations, queries"},
    {"name": "Component/Auth", "color": "E99695", "description": "Authentication and authorization"},
    {"name": "Component/Deploy", "color": "BFD4F2", "description": "Deployment, infrastructure, DevOps"},
    {"name": "Component/Testing", "color": "F9D0C4", "description": "Test infrastructure and frameworks"},
    {"name": "Component/Docs", "color": "C5DEF5", "description": "Documentation and guides"},
    {"name": "Component/Infra", "color": "D4C5F9", "description": "Infrastructure and system configuration"},

    # Tech (7)
    {"name": "Tech/Python", "color": "3572A5", "description": "Python language and libraries"},
    {"name": "Tech/JavaScript", "color": "F1E05A", "description": "JavaScript/Node.js code"},
    {"name": "Tech/Docker", "color": "384D54", "description": "Docker containers and compose"},
    {"name": "Tech/PostgreSQL", "color": "336791", "description": "PostgreSQL database"},
    {"name": "Tech/Redis", "color": "DC382D", "description": "Redis cache and pub/sub"},
    {"name": "Tech/Vue", "color": "42B883", "description": "Vue.js frontend framework"},
    {"name": "Tech/FastAPI", "color": "009688", "description": "FastAPI backend framework"},
]

def create_org_labels():
    """Create organization-level labels"""
    print(f"\n{'='*60}")
    print(f"Creating {len(org_labels)} ORGANIZATION labels in {ORG}")
    print(f"{'='*60}\n")

    created = 0
    skipped = 0
    errors = 0

    for label in org_labels:
        try:
            response = requests.post(
                f"{GITEA_URL}/api/v1/orgs/{ORG}/labels",
                headers=headers,
                json=label
            )

            if response.status_code == 201:
                print(f"✅ Created: {label['name']}")
                created += 1
            elif response.status_code == 409:
                print(f"⏭️  Skipped (exists): {label['name']}")
                skipped += 1
            else:
                print(f"❌ Failed: {label['name']} - {response.status_code} {response.text}")
                errors += 1
        except Exception as e:
            print(f"❌ Error creating {label['name']}: {e}")
            errors += 1

    print(f"\n📊 Organization Labels Summary:")
    print(f"   ✅ Created: {created}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   ❌ Errors: {errors}")
    return created, skipped, errors

def create_repo_labels():
    """Create repository-level labels"""
    print(f"\n{'='*60}")
    print(f"Creating {len(repo_labels)} REPOSITORY labels in {ORG}/{REPO}")
    print(f"{'='*60}\n")

    created = 0
    skipped = 0
    errors = 0

    for label in repo_labels:
        try:
            response = requests.post(
                f"{GITEA_URL}/api/v1/repos/{ORG}/{REPO}/labels",
                headers=headers,
                json=label
            )

            if response.status_code == 201:
                print(f"✅ Created: {label['name']}")
                created += 1
            elif response.status_code == 409:
                print(f"⏭️  Skipped (exists): {label['name']}")
                skipped += 1
            else:
                print(f"❌ Failed: {label['name']} - {response.status_code} {response.text}")
                errors += 1
        except Exception as e:
            print(f"❌ Error creating {label['name']}: {e}")
            errors += 1

    print(f"\n📊 Repository Labels Summary:")
    print(f"   ✅ Created: {created}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   ❌ Errors: {errors}")
    return created, skipped, errors

def verify_labels():
    """Verify all labels were created"""
    print(f"\n{'='*60}")
    print("VERIFICATION")
    print(f"{'='*60}\n")

    try:
        # Count organization labels
        response = requests.get(
            f"{GITEA_URL}/api/v1/orgs/{ORG}/labels",
            headers=headers
        )
        org_count = len(response.json()) if response.status_code == 200 else 0

        # Count repository labels (includes org labels)
        response = requests.get(
            f"{GITEA_URL}/api/v1/repos/{ORG}/{REPO}/labels",
            headers=headers
        )
        total_count = len(response.json()) if response.status_code == 200 else 0

        print(f"📊 Label Count:")
        print(f"   Organization labels: {org_count} (expected: 28)")
        print(f"   Total labels: {total_count} (expected: 44)")

        if org_count == 28 and total_count == 44:
            print(f"\n✅ SUCCESS! All labels created correctly!")
            return True
        else:
            print(f"\n⚠️  WARNING: Label count mismatch")
            if org_count != 28:
                print(f"   - Expected 28 org labels, got {org_count}")
            if total_count != 44:
                print(f"   - Expected 44 total labels, got {total_count}")
            return False
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def main():
    print(f"\n{'#'*60}")
    print("# Gitea Label Creation Script")
    print("# Creating 44-label taxonomy for bandit organization")
    print(f"{'#'*60}")

    # Create organization labels
    org_created, org_skipped, org_errors = create_org_labels()

    # Create repository labels
    repo_created, repo_skipped, repo_errors = create_repo_labels()

    # Verify creation
    success = verify_labels()

    # Final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Total created: {org_created + repo_created}")
    print(f"Total skipped: {org_skipped + repo_skipped}")
    print(f"Total errors: {org_errors + repo_errors}")

    if success:
        print(f"\n✅ All labels created successfully!")
        print(f"\nNext steps:")
        print(f"1. Run: /labels-sync")
        print(f"2. Test: /sprint-plan")
        print(f"3. Verify plugin detects all 44 labels")
        return 0
    else:
        print(f"\n⚠️  Label creation completed with warnings")
        print(f"Check the output above for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())
