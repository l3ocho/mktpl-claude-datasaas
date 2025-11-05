#!/usr/bin/env python3
"""
Claude Plugin Manifest Validator
Validates plugin.json files against the official schema.

Usage:
    python validate_manifest.py <path-to-plugin.json>
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any

class ManifestValidator:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, manifest_path: str) -> Tuple[bool, List[str], List[str]]:
        """Validate a plugin manifest file."""
        self.errors = []
        self.warnings = []
        
        # Check if file exists
        path = Path(manifest_path)
        if not path.exists():
            self.errors.append(f"File not found: {manifest_path}")
            return False, self.errors, self.warnings
        
        # Load and parse JSON
        try:
            with open(path, 'r') as f:
                manifest = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False, self.errors, self.warnings
        
        # Validate required fields
        self._validate_required_fields(manifest)
        
        # Validate field formats
        if "name" in manifest:
            self._validate_name(manifest["name"])
        
        if "version" in manifest:
            self._validate_version(manifest["version"])
        
        if "description" in manifest:
            self._validate_description(manifest["description"])
        
        if "author" in manifest:
            self._validate_author(manifest["author"])
        
        # Validate optional fields
        if "dependencies" in manifest:
            self._validate_dependencies(manifest["dependencies"])
        
        if "config" in manifest:
            self._validate_config(manifest["config"])
        
        if "permissions" in manifest:
            self._validate_permissions(manifest["permissions"])
        
        if "keywords" in manifest:
            self._validate_keywords(manifest["keywords"])
        
        # Check for unknown fields
        self._check_unknown_fields(manifest)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_required_fields(self, manifest: Dict[str, Any]):
        """Check for required fields."""
        required_fields = ["name", "version", "description", "author"]
        
        for field in required_fields:
            if field not in manifest:
                self.errors.append(f"Missing required field: {field}")
    
    def _validate_name(self, name: str):
        """Validate plugin name format."""
        if not isinstance(name, str):
            self.errors.append("Name must be a string")
            return
        
        if len(name) < 2 or len(name) > 40:
            self.errors.append("Name must be between 2 and 40 characters")
        
        pattern = r"^[a-z][a-z0-9-]*[a-z0-9]$"
        if not re.match(pattern, name):
            self.errors.append(
                "Name must start with lowercase letter, "
                "contain only lowercase letters, numbers, and hyphens, "
                "and not end with a hyphen"
            )
        
        if "--" in name:
            self.errors.append("Name cannot contain consecutive hyphens")
    
    def _validate_version(self, version: str):
        """Validate semantic version format."""
        if not isinstance(version, str):
            self.errors.append("Version must be a string")
            return
        
        # Basic semver pattern
        pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
        if not re.match(pattern, version):
            self.errors.append(
                "Version must follow semantic versioning (e.g., 1.0.0)"
            )
    
    def _validate_description(self, description: str):
        """Validate description field."""
        if not isinstance(description, str):
            self.errors.append("Description must be a string")
            return
        
        if len(description) > 200:
            self.errors.append("Description must be 200 characters or less")
        
        if len(description) < 10:
            self.warnings.append("Description should be at least 10 characters")
    
    def _validate_author(self, author: Any):
        """Validate author field."""
        if isinstance(author, str):
            # Legacy format - just a name
            self.warnings.append(
                "Author as string is deprecated. "
                "Use object format: {\"name\": \"...\", \"email\": \"...\"}"
            )
        elif isinstance(author, dict):
            if "name" not in author:
                self.errors.append("Author object must have 'name' field")
            elif not isinstance(author["name"], str):
                self.errors.append("Author name must be a string")
            
            if "email" in author:
                if not isinstance(author["email"], str):
                    self.errors.append("Author email must be a string")
                elif not self._is_valid_email(author["email"]):
                    self.errors.append("Invalid email format")
            
            if "url" in author:
                if not isinstance(author["url"], str):
                    self.errors.append("Author url must be a string")
                elif not self._is_valid_url(author["url"]):
                    self.errors.append("Invalid URL format")
        else:
            self.errors.append("Author must be string or object")
    
    def _validate_dependencies(self, dependencies: Dict[str, Any]):
        """Validate dependencies field."""
        if not isinstance(dependencies, dict):
            self.errors.append("Dependencies must be an object")
            return
        
        for dep, version in dependencies.items():
            if not isinstance(dep, str):
                self.errors.append(f"Dependency key must be string: {dep}")
            
            if not isinstance(version, str):
                self.errors.append(
                    f"Dependency version must be string: {dep}"
                )
            else:
                # Basic version constraint validation
                if not re.match(r"^[><=~^]", version) and not re.match(r"^\d", version):
                    self.warnings.append(
                        f"Unusual version constraint for {dep}: {version}"
                    )
    
    def _validate_config(self, config: Dict[str, Any]):
        """Validate config field."""
        if not isinstance(config, dict):
            self.errors.append("Config must be an object")
            return
        
        # Validate known config options
        if "default_shell" in config:
            if config["default_shell"] not in ["bash", "sh", "zsh", "fish"]:
                self.warnings.append(
                    f"Unusual shell: {config['default_shell']}"
                )
        
        if "timeout" in config:
            if not isinstance(config["timeout"], (int, float)):
                self.errors.append("Config timeout must be a number")
            elif config["timeout"] <= 0:
                self.errors.append("Config timeout must be positive")
        
        if "environment" in config:
            if not isinstance(config["environment"], dict):
                self.errors.append("Config environment must be an object")
    
    def _validate_permissions(self, permissions: Dict[str, Any]):
        """Validate permissions field."""
        if not isinstance(permissions, dict):
            self.errors.append("Permissions must be an object")
            return
        
        valid_permissions = {
            "file_access": ["read", "write", "execute"],
            "network_access": [True, False],
            "shell_access": [True, False],
            "env_access": list  # List of patterns
        }
        
        for perm, value in permissions.items():
            if perm not in valid_permissions:
                self.warnings.append(f"Unknown permission: {perm}")
                continue
            
            expected = valid_permissions[perm]
            if isinstance(expected, list) and not isinstance(value, type(expected[0])):
                if expected == list:
                    self.errors.append(f"Permission {perm} must be a list")
                else:
                    self.errors.append(
                        f"Permission {perm} must be one of: {expected}"
                    )
    
    def _validate_keywords(self, keywords: List[str]):
        """Validate keywords field."""
        if not isinstance(keywords, list):
            self.errors.append("Keywords must be an array")
            return
        
        for keyword in keywords:
            if not isinstance(keyword, str):
                self.errors.append("All keywords must be strings")
            elif len(keyword) > 20:
                self.warnings.append(
                    f"Keyword too long (max 20 chars): {keyword}"
                )
    
    def _check_unknown_fields(self, manifest: Dict[str, Any]):
        """Check for unknown fields."""
        known_fields = {
            "name", "version", "description", "author", "license",
            "keywords", "homepage", "repository", "bugs", "dependencies",
            "config", "permissions", "scripts", "engines"
        }
        
        unknown_fields = set(manifest.keys()) - known_fields
        for field in unknown_fields:
            self.warnings.append(f"Unknown field: {field}")
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if email format is valid."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL format is valid."""
        pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        return bool(re.match(pattern, url))


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_manifest.py <path-to-plugin.json>")
        sys.exit(1)
    
    manifest_path = sys.argv[1]
    validator = ManifestValidator()
    
    print(f"Validating: {manifest_path}\n")
    
    is_valid, errors, warnings = validator.validate(manifest_path)
    
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  ✗ {error}")
        print()
    
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        print()
    
    if is_valid:
        print("✓ Manifest is valid")
        sys.exit(0)
    else:
        print("✗ Manifest validation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
