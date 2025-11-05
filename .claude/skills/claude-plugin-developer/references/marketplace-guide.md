# Marketplace Publication Guide

Complete guide for distributing Claude plugins through marketplaces.

## Marketplace Types

### GitHub Marketplace
Best for: Open source, team collaboration, public distribution

```bash
# Add marketplace
claude plugin marketplace add owner/repo

# Structure required
repo/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    ├── plugin-one/
    ├── plugin-two/
    └── plugin-three/
```

### GitLab Marketplace
Best for: Private teams, enterprise environments

```bash
# Add GitLab marketplace
claude plugin marketplace add gitlab:group/project

# Requires access token
export GITLAB_TOKEN="your-token"
```

### Local Marketplace
Best for: Development, testing, private plugins

```bash
# Add local marketplace
claude plugin marketplace add file:///path/to/marketplace

# Structure
/path/to/marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
```

### Remote URL Marketplace
Best for: Custom hosting, CDN distribution

```bash
# Add remote marketplace
claude plugin marketplace add https://plugins.example.com
```

## Marketplace Configuration

### marketplace.json Structure
```json
{
  "name": "Hyper Hive Labs Plugins",
  "description": "Restaurant automation and AI tools",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "restaurant-analytics",
      "version": "2.1.0",
      "description": "Analytics dashboard for restaurant data",
      "author": "Hyper Hive Labs",
      "path": "plugins/restaurant-analytics",
      "tags": ["analytics", "restaurant", "reporting"],
      "requirements": {
        "claude-version": ">=1.0.0",
        "dependencies": ["python>=3.9", "pandas"]
      }
    },
    {
      "name": "order-automation",
      "version": "1.5.2",
      "description": "Automated order processing system",
      "author": "Hyper Hive Labs",
      "path": "plugins/order-automation",
      "featured": true,
      "beta": false
    }
  ],
  "categories": [
    {
      "name": "Analytics",
      "description": "Data analysis and reporting tools",
      "plugins": ["restaurant-analytics", "sales-insights"]
    },
    {
      "name": "Automation",
      "description": "Workflow automation tools",
      "plugins": ["order-automation", "inventory-manager"]
    }
  ]
}
```

## Publishing Workflow

### 1. Prepare Plugin
```bash
# Validate plugin structure
cd my-plugin/
claude plugin validate .

# Test locally
claude plugin install file://$(pwd)

# Version bump
npm version patch  # or minor/major
```

### 2. Create Release Branch
```bash
# GitHub flow
git checkout -b release/v1.2.0
git add .
git commit -m "Release v1.2.0"
git push origin release/v1.2.0
```

### 3. Update Marketplace
```json
// Add to marketplace.json
{
  "name": "my-new-plugin",
  "version": "1.2.0",
  "path": "plugins/my-new-plugin",
  "description": "My awesome plugin",
  "changelog": {
    "1.2.0": "Added new features",
    "1.1.0": "Bug fixes",
    "1.0.0": "Initial release"
  }
}
```

### 4. Tag and Release
```bash
# Create signed tag
git tag -s v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# GitHub release
gh release create v1.2.0 \
  --title "Release v1.2.0" \
  --notes "Release notes here"
```

## Team Marketplace Setup

### Organization Structure
```
github.com/myorg/claude-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── shared-utils/
│   ├── deploy-tools/
│   └── code-review/
├── docs/
│   ├── CONTRIBUTING.md
│   └── STANDARDS.md
└── .github/
    └── workflows/
        └── validate-plugins.yml
```

### Team Configuration
```json
// .claude/settings.json in user's machine
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "myorg/claude-plugins"
      },
      "autoUpdate": true,
      "updateInterval": 3600
    }
  }
}
```

### Access Control
```yaml
# .github/CODEOWNERS
/plugins/deploy-tools/ @devops-team
/plugins/code-review/ @engineering-leads
/.claude-plugin/ @plugin-admins
```

## Security Requirements

### Code Signing
```bash
# Generate GPG key
gpg --gen-key

# Sign commits
git config commit.gpgsign true
git config user.signingkey YOUR_KEY_ID

# Sign tags
git tag -s v1.0.0 -m "Signed release"
```

### Dependency Verification
```json
{
  "dependencies": {
    "axios": {
      "version": "1.6.0",
      "integrity": "sha512-...",
      "source": "npm"
    }
  }
}
```

