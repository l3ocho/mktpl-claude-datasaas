# CI/CD Integration Guide

Complete guide for automating plugin testing, validation, and deployment.

## GitHub Actions

### Basic Validation Workflow
```yaml
# .github/workflows/validate-plugin.yml
name: Validate Plugin

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Validate plugin manifest
        run: |
          python scripts/validate_manifest.py .claude-plugin/plugin.json
      
      - name: Check JSON syntax
        run: |
          find . -name "*.json" -exec jq . {} \; > /dev/null
      
      - name: Test commands
        run: |
          python scripts/test_commands.py .
      
      - name: Check file permissions
        run: |
          # Ensure hook scripts are executable
          find hooks -name "*.sh" -type f -exec test -x {} \; || exit 1
```

### Advanced Testing Workflow
```yaml
# .github/workflows/test-plugin.yml
name: Test Plugin

on:
  push:
    branches: [main, develop]
  pull_request:

env:
  PLUGIN_NAME: my-plugin

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Lint Markdown
        uses: DavidAnson/markdownlint-cli2-action@v14
        with:
          globs: |
            **/*.md
            !node_modules
      
      - name: Spell Check
        uses: streetsidesoftware/cspell-action@v5
        with:
          files: |
            **/*.md
            **/*.json
  
  test-scripts:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run Python tests
        run: |
          pytest tests/ --cov=scripts --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  test-hooks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Test shell scripts
        run: |
          # Install shellcheck
          sudo apt-get update && sudo apt-get install -y shellcheck
          
          # Check all shell scripts
          find . -name "*.sh" -exec shellcheck {} \;
      
      - name: Test hook execution
        run: |
          # Simulate hook environment
          export CHANGED_FILE="test.py"
          export FILE_EXTENSION="py"
          
          # Test each hook
          for hook in hooks/*.sh; do
            if [ -x "$hook" ]; then
              echo "Testing $hook..."
              timeout 10s "$hook" || echo "Hook $hook failed or timed out"
            fi
          done
  
  integration:
    runs-on: ubuntu-latest
    needs: [lint, test-scripts, test-hooks]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Claude CLI (mock)
        run: |
          # In real scenario, install actual Claude CLI
          echo "Installing Claude CLI..."
      
      - name: Test plugin installation
        run: |
          # Mock test - in reality would use Claude CLI
          echo "Testing plugin installation..."
          
      - name: Test command execution
        run: |
          # Mock test - in reality would test commands
          echo "Testing command execution..."
```

### Release Workflow
```yaml
# .github/workflows/release.yml
name: Release Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate version tag
        run: |
          # Extract version from tag
          VERSION=${GITHUB_REF#refs/tags/v}
          
          # Check manifest version matches
          MANIFEST_VERSION=$(jq -r .version .claude-plugin/plugin.json)
          
          if [ "$VERSION" != "$MANIFEST_VERSION" ]; then
            echo "Tag version ($VERSION) doesn't match manifest ($MANIFEST_VERSION)"
            exit 1
          fi
      
      - name: Create changelog
        id: changelog
        run: |
          # Generate changelog from commits
          git log --pretty=format:"- %s" $(git describe --tags --abbrev=0 HEAD^)..HEAD > CHANGELOG.md
          
      - name: Update marketplace
        run: |
          # Update marketplace.json if it exists
          if [ -f "../marketplace/.claude-plugin/marketplace.json" ]; then
            # Update plugin version in marketplace
            jq --arg v "$VERSION" \
              '.plugins[] | select(.name == "${{ env.PLUGIN_NAME }}").version = $v' \
              ../marketplace/.claude-plugin/marketplace.json > tmp.json
            mv tmp.json ../marketplace/.claude-plugin/marketplace.json
          fi
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          body_path: CHANGELOG.md
          files: |
            .claude-plugin/plugin.json
            README.md
```

## GitLab CI

### Basic Pipeline
```yaml
# .gitlab-ci.yml
stages:
  - validate
  - test
  - deploy

variables:
  PLUGIN_NAME: "my-plugin"

validate:manifest:
  stage: validate
  image: python:3.11
  script:
    - python scripts/validate_manifest.py .claude-plugin/plugin.json
  only:
    - merge_requests
    - main

validate:json:
  stage: validate
  image: stedolan/jq
  script:
    - find . -name "*.json" -exec jq . {} \;
  only:
    - merge_requests
    - main

test:commands:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python scripts/test_commands.py .
  artifacts:
    reports:
      junit: test-results.xml

test:scripts:
  stage: test
  image: python:3.11
  script:
    - pip install pytest pytest-cov
    - pytest tests/ --junitxml=test-results.xml
  coverage: '/TOTAL.*\s+(\d+%)$/'

deploy:marketplace:
  stage: deploy
  image: alpine/git
  script:
    - |
      # Update marketplace repository
      git clone $MARKETPLACE_REPO marketplace
      cd marketplace
      
      # Update plugin entry
      # ... update logic ...
      
      git add .
      git commit -m "Update $PLUGIN_NAME to $CI_COMMIT_TAG"
      git push origin main
  only:
    - tags
```

