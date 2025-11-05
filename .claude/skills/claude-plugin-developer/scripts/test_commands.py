#!/usr/bin/env python3
"""
Claude Plugin Command Tester
Automated testing for plugin commands.

Usage:
    python test_commands.py <plugin-directory> [--command <specific-command>]
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Any
import re
import time

class CommandTester:
    def __init__(self, plugin_dir: str):
        self.plugin_dir = Path(plugin_dir)
        self.plugin_name = self._get_plugin_name()
        self.test_results: List[Dict[str, Any]] = []
    
    def _get_plugin_name(self) -> str:
        """Extract plugin name from manifest."""
        manifest_path = self.plugin_dir / ".claude-plugin" / "plugin.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"No plugin.json found at {manifest_path}")
        
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        return manifest.get("name", "unknown")
    
    def discover_commands(self) -> List[str]:
        """Discover all commands in the plugin."""
        commands = []
        commands_dir = self.plugin_dir / "commands"
        
        if not commands_dir.exists():
            return commands
        
        for md_file in commands_dir.rglob("*.md"):
            # Skip index files
            if md_file.name == "_index.md":
                continue
            
            # Extract command from frontmatter
            command = self._extract_command_from_file(md_file)
            if command:
                commands.append(command)
        
        return sorted(commands)
    
    def _extract_command_from_file(self, file_path: Path) -> str:
        """Extract command name from markdown file."""
        with open(file_path) as f:
            content = f.read()
        
        # Look for _command in frontmatter
        match = re.search(r'^_command:\s*(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Fallback to filename
        return file_path.stem
    
    def test_command(self, command: str) -> Dict[str, Any]:
        """Test a specific command."""
        print(f"Testing command: /{self.plugin_name} {command}")
        
        result = {
            "command": command,
            "status": "unknown",
            "tests": []
        }
        
        # Test 1: Check if command file exists
        command_file = self._find_command_file(command)
        if not command_file:
            result["status"] = "failed"
            result["error"] = "Command file not found"
            return result
        
        result["tests"].append({
            "name": "file_exists",
            "passed": True,
            "message": f"Found at {command_file}"
        })
        
        # Test 2: Validate command metadata
        metadata_valid, metadata_errors = self._validate_command_metadata(command_file)
        result["tests"].append({
            "name": "metadata_validation",
            "passed": metadata_valid,
            "errors": metadata_errors
        })
        
        # Test 3: Check for required sections
        sections_valid, missing_sections = self._check_required_sections(command_file)
        result["tests"].append({
            "name": "required_sections",
            "passed": sections_valid,
            "missing": missing_sections
        })
        
        # Test 4: Validate examples
        examples_valid, example_errors = self._validate_examples(command_file)
        result["tests"].append({
            "name": "examples_validation",
            "passed": examples_valid,
            "errors": example_errors
        })
        
        # Test 5: Check for common issues
        issues = self._check_common_issues(command_file)
        result["tests"].append({
            "name": "common_issues",
            "passed": len(issues) == 0,
            "issues": issues
        })
        
        # Determine overall status
        all_passed = all(test["passed"] for test in result["tests"])
        result["status"] = "passed" if all_passed else "failed"
        
        return result
    
    def _find_command_file(self, command: str) -> Path:
        """Find the markdown file for a command."""
        commands_dir = self.plugin_dir / "commands"
        
        # Direct file
        direct = commands_dir / f"{command}.md"
        if direct.exists():
            return direct
        
        # Check subdirectories
        for md_file in commands_dir.rglob("*.md"):
            if self._extract_command_from_file(md_file) == command:
                return md_file
        
        return None
    
    def _validate_command_metadata(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Validate command frontmatter metadata."""
        errors = []
        
        with open(file_path) as f:
            content = f.read()
        
        # Check for frontmatter
        if not content.startswith("---"):
            errors.append("Missing frontmatter")
            return False, errors
        
        # Extract frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append("Invalid frontmatter format")
            return False, errors
        
        frontmatter = parts[1].strip()
        
        # Check required fields
        required_fields = ["_type", "_command", "_description"]
        for field in required_fields:
            if f"{field}:" not in frontmatter:
                errors.append(f"Missing required field: {field}")
        
        # Validate _type
        if "_type: command" not in frontmatter:
            errors.append("_type must be 'command'")
        
        # Validate _description length
        desc_match = re.search(r'^_description:\s*(.+)$', frontmatter, re.MULTILINE)
        if desc_match:
            description = desc_match.group(1).strip()
            if len(description) < 10:
                errors.append("Description too short (min 10 chars)")
            elif len(description) > 100:
                errors.append("Description too long (max 100 chars)")
        
        return len(errors) == 0, errors
    
    def _check_required_sections(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Check for required documentation sections."""
        with open(file_path) as f:
            content = f.read()
        
        # Remove frontmatter
        if content.startswith("---"):
            content = content.split("---", 2)[2]
        
        required_sections = ["Usage", "What it does"]
        missing = []
        
        for section in required_sections:
            # Check for section header
            if not re.search(rf'^#{1,3}\s*{section}', content, re.MULTILINE | re.IGNORECASE):
                missing.append(section)
        
        return len(missing) == 0, missing
    
    def _validate_examples(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Validate command examples."""
        errors = []
        
        with open(file_path) as f:
            content = f.read()
        
        # Look for example section
        example_match = re.search(r'^#{1,3}\s*Examples?.*?(?=^#{1,3}|\Z)', 
                                 content, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        
        if not example_match:
            # Examples are recommended but not required
            return True, []
        
        example_section = example_match.group(0)
        
        # Check for code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', example_section)
        if not code_blocks:
            errors.append("Example section has no code blocks")
        
        # Check that examples use the plugin name
        plugin_ref = f"/{self.plugin_name}"
        if plugin_ref not in example_section:
            errors.append(f"Examples should reference the plugin: {plugin_ref}")
        
        return len(errors) == 0, errors
    
    def _check_common_issues(self, file_path: Path) -> List[str]:
        """Check for common issues in command files."""
        issues = []
        
        with open(file_path) as f:
            content = f.read()
        
        # Check for TODO/FIXME
        if "TODO" in content or "FIXME" in content:
            issues.append("Contains TODO/FIXME markers")
        
        # Check for broken markdown links
        broken_links = re.findall(r'\[([^\]]+)\]\(\s*\)', content)
        if broken_links:
            issues.append(f"Broken markdown links: {broken_links}")
        
        # Check for very long lines
        lines = content.split('\n')
        long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 120]
        if long_lines:
            issues.append(f"Very long lines (>120 chars) at: {long_lines[:3]}...")
        
        # Check for trailing whitespace
        trailing_ws = [i for i, line in enumerate(lines, 1) if line.rstrip() != line]
        if trailing_ws:
            issues.append(f"Trailing whitespace at lines: {trailing_ws[:3]}...")
        
        return issues
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests on all commands."""
        commands = self.discover_commands()
        
        if not commands:
            return {
                "plugin": self.plugin_name,
                "total_commands": 0,
                "passed": 0,
                "failed": 0,
                "results": []
            }
        
        print(f"Found {len(commands)} commands in {self.plugin_name}\n")
        
        results = []
        for command in commands:
            result = self.test_command(command)
            results.append(result)
            
            # Print summary
            status_icon = "✓" if result["status"] == "passed" else "✗"
            print(f"{status_icon} {command}")
            
            # Print failures
            for test in result["tests"]:
                if not test["passed"]:
                    print(f"  - {test['name']}: FAILED")
                    if "errors" in test:
                        for error in test["errors"]:
                            print(f"    • {error}")
                    if "issues" in test:
                        for issue in test["issues"]:
                            print(f"    • {issue}")
            print()
        
        # Summary
        passed = sum(1 for r in results if r["status"] == "passed")
        failed = len(results) - passed
        
        return {
            "plugin": self.plugin_name,
            "total_commands": len(commands),
            "passed": passed,
            "failed": failed,
            "results": results
        }
    
    def generate_report(self, output_file: str = None):
        """Generate a detailed test report."""
        results = self.run_all_tests()
        
        report = f"""# Test Report: {results['plugin']}

## Summary
- Total Commands: {results['total_commands']}
- Passed: {results['passed']}
- Failed: {results['failed']}
- Success Rate: {results['passed'] / max(1, results['total_commands']) * 100:.1f}%

## Detailed Results
"""
        
        for cmd_result in results['results']:
            report += f"\n### Command: `{cmd_result['command']}`\n"
            report += f"Status: **{cmd_result['status'].upper()}**\n\n"
            
            for test in cmd_result['tests']:
                status = "✓" if test['passed'] else "✗"
                report += f"- {status} {test['name'].replace('_', ' ').title()}\n"
                
                if not test['passed']:
                    if 'errors' in test:
                        for error in test['errors']:
                            report += f"  - {error}\n"
                    if 'issues' in test:
                        for issue in test['issues']:
                            report += f"  - {issue}\n"
                    if 'missing' in test:
                        report += f"  - Missing: {', '.join(test['missing'])}\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"\nReport saved to: {output_file}")
        else:
            print("\n" + report)


def main():
    parser = argparse.ArgumentParser(
        description="Test Claude plugin commands"
    )
    parser.add_argument("plugin_dir", help="Path to plugin directory")
    parser.add_argument(
        "--command", 
        help="Test specific command only"
    )
    parser.add_argument(
        "--report", 
        help="Save detailed report to file"
    )
    
    args = parser.parse_args()
    
    try:
        tester = CommandTester(args.plugin_dir)
        
        if args.command:
            # Test single command
            result = tester.test_command(args.command)
            
            if result["status"] == "passed":
                print(f"\n✓ Command '{args.command}' passed all tests")
                sys.exit(0)
            else:
                print(f"\n✗ Command '{args.command}' failed tests")
                sys.exit(1)
        else:
            # Test all commands
            if args.report:
                tester.generate_report(args.report)
            else:
                results = tester.run_all_tests()
                
                print(f"\nOverall Results:")
                print(f"- Commands tested: {results['total_commands']}")
                print(f"- Passed: {results['passed']}")
                print(f"- Failed: {results['failed']}")
                
                sys.exit(0 if results['failed'] == 0 else 1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