### Security Manifest
```json
// security.json
{
  "permissions": {
    "file_access": ["read", "write"],
    "network_access": {
      "allowed_domains": ["api.mycompany.com"],
      "protocols": ["https"]
    }
  },
  "audit": {
    "last_review": "2024-01-15",
    "reviewer": "security-team",
    "findings": "none"
  }
}
```

## Version Management

### Semantic Versioning
```
MAJOR.MINOR.PATCH

1.0.0 -> 1.0.1 (patch: bug fixes)
1.0.0 -> 1.1.0 (minor: new features, backward compatible)
1.0.0 -> 2.0.0 (major: breaking changes)
```

### Version Constraints
```json
{
  "requirements": {
    "claude-version": ">=1.0.0 <2.0.0",
    "dependencies": {
      "python": "~3.9.0",  // 3.9.x
      "node": "^18.0.0"    // >=18.0.0 <19.0.0
    }
  }
}
```

### Deprecation Policy
```json
{
  "deprecated": true,
  "deprecation_notice": "Use 'advanced-deploy' instead",
  "sunset_date": "2024-06-01",
  "migration_guide": "https://docs.example.com/migrate"
}
```

## Distribution Strategies

### Public Distribution
1. **Open Source**
   - Host on GitHub/GitLab
   - Include LICENSE file
   - Accept contributions
   - Maintain changelog

2. **Discovery**
   - Submit to official registry
   - Add topics/tags
   - Write good descriptions
   - Include screenshots

### Private Distribution
1. **Internal Teams**
   - Private Git repositories
   - VPN-only marketplaces
   - Access tokens
   - audit logs

2. **Enterprise**
   - Self-hosted marketplaces
   - Air-gapped environments
   - Signed packages
   - Compliance tracking

### Hybrid Approach
```json
{
  "public_plugins": ["docs-generator", "linter"],
  "private_plugins": ["deploy-prod", "customer-data"],
  "visibility": {
    "docs-generator": "public",
    "deploy-prod": "internal-only"
  }
}
```

## Marketplace Features

### Plugin Search
```json
{
  "search": {
    "enabled": true,
    "fields": ["name", "description", "tags"],
    "filters": ["category", "author", "version"]
  }
}
```

### Auto-updates
```json
{
  "auto_update": {
    "enabled": true,
    "channels": {
      "stable": "*/releases/latest",
      "beta": "*/releases/beta",
      "nightly": "*/commits/main"
    },
    "strategy": "minor-only"
  }
}
```

### Plugin Analytics
```json
{
  "analytics": {
    "track_installs": true,
    "track_usage": false,
    "anonymize": true,
    "retention_days": 90
  }
}
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Validate and Publish Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate Plugin Structure
        run: |
          # Validate JSON files
          jq . .claude-plugin/plugin.json
          jq . .claude-plugin/marketplace.json
          
      - name: Run Tests
        run: |
          npm test
          
      - name: Update Marketplace
        run: |
          # Update marketplace.json with new version
          jq '.plugins[0].version = "${{ github.ref_name }}"' \
            marketplace.json > tmp.json
          mv tmp.json marketplace.json
          
      - name: Commit Changes
        run: |
          git config user.name "GitHub Actions"
          git commit -am "Update marketplace for ${{ github.ref_name }}"
          git push
```

### GitLab CI
```yaml
stages:
  - validate
  - test
  - publish

validate:plugin:
  stage: validate
  script:
    - jq . .claude-plugin/plugin.json
    - jq . .claude-plugin/marketplace.json

publish:marketplace:
  stage: publish
  only:
    - tags
  script:
    - update-marketplace-version.sh
    - git push origin main
```

## Troubleshooting

### Common Issues

1. **Marketplace not found**
   ```bash
   # Check marketplace list
   claude plugin marketplace list
   
   # Verify URL/path
   curl https://marketplace.url/.claude-plugin/marketplace.json
   ```

2. **Plugin installation fails**
   ```bash
   # Debug mode
   claude --debug plugin install my-plugin
   
   # Check permissions
   ls -la ~/.claude/plugins/
   ```

3. **Version conflicts**
   ```bash
   # Force specific version
   claude plugin install my-plugin@1.2.0
   
   # Clear cache
   claude plugin cache clear
   ```

### Validation Checklist

- [ ] Valid marketplace.json structure
- [ ] All plugin paths exist
- [ ] Plugin versions match tags
- [ ] Dependencies are specified
- [ ] Security manifest included
- [ ] Changelog updated
- [ ] Documentation current
- [ ] Tests passing
- [ ] Code signed
- [ ] Access permissions set