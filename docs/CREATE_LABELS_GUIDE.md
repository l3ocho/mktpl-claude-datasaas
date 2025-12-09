# Quick Guide: Creating Label Taxonomy in Gitea

**Estimated Time:** 15-20 minutes
**Required:** Admin access to bandit organization in Gitea

## Why This Is Needed

The Projman plugin depends on a 44-label taxonomy system for:
- Issue categorization (Type, Priority, Component, Tech)
- Intelligent label suggestions
- Sprint planning and filtering
- Progress tracking by category

**Currently:** Repository has 0 labels
**Required:** 44 labels (28 organization + 16 repository)

## Step 1: Create Organization Labels (28 labels)

**Navigate to:** https://gitea.example.com/org/bandit/settings/labels

These labels will be available to ALL repositories in bandit organization.

### Agent (2 labels)
| Name | Color | Description |
|------|-------|-------------|
| Agent/Human | `#0052CC` | Work performed by human developers |
| Agent/Claude | `#6554C0` | Work performed by Claude Code or AI assistants |

### Complexity (3 labels)
| Name | Color | Description |
|------|-------|-------------|
| Complexity/Simple | `#C2E0C6` | Straightforward tasks requiring minimal analysis |
| Complexity/Medium | `#FFF4CE` | Moderate complexity with some architectural decisions |
| Complexity/Complex | `#FFBDAD` | High complexity requiring significant planning |

### Efforts (5 labels)
| Name | Color | Description |
|------|-------|-------------|
| Efforts/XS | `#C2E0C6` | Extra small effort (< 2 hours) |
| Efforts/S | `#D4F1D4` | Small effort (2-4 hours) |
| Efforts/M | `#FFF4CE` | Medium effort (4-8 hours / 1 day) |
| Efforts/L | `#FFE0B2` | Large effort (1-3 days) |
| Efforts/XL | `#FFBDAD` | Extra large effort (> 3 days) |

### Priority (4 labels)
| Name | Color | Description |
|------|-------|-------------|
| Priority/Low | `#D4E157` | Nice to have, can wait |
| Priority/Medium | `#FFEB3B` | Should be done this sprint |
| Priority/High | `#FF9800` | Important, do soon |
| Priority/Critical | `#F44336` | Urgent, blocking other work |

### Risk (3 labels)
| Name | Color | Description |
|------|-------|-------------|
| Risk/Low | `#C2E0C6` | Low risk of issues or impact |
| Risk/Medium | `#FFF4CE` | Moderate risk, proceed with caution |
| Risk/High | `#FFBDAD` | High risk, needs careful planning and testing |

### Source (4 labels)
| Name | Color | Description |
|------|-------|-------------|
| Source/Development | `#7CB342` | Issue discovered during development |
| Source/Staging | `#FFB300` | Issue found in staging environment |
| Source/Production | `#E53935` | Issue found in production |
| Source/Customer | `#AB47BC` | Issue reported by customer |

### Type (6 labels)
| Name | Color | Description |
|------|-------|-------------|
| Type/Bug | `#D73A4A` | Bug fixes and error corrections |
| Type/Feature | `#0075CA` | New features and enhancements |
| Type/Refactor | `#FBCA04` | Code restructuring and architectural changes |
| Type/Documentation | `#0E8A16` | Documentation updates and improvements |
| Type/Test | `#1D76DB` | Testing-related work (unit, integration, e2e) |
| Type/Chore | `#FEF2C0` | Maintenance, tooling, dependencies, build tasks |

**Total Organization Labels: 28**

## Step 2: Create Repository Labels (16 labels)

**Navigate to:** https://gitea.example.com/bandit/support-claude-mktplace/labels

These labels are specific to the support-claude-mktplace repository.

### Component (9 labels)
| Name | Color | Description |
|------|-------|-------------|
| Component/Backend | `#5319E7` | Backend service code and business logic |
| Component/Frontend | `#1D76DB` | User interface and client-side code |
| Component/API | `#0366D6` | API endpoints, contracts, and integration |
| Component/Database | `#006B75` | Database schemas, migrations, queries |
| Component/Auth | `#E99695` | Authentication and authorization |
| Component/Deploy | `#BFD4F2` | Deployment, infrastructure, DevOps |
| Component/Testing | `#F9D0C4` | Test infrastructure and frameworks |
| Component/Docs | `#C5DEF5` | Documentation and guides |
| Component/Infra | `#D4C5F9` | Infrastructure and system configuration |

### Tech (7 labels)
| Name | Color | Description |
|------|-------|-------------|
| Tech/Python | `#3572A5` | Python language and libraries |
| Tech/JavaScript | `#F1E05A` | JavaScript/Node.js code |
| Tech/Docker | `#384D54` | Docker containers and compose |
| Tech/PostgreSQL | `#336791` | PostgreSQL database |
| Tech/Redis | `#DC382D` | Redis cache and pub/sub |
| Tech/Vue | `#42B883` | Vue.js frontend framework |
| Tech/FastAPI | `#009688` | FastAPI backend framework |

**Total Repository Labels: 16**

## Step 3: Verify Label Creation

After creating all labels, verify:

```bash
# Count organization labels
curl -s "https://gitea.example.com/api/v1/orgs/bandit/labels" \
  -H "Authorization: token YOUR_TOKEN" | python3 -c "import sys, json; print(len(json.load(sys.stdin)), 'org labels')"

# Count repository labels
curl -s "https://gitea.example.com/api/v1/repos/bandit/support-claude-mktplace/labels" \
  -H "Authorization: token YOUR_TOKEN" | python3 -c "import sys, json; print(len(json.load(sys.stdin)), 'repo labels')"
```

**Expected Output:**
```
28 org labels
44 repo labels  # (28 org + 16 repo)
```

## Step 4: Sync Labels with Plugin

After creating all labels in Gitea:

```bash
cd /home/lmiranda/Repositories/hhl/hhl-claude-agents
/labels-sync
```

**Expected Output:**
```
Fetching labels from Gitea...

Current Label Taxonomy:
- Organization Labels: 28
- Repository Labels: 16
- Total: 44 labels

✅ Label taxonomy synchronized successfully!
```

The plugin will update `projman/skills/label-taxonomy/labels-reference.md` with the current taxonomy.

## Alternative: Batch Creation Script

If you prefer to create labels programmatically:

```python
#!/usr/bin/env python3
"""
Batch create Gitea labels via API
"""
import requests

GITEA_URL = "https://gitea.example.com"
TOKEN = "ae72c63cd7de02e40bd16f66d1e98059c187759b"
ORG = "bandit"
REPO = "support-claude-mktplace"

headers = {"Authorization": f"token {TOKEN}"}

# Organization labels
org_labels = [
    {"name": "Agent/Human", "color": "#0052CC", "description": "Work performed by human developers"},
    {"name": "Agent/Claude", "color": "#6554C0", "description": "Work performed by Claude Code"},
    # ... (add all 28 org labels)
]

# Repository labels
repo_labels = [
    {"name": "Component/Backend", "color": "#5319E7", "description": "Backend service code"},
    # ... (add all 16 repo labels)
]

# Create organization labels
for label in org_labels:
    response = requests.post(
        f"{GITEA_URL}/api/v1/orgs/{ORG}/labels",
        headers=headers,
        json=label
    )
    print(f"Created org label: {label['name']} - {response.status_code}")

# Create repository labels
for label in repo_labels:
    response = requests.post(
        f"{GITEA_URL}/api/v1/repos/{ORG}/{REPO}/labels",
        headers=headers,
        json=label
    )
    print(f"Created repo label: {label['name']} - {response.status_code}")

print("\n✅ Label creation complete!")
```

## After Label Creation

Once labels are created, you can:

1. ✅ Run `/labels-sync` to update plugin
2. ✅ Run `/sprint-plan` to create labeled issues
3. ✅ Test label suggestions
4. ✅ Use label-based filtering in `/sprint-status`
5. ✅ Execute full workflow test

The plugin will now have full functionality!

---

**Total Time:** 15-20 minutes (manual) or 2-3 minutes (script)
**Benefit:** Full plugin functionality unlocked
**One-Time Task:** Labels persist and are reusable across all sprints
