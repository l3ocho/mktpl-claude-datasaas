"""
dbt MCP Tools.

Provides dbt CLI wrapper with pre-execution validation.
"""
import subprocess
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

from .config import load_config

logger = logging.getLogger(__name__)


class DbtTools:
    """dbt CLI wrapper tools with pre-validation"""

    def __init__(self):
        self.config = load_config()
        self.project_dir = self.config.get('dbt_project_dir')
        self.profiles_dir = self.config.get('dbt_profiles_dir')

    def _get_dbt_command(self, cmd: List[str]) -> List[str]:
        """Build dbt command with project and profiles directories"""
        base = ['dbt']
        if self.project_dir:
            base.extend(['--project-dir', self.project_dir])
        if self.profiles_dir:
            base.extend(['--profiles-dir', self.profiles_dir])
        base.extend(cmd)
        return base

    def _run_dbt(
        self,
        cmd: List[str],
        timeout: int = 300,
        capture_json: bool = False
    ) -> Dict:
        """
        Run dbt command and return result.

        Args:
            cmd: dbt subcommand and arguments
            timeout: Command timeout in seconds
            capture_json: If True, parse JSON output

        Returns:
            Dict with command result
        """
        if not self.project_dir:
            return {
                'error': 'dbt project not found',
                'suggestion': 'Set DBT_PROJECT_DIR in project .env or ensure dbt_project.yml exists'
            }

        full_cmd = self._get_dbt_command(cmd)
        logger.info(f"Running: {' '.join(full_cmd)}")

        try:
            env = os.environ.copy()
            # Disable dbt analytics/tracking
            env['DBT_SEND_ANONYMOUS_USAGE_STATS'] = 'false'

            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_dir,
                env=env
            )

            output = {
                'success': result.returncode == 0,
                'command': ' '.join(cmd),
                'stdout': result.stdout,
                'stderr': result.stderr if result.returncode != 0 else None
            }

            if capture_json and result.returncode == 0:
                try:
                    output['data'] = json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass

            return output

        except subprocess.TimeoutExpired:
            return {
                'error': f'Command timed out after {timeout}s',
                'command': ' '.join(cmd)
            }
        except FileNotFoundError:
            return {
                'error': 'dbt not found in PATH',
                'suggestion': 'Install dbt: pip install dbt-core dbt-postgres'
            }
        except Exception as e:
            logger.error(f"dbt command failed: {e}")
            return {'error': str(e)}

    async def dbt_parse(self) -> Dict:
        """
        Validate dbt project without executing (pre-flight check).

        Returns:
            Dict with validation result and any errors
        """
        result = self._run_dbt(['parse'])

        # Check if _run_dbt returned an error (e.g., project not found, timeout, dbt not installed)
        if 'error' in result:
            return result

        if not result.get('success'):
            # Extract useful error info from stderr
            stderr = result.get('stderr', '') or result.get('stdout', '')
            errors = []

            # Look for common dbt 1.9+ deprecation warnings
            if 'deprecated' in stderr.lower():
                errors.append({
                    'type': 'deprecation',
                    'message': 'Deprecated syntax found - check dbt 1.9+ migration guide'
                })

            # Look for compilation errors
            if 'compilation error' in stderr.lower():
                errors.append({
                    'type': 'compilation',
                    'message': 'SQL compilation error - check model syntax'
                })

            return {
                'valid': False,
                'errors': errors,
                'details': stderr[:2000] if stderr else None,
                'suggestion': 'Fix issues before running dbt models'
            }

        return {
            'valid': True,
            'message': 'dbt project validation passed'
        }

    async def dbt_run(
        self,
        select: Optional[str] = None,
        exclude: Optional[str] = None,
        full_refresh: bool = False
    ) -> Dict:
        """
        Run dbt models with pre-validation.

        Args:
            select: Model selection (e.g., "model_name", "+model_name", "tag:daily")
            exclude: Models to exclude
            full_refresh: If True, rebuild incremental models

        Returns:
            Dict with run result
        """
        # ALWAYS validate first
        parse_result = await self.dbt_parse()
        if not parse_result.get('valid'):
            return {
                'error': 'Pre-validation failed',
                **parse_result
            }

        cmd = ['run']
        if select:
            cmd.extend(['--select', select])
        if exclude:
            cmd.extend(['--exclude', exclude])
        if full_refresh:
            cmd.append('--full-refresh')

        return self._run_dbt(cmd)

    async def dbt_test(
        self,
        select: Optional[str] = None,
        exclude: Optional[str] = None
    ) -> Dict:
        """
        Run dbt tests.

        Args:
            select: Test selection
            exclude: Tests to exclude

        Returns:
            Dict with test results
        """
        cmd = ['test']
        if select:
            cmd.extend(['--select', select])
        if exclude:
            cmd.extend(['--exclude', exclude])

        return self._run_dbt(cmd)

    async def dbt_build(
        self,
        select: Optional[str] = None,
        exclude: Optional[str] = None,
        full_refresh: bool = False
    ) -> Dict:
        """
        Run dbt build (run + test) with pre-validation.

        Args:
            select: Model/test selection
            exclude: Resources to exclude
            full_refresh: If True, rebuild incremental models

        Returns:
            Dict with build result
        """
        # ALWAYS validate first
        parse_result = await self.dbt_parse()
        if not parse_result.get('valid'):
            return {
                'error': 'Pre-validation failed',
                **parse_result
            }

        cmd = ['build']
        if select:
            cmd.extend(['--select', select])
        if exclude:
            cmd.extend(['--exclude', exclude])
        if full_refresh:
            cmd.append('--full-refresh')

        return self._run_dbt(cmd)

    async def dbt_compile(
        self,
        select: Optional[str] = None
    ) -> Dict:
        """
        Compile dbt models to SQL without executing.

        Args:
            select: Model selection

        Returns:
            Dict with compiled SQL info
        """
        cmd = ['compile']
        if select:
            cmd.extend(['--select', select])

        return self._run_dbt(cmd)

    async def dbt_ls(
        self,
        select: Optional[str] = None,
        resource_type: Optional[str] = None,
        output: str = 'name'
    ) -> Dict:
        """
        List dbt resources.

        Args:
            select: Resource selection
            resource_type: Filter by type (model, test, seed, snapshot, source)
            output: Output format ('name', 'path', 'json')

        Returns:
            Dict with list of resources
        """
        cmd = ['ls', '--output', output]
        if select:
            cmd.extend(['--select', select])
        if resource_type:
            cmd.extend(['--resource-type', resource_type])

        result = self._run_dbt(cmd)

        if result.get('success') and result.get('stdout'):
            lines = [l.strip() for l in result['stdout'].split('\n') if l.strip()]
            result['resources'] = lines
            result['count'] = len(lines)

        return result

    async def dbt_docs_generate(self) -> Dict:
        """
        Generate dbt documentation.

        Returns:
            Dict with generation result
        """
        result = self._run_dbt(['docs', 'generate'])

        if result.get('success') and self.project_dir:
            # Check for generated catalog
            catalog_path = Path(self.project_dir) / 'target' / 'catalog.json'
            manifest_path = Path(self.project_dir) / 'target' / 'manifest.json'
            result['catalog_generated'] = catalog_path.exists()
            result['manifest_generated'] = manifest_path.exists()

        return result

    async def dbt_lineage(self, model: str) -> Dict:
        """
        Get model dependencies and lineage.

        Args:
            model: Model name to analyze

        Returns:
            Dict with upstream and downstream dependencies
        """
        if not self.project_dir:
            return {'error': 'dbt project not found'}

        manifest_path = Path(self.project_dir) / 'target' / 'manifest.json'

        # Generate manifest if not exists
        if not manifest_path.exists():
            compile_result = await self.dbt_compile(select=model)
            if not compile_result.get('success'):
                return {
                    'error': 'Failed to compile manifest',
                    'details': compile_result
                }

        if not manifest_path.exists():
            return {
                'error': 'Manifest not found',
                'suggestion': 'Run dbt compile first'
            }

        try:
            with open(manifest_path) as f:
                manifest = json.load(f)

            # Find the model node
            model_key = None
            for key in manifest.get('nodes', {}):
                if key.endswith(f'.{model}') or manifest['nodes'][key].get('name') == model:
                    model_key = key
                    break

            if not model_key:
                return {
                    'error': f'Model not found: {model}',
                    'available_models': [
                        n.get('name') for n in manifest.get('nodes', {}).values()
                        if n.get('resource_type') == 'model'
                    ][:20]
                }

            node = manifest['nodes'][model_key]

            # Get upstream (depends_on)
            upstream = node.get('depends_on', {}).get('nodes', [])

            # Get downstream (find nodes that depend on this one)
            downstream = []
            for key, other_node in manifest.get('nodes', {}).items():
                deps = other_node.get('depends_on', {}).get('nodes', [])
                if model_key in deps:
                    downstream.append(key)

            return {
                'model': model,
                'unique_id': model_key,
                'materialization': node.get('config', {}).get('materialized'),
                'schema': node.get('schema'),
                'database': node.get('database'),
                'upstream': upstream,
                'downstream': downstream,
                'description': node.get('description'),
                'tags': node.get('tags', [])
            }

        except Exception as e:
            logger.error(f"dbt_lineage failed: {e}")
            return {'error': str(e)}