### Advanced GitLab Pipeline
```yaml
# .gitlab-ci.yml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Code-Quality.gitlab-ci.yml

stages:
  - build
  - test
  - security
  - deploy
  - cleanup

.plugin_template:
  image: node:18
  before_script:
    - npm ci --cache .npm --prefer-offline
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .npm/
      - node_modules/

build:plugin:
  extends: .plugin_template
  stage: build
  script:
    - npm run build
    - tar -czf plugin.tar.gz .
  artifacts:
    paths:
      - plugin.tar.gz
    expire_in: 1 week

test:unit:
  extends: .plugin_template
  stage: test
  script:
    - npm test -- --coverage
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:integration:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $PLUGIN_NAME:test .
    - docker run --rm $PLUGIN_NAME:test npm run test:integration

security:dependencies:
  stage: security
  image: node:18
  script:
    - npm audit --production
  allow_failure: true

deploy:staging:
  stage: deploy
  script:
    - echo "Deploying to staging marketplace..."
  environment:
    name: staging
    url: https://staging.marketplace.example.com
  only:
    - develop

deploy:production:
  stage: deploy
  script:
    - echo "Deploying to production marketplace..."
  environment:
    name: production
    url: https://marketplace.example.com
  only:
    - tags
  when: manual
```

## Jenkins Pipeline

### Jenkinsfile
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        PLUGIN_NAME = 'my-plugin'
        PYTHON = 'python3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Validate') {
            parallel {
                stage('Manifest') {
                    steps {
                        sh '${PYTHON} scripts/validate_manifest.py .claude-plugin/plugin.json'
                    }
                }
                
                stage('JSON Files') {
                    steps {
                        sh 'find . -name "*.json" -exec jq . {} \\;'
                    }
                }
                
                stage('Markdown') {
                    steps {
                        sh 'npx markdownlint-cli2 "**/*.md"'
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    ${PYTHON} -m pip install -r requirements.txt
                    ${PYTHON} -m pytest tests/ --junitxml=test-results.xml
                '''
            }
            
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                sh '''
                    # Run security scans
                    ${PYTHON} -m pip install safety
                    safety check
                    
                    # Check for secrets
                    npx @secretlint/quick-start "**/*"
                '''
            }
        }
        
        stage('Build') {
            when {
                tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
            }
            steps {
                sh '''
                    # Package plugin
                    tar -czf ${PLUGIN_NAME}-${TAG_NAME}.tar.gz .
                '''
                
                archiveArtifacts artifacts: '*.tar.gz'
            }
        }
        
        stage('Deploy') {
            when {
                tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
            }
            steps {
                input message: 'Deploy to marketplace?'
                
                sh '''
                    # Deploy to marketplace
                    echo "Deploying version ${TAG_NAME}"
                '''
            }
        }
    }
    
    post {
        success {
            slackSend(
                color: 'good',
                message: "Plugin ${PLUGIN_NAME} build successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
            )
        }
        
        failure {
            slackSend(
                color: 'danger',
                message: "Plugin ${PLUGIN_NAME} build failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
            )
        }
    }
}
```

## CircleCI Configuration

### .circleci/config.yml
```yaml
version: 2.1

orbs:
  python: circleci/python@2.1.1
  node: circleci/node@5.1.0

executors:
  plugin-executor:
    docker:
      - image: cimg/python:3.11-node
    working_directory: ~/plugin

jobs:
  validate:
    executor: plugin-executor
    steps:
      - checkout
      - run:
          name: Validate Manifest
          command: python scripts/validate_manifest.py .claude-plugin/plugin.json
      - run:
          name: Check JSON
          command: |
            sudo apt-get update && sudo apt-get install -y jq
            find . -name "*.json" -exec jq . {} \;
  
  test:
    executor: plugin-executor
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          pip-dependency-file: requirements.txt
      - run:
          name: Run Tests
          command: |
            pytest tests/ --junitxml=test-results/junit.xml
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: test-results
  
  security:
    executor: plugin-executor
    steps:
      - checkout
      - run:
          name: Security Scan
          command: |
            pip install safety
            safety check
  
  deploy:
    executor: plugin-executor
    steps:
      - checkout
      - run:
          name: Deploy to Marketplace
          command: |
            echo "Deploying to marketplace..."

workflows:
  plugin-pipeline:
    jobs:
      - validate
      - test:
          requires:
            - validate
      - security:
          requires:
            - validate
      - deploy:
          requires:
            - test
            - security
          filters:
            tags:
              only: /^v.*/
            branches:
              ignore: /.*/
```

## Testing Strategies

### Unit Tests
```python
# tests/test_commands.py

import pytest
from pathlib import Path
import json

class TestCommands:
    def test_all_commands_have_metadata(self):
        """Ensure all command files have proper metadata."""
        commands_dir = Path("commands")
        for md_file in commands_dir.rglob("*.md"):
            with open(md_file) as f:
                content = f.read()
            
            assert content.startswith("---"), f"{md_file} missing frontmatter"
            assert "_type: command" in content, f"{md_file} missing _type"
            assert "_command:" in content, f"{md_file} missing _command"
            assert "_description:" in content, f"{md_file} missing _description"
    
    def test_manifest_valid(self):
        """Test plugin manifest is valid."""
        with open(".claude-plugin/plugin.json") as f:
            manifest = json.load(f)
        
        assert "name" in manifest
        assert "version" in manifest
        assert "description" in manifest
        assert "author" in manifest
```

### Integration Tests
```python
# tests/test_integration.py

import subprocess
import tempfile
import shutil
from pathlib import Path

def test_plugin_installation():
    """Test plugin can be installed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy plugin to temp directory
        plugin_dir = Path(tmpdir) / "test-plugin"
        shutil.copytree(".", plugin_dir)
        
        # Mock installation test
        result = subprocess.run(
            ["python", "scripts/validate_manifest.py", 
             str(plugin_dir / ".claude-plugin/plugin.json")],
            capture_output=True
        )
        
        assert result.returncode == 0
```

## Deployment Strategies

### Blue-Green Deployment
```yaml
# Deploy to staging first, then swap
deploy:staging:
  stage: deploy
  script:
    - deploy_to_marketplace staging
    - run_smoke_tests staging
  environment:
    name: staging

deploy:production:
  stage: deploy
  script:
    - swap_marketplace_slots staging production
  when: manual
  only:
    - tags
```

### Canary Releases
```yaml
deploy:canary:
  stage: deploy
  script:
    - |
      # Deploy to 10% of users
      update_marketplace_config canary 0.1
      
      # Monitor for 1 hour
      sleep 3600
      
      # Check metrics
      if check_canary_metrics; then
        update_marketplace_config canary 1.0
      else
        rollback_canary
      fi
```

### Rollback Strategy
```bash
#!/bin/bash
# scripts/rollback.sh

PLUGIN_NAME="my-plugin"
PREVIOUS_VERSION=$(git describe --tags --abbrev=0 HEAD^)

echo "Rolling back $PLUGIN_NAME to $PREVIOUS_VERSION"

# Restore previous version
git checkout "v$PREVIOUS_VERSION"

# Update marketplace
update_marketplace_version "$PLUGIN_NAME" "$PREVIOUS_VERSION"

# Notify team
send_notification "Rolled back $PLUGIN_NAME to $PREVIOUS_VERSION"
```

## Monitoring & Alerts

### Health Checks
```yaml
# monitoring/health_check.yml
checks:
  - name: plugin_availability
    url: https://marketplace.example.com/api/plugins/my-plugin
    interval: 5m
    
  - name: command_execution
    command: claude /my-plugin health-check
    interval: 10m
    
  - name: version_check
    script: |
      CURRENT=$(claude plugin list | grep my-plugin | awk '{print $2}')
      EXPECTED=$(cat .claude-plugin/plugin.json | jq -r .version)
      [ "$CURRENT" = "$EXPECTED" ]
    interval: 1h
```

### Metrics Collection
```python
# scripts/collect_metrics.py

import json
import requests
from datetime import datetime

def collect_plugin_metrics():
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "plugin": "my-plugin",
        "installations": get_installation_count(),
        "daily_active_users": get_dau(),
        "command_usage": get_command_stats(),
        "error_rate": get_error_rate()
    }
    
    # Send to monitoring service
    requests.post(
        "https://metrics.example.com/api/plugins",
        json=metrics
    )
```

## Best Practices

1. **Version Everything**
   - Tag releases with semantic versions
   - Keep changelog updated
   - Version lock dependencies

2. **Automate Testing**
   - Run tests on every commit
   - Block merges without passing tests
   - Include security scanning

3. **Progressive Rollout**
   - Deploy to staging first
   - Use canary releases for major changes
   - Have rollback plan ready

4. **Monitor Everything**
   - Track installation success rate
   - Monitor command execution time
   - Alert on error spikes

5. **Documentation**
   - Update docs with releases
   - Include migration guides
   - Document breaking changes