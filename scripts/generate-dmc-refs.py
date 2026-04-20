#!/usr/bin/env python3
"""
Generate the DMC component registry from llms.json.

Reads DMC_LLMS_JSON_URL from a consumer project's .env, fetches llms.json,
filters components based on .claude/dmc-components.json, and writes:
  - mcp-servers/dmc-design/registry/dmc_{major}_{minor}.json

Usage:
  python scripts/generate-dmc-refs.py --project /path/to/consumer-project
  python scripts/generate-dmc-refs.py --project /path/to/consumer-project --dry-run
  python scripts/generate-dmc-refs.py --project /path/to/consumer-project --verbose
"""
import argparse
import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is required. Install it: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import dotenv_values
except ImportError:
    print("ERROR: 'python-dotenv' is required. Install it: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)

MARKETPLACE_ROOT = Path(__file__).parent.parent
REGISTRY_OUTPUT_DIR = MARKETPLACE_ROOT / "mcp-servers" / "dmc-design" / "registry"

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_project_env(project_path: Path) -> dict[str, str | None]:
    env_file = project_path / ".env"
    if not env_file.exists():
        return {}
    return dict(dotenv_values(env_file))


def load_consumer_config(project_path: Path) -> dict[str, Any]:
    config_file = project_path / ".claude" / "dmc-components.json"
    if not config_file.exists():
        logger.warning(
            f"No .claude/dmc-components.json found in {project_path}. "
            "Generating full library (not recommended for large projects)."
        )
        return {}
    with open(config_file) as f:
        return json.load(f)


def fetch_llms_json(url: str) -> list[dict[str, Any]]:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"ERROR: Failed to fetch llms.json from {url}: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: llms.json is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print(
            f"ERROR: llms.json must be a JSON array, got {type(data).__name__}. "
            "Check that DMC_LLMS_JSON_URL points to the correct endpoint.",
            file=sys.stderr,
        )
        sys.exit(1)

    return data


def filter_components(
    entries: list[dict[str, Any]],
    config: dict[str, Any],
    verbose: bool,
) -> list[dict[str, Any]]:
    wanted_names: set[str] = set(config.get("components", []))
    wanted_cats: set[str] = {c.lower() for c in config.get("categories", [])}

    if not wanted_names and not wanted_cats:
        if verbose:
            logger.setLevel(logging.INFO)
        logger.warning(
            "No component or category filters specified — including all %d entries.",
            len(entries),
        )
        return entries

    matched: list[dict[str, Any]] = []
    for entry in entries:
        name = entry.get("title", entry.get("name", ""))
        cat = (entry.get("category") or "").lower()

        if name in wanted_names or cat in wanted_cats:
            if verbose:
                logger.info("  MATCH  %-30s  category=%s", name, cat or "(none)")
            matched.append(entry)
        else:
            if verbose:
                logger.info("  SKIP   %-30s  category=%s", name, cat or "(none)")

    return matched


def extract_version_from_url(url: str) -> str:
    match = re.search(r"(\d+\.\d+\.\d+)", url)
    return match.group(1) if match else "unknown"


def build_registry(
    matched: list[dict[str, Any]],
    version: str,
    url: str,
    timestamp: str,
) -> dict[str, Any]:
    categories: dict[str, list[str]] = {}
    components: dict[str, dict[str, Any]] = {}

    for entry in matched:
        name = entry.get("title", entry.get("name", ""))
        if not name:
            continue
        cat = (entry.get("category") or "General").lower().replace(" ", "_")

        categories.setdefault(cat, [])
        if name not in categories[cat]:
            categories[cat].append(name)

        props = entry.get("props", {})
        if not isinstance(props, dict):
            props = {}

        components[name] = {
            "description": entry.get("description", f"{name} component"),
            "props": props,
        }

    return {
        "version": version,
        "generated": timestamp,
        "source_url": url,
        "categories": categories,
        "components": components,
    }


def write_registry(
    registry: dict[str, Any],
    version: str,
    output_dir: Path,
    dry_run: bool,
    verbose: bool,
) -> Path:
    if version != "unknown":
        parts = version.split(".")
        if len(parts) >= 2:
            fname = f"dmc_{parts[0]}_{parts[1]}.json"
        else:
            fname = f"dmc_{version}.json"
    else:
        fname = "dmc_generated.json"

    out_path = output_dir / fname

    if dry_run:
        total = sum(len(v) for v in registry["categories"].values())
        print(f"  [dry-run] Would write {out_path} ({total} component(s))")
    else:
        out_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
        if verbose:
            total = sum(len(v) for v in registry["categories"].values())
            logger.info("Wrote %s (%d component(s))", out_path, total)

    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate DMC component registry JSON from llms.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--project",
        metavar="PATH",
        required=True,
        help="Path to the consumer project (must contain .env with DMC_LLMS_JSON_URL)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without writing any files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Log each component matched",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
        logger.setLevel(logging.INFO)

    project_path = Path(args.project).resolve()
    if not project_path.is_dir():
        print(f"ERROR: --project path does not exist or is not a directory: {project_path}", file=sys.stderr)
        sys.exit(1)

    env = load_project_env(project_path)
    url = env.get("DMC_LLMS_JSON_URL")
    if not url:
        print(
            "ERROR: DMC_LLMS_JSON_URL is not set.\n"
            f"Add it to {project_path / '.env'}:\n\n"
            "  DMC_LLMS_JSON_URL=https://www.dash-mantine-components.com/assets/llms.json\n\n"
            "Set the URL to match the DMC version installed in your project's .venv.",
            file=sys.stderr,
        )
        sys.exit(1)

    consumer_config = load_consumer_config(project_path)

    print(f"Fetching llms.json from: {url}")
    entries = fetch_llms_json(url)
    print(f"  {len(entries)} entries found in llms.json")

    matched = filter_components(entries, consumer_config, args.verbose)
    print(f"  {len(matched)} components matched after filtering")

    if not matched:
        print("WARNING: No components matched. Check your .claude/dmc-components.json filters.", file=sys.stderr)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    version = extract_version_from_url(url)

    print()
    if args.dry_run:
        print("[dry-run mode — no files will be written]")
    print("Writing dmc-design component registry:")

    registry = build_registry(matched, version, url, timestamp)
    registry_path = write_registry(registry, version, REGISTRY_OUTPUT_DIR, args.dry_run, args.verbose)

    print()
    print(f"Done. {len(matched)} component(s) matched.")
    print(f"  registry → {registry_path}")


if __name__ == "__main__":
    main()
