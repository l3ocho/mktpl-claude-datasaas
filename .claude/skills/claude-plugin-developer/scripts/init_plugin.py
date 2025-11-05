#!/usr/bin/env python3
"""
Claude Plugin Initializer
Creates a new plugin with proper structure and example files.

Usage:
    python init_plugin.py <plugin-name> [--path <output-dir>]
"""

import os
import sys
import json
import argparse
from pathlib import Path

def create_plugin_structure(plugin_name: str, output_path: str = "."):
    """Create a new plugin with standard structure."""
    
    # Validate plugin name
    if not plugin_name.replace("-", "").replace("_", "").isalnum():
        print(f"Error: Plugin name must be alphanumeric with hyphens or underscores")
        return False
    
    # Create plugin directory
    plugin_dir = Path(output_path) / plugin_name
    if plugin_dir.exists():
        print(f"Error: Directory {plugin_dir} already exists")
        return False
    
    # Create directory structure
    directories = [
        plugin_dir / ".claude-plugin",
        plugin_dir / "commands",
        plugin_dir / "agents",
        plugin_dir / "hooks",
        plugin_dir / "scripts",
        plugin_dir / "docs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Create plugin.json
    plugin_manifest = {
        "name": plugin_name,
        "version": "1.0.0",
        "description": f"Description for {plugin_name}",
        "author": {
            "name": "Your Name",
            "email": "your.email@example.com"
        },
        "license": "MIT",
        "keywords": [],
        "config": {
            "default_shell": "bash"
        }
    }
    
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    with open(manifest_path, "w") as f:
        json.dump(plugin_manifest, f, indent=2)
    
    # Create example command
    example_command = f"""---
_type: command
_command: hello
_description: Example command that greets the user
---

# Hello Command

This is an example command for the {plugin_name} plugin.

## Usage

```
/{plugin_name} hello
```

## What it does

This command demonstrates the basic structure of a plugin command.
It will greet the user and show the current time.

## Example

User: `/{plugin_name} hello`

Response: Hello from {plugin_name}! The current time is [current time].
"""
    
    with open(plugin_dir / "commands" / "hello.md", "w") as f:
        f.write(example_command)
    
    # Create example agent
    example_agent = f"""---
_type: agent
_name: {plugin_name}-assistant
_description: Example agent for the {plugin_name} plugin
---

# {plugin_name.replace("-", " ").title()} Assistant

You are a specialized assistant for the {plugin_name} plugin.

## Your Role

- Help users understand how to use the {plugin_name} plugin
- Provide guidance on best practices
- Assist with troubleshooting common issues

## Guidelines

1. Always be helpful and concise
2. Provide code examples when appropriate
3. Reference the plugin documentation when needed
"""
    
    with open(plugin_dir / "agents" / f"{plugin_name}-assistant.md", "w") as f:
        f.write(example_agent)
    
    # Create example hook configuration
    hooks_config = {
        "hooks": [
            {
                "event": "file-changed",
                "pattern": f"**/*.{plugin_name}",
                "script": "hooks/process_file.sh",
                "description": f"Process {plugin_name} files when changed"
            }
        ]
    }
    
    with open(plugin_dir / "hooks" / "hooks.json", "w") as f:
        json.dump(hooks_config, f, indent=2)
    
    # Create example hook script
    hook_script = f"""#!/bin/bash
# Process {plugin_name} files when changed

set -e

FILE_PATH="${{CHANGED_FILE}}"
FILE_EXTENSION="${{FILE_EXTENSION}}"

echo "Processing ${{FILE_PATH}}..."

# Add your processing logic here
# Example: validate file format, run linter, etc.

echo "✓ Successfully processed ${{FILE_PATH}}"
"""
    
    hook_script_path = plugin_dir / "hooks" / "process_file.sh"
    with open(hook_script_path, "w") as f:
        f.write(hook_script)
    
    # Make hook script executable
    os.chmod(hook_script_path, 0o755)
    
    # Create README
    readme_content = f"""# {plugin_name.replace("-", " ").title()}

## Description

{plugin_name} is a Claude plugin that [describe what your plugin does].

## Installation

```bash
claude plugin install {plugin_name}
```

## Commands

- `/{plugin_name} hello` - Example greeting command

## Configuration

This plugin supports the following configuration options:

- `example_option`: Description of the option

## Development

### Testing

```bash
# Test the plugin locally
claude --debug plugin install file://$(pwd)
```

### Contributing

[Add contribution guidelines here]

## License

MIT
"""
    
    with open(plugin_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    # Create .gitignore
    gitignore_content = """# Dependencies
node_modules/
__pycache__/
*.pyc

# Build outputs
dist/
build/
*.egg-info/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Logs
*.log
logs/

# Test coverage
coverage/
.coverage
"""
    
    with open(plugin_dir / ".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print(f"✓ Created plugin structure at: {plugin_dir}")
    print(f"\nNext steps:")
    print(f"1. cd {plugin_dir}")
    print(f"2. Edit .claude-plugin/plugin.json with your plugin details")
    print(f"3. Add your commands to the commands/ directory")
    print(f"4. Test with: claude --debug plugin install file://$(pwd)")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude plugin with standard structure"
    )
    parser.add_argument("plugin_name", help="Name of the plugin (kebab-case)")
    parser.add_argument(
        "--path", 
        default=".", 
        help="Output directory (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Validate plugin name format
    if not args.plugin_name.replace("-", "").isalnum():
        print("Error: Plugin name must contain only letters, numbers, and hyphens")
        sys.exit(1)
    
    success = create_plugin_structure(args.plugin_name, args.path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
