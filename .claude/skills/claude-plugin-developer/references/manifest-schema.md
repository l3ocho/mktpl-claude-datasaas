# Plugin Manifest Schema

Complete JSON schema reference for `.claude-plugin/plugin.json` files.

## Required Fields

### Basic Information
```json
{
  "name": "string",
  "version": "string",
  "description": "string",
  "author": {
    "name": "string",
    "email": "string (optional)",
    "url": "string (optional)"
  }
}
```

### Field Specifications

#### name
- **Type**: string
- **Pattern**: `^[a-z][a-z0-9-]*$`
- **Description**: Plugin identifier in kebab-case
- **Example**: `"deploy-tools"`

#### version
- **Type**: string
- **Format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Example**: `"1.0.0"`

#### description
- **Type**: string
- **Max length**: 200 characters
- **Purpose**: Brief explanation of plugin functionality

#### author
- **Type**: object
- **Required**: name field
- **Optional**: email, url fields

## Optional Fields

### Dependencies
```json
{
  "dependencies": {
    "node": ">=18.0.0",
    "python": ">=3.9",
    "docker": ">=20.0.0"
  }
}
```

### Configuration
```json
{
  "config": {
    "default_shell": "bash",
    "require_safety_check": true,
    "environment": {
      "NODE_ENV": "production",
      "PLUGIN_HOME": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

### Permissions
```json
{
  "permissions": {
    "file_access": ["read", "write"],
    "network_access": true,
    "shell_access": true
  }
}
```

### Scripts
```json
{
  "scripts": {
    "install": "npm install",
    "test": "npm test",
    "build": "npm run build"
  }
}
```

## Complete Example

```json
{
  "name": "deploy-automation",
  "version": "2.1.0",
  "description": "Automated deployment tools for cloud platforms",
  "author": {
    "name": "Hyper Hive Labs",
    "email": "plugins@hyperhivelabs.com",
    "url": "https://hyperhivelabs.com"
  },
  "license": "MIT",
  "keywords": ["deployment", "automation", "cloud", "devops"],
  "homepage": "https://github.com/hyperhivelabs/deploy-automation",
  "repository": {
    "type": "git",
    "url": "https://github.com/hyperhivelabs/deploy-automation.git"
  },
  "bugs": {
    "url": "https://github.com/hyperhivelabs/deploy-automation/issues"
  },
  "dependencies": {
    "node": ">=18.0.0",
    "aws-cli": ">=2.0.0",
    "terraform": ">=1.0.0"
  },
  "config": {
    "default_shell": "bash",
    "require_safety_check": true,
    "timeout": 300,
    "environment": {
      "DEPLOY_ENV": "production",
      "LOG_LEVEL": "info"
    }
  },
  "permissions": {
    "file_access": ["read", "write"],
    "network_access": true,
    "shell_access": true,
    "env_access": ["AWS_*", "DEPLOY_*"]
  },
  "scripts": {
    "install": "./scripts/install.sh",
    "test": "./scripts/test.sh",
    "validate": "./scripts/validate.sh"
  }
}
```

## Validation Rules

### Name Validation
- Must start with lowercase letter
- Can contain lowercase letters, numbers, hyphens
- Cannot end with hyphen
- Cannot contain consecutive hyphens
- Length: 2-40 characters

### Version Validation
- Must follow semantic versioning
- Format: `MAJOR.MINOR.PATCH`
- Optional pre-release: `-alpha`, `-beta`, `-rc.1`
- Optional build metadata: `+build.123`

### Description Validation
- Required field
- Maximum 200 characters
- Should describe what the plugin does
- Should include primary use cases

### Author Validation
- Name is required
- Email must be valid format if provided
- URL must be valid HTTP(S) URL if provided

## Security Considerations

### Restricted Fields
These fields require special marketplace approval:
```json
{
  "privileged": true,
  "system_access": true,
  "unrestricted_network": true
}
```

### Environment Variables
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin paths
- Never hardcode sensitive data
- Document all required env vars

### Path Resolution
- All paths relative to plugin root
- No parent directory traversal (`../`)
- No absolute paths unless documented

## Migration Guide

### From v1 to v2
- Add `author` object (previously string)
- Update `dependencies` format
- Add `permissions` field

### Legacy Support
- Old manifests auto-upgraded
- Deprecation warnings shown
- Grace period: 6 months