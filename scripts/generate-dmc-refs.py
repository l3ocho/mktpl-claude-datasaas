#!/usr/bin/env python3
"""
Generate DMC reference artifacts from llms.json.

Reads DMC_LLMS_JSON_URL from a consumer project's .env, fetches llms.json,
filters components based on .claude/dmc-components.json, and outputs:
  - plugins/drawio-plugin/references/dmc/dmc-{domain}.txt
  - mcp-servers/dmc-design/registry/dmc_{major}_{minor}.json

Output filenames are derived dynamically from DOMAIN_CATEGORY_MAP keys —
no fixed filename list. Adding a new entry to DOMAIN_CATEGORY_MAP automatically
creates a new dmc-{domain}.txt file on the next run.

Usage:
  python scripts/generate-dmc-refs.py --project /path/to/consumer-project
  python scripts/generate-dmc-refs.py --project /path/to/consumer-project --dry-run
  python scripts/generate-dmc-refs.py --project /path/to/consumer-project --verbose
  python scripts/generate-dmc-refs.py --baseline
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

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MARKETPLACE_ROOT = Path(__file__).parent.parent

DMC_TXT_OUTPUT_DIR = MARKETPLACE_ROOT / "plugins" / "drawio-plugin" / "references" / "dmc"
REGISTRY_OUTPUT_DIR = MARKETPLACE_ROOT / "mcp-servers" / "dmc-design" / "registry"

# Map domain file name (without .txt) → list of llms.json category values to include.
# IMPORTANT: Filenames are derived dynamically from these keys. To add a new domain file,
# add a new entry here — no other code changes needed. The key becomes the filename stem
# (e.g., "dmc-charts" → "dmc-charts.txt"). The order here is the order files are written.
DOMAIN_CATEGORY_MAP: dict[str, list[str]] = {
    "dmc-layout":   ["Layout", "layout", "AppShell", "appshell"],
    "dmc-ui":       ["Buttons", "buttons", "Inputs", "inputs", "Navigation", "navigation",
                     "Typography", "typography", "Overlays", "overlays",
                     "Data Display", "data_display", "Misc", "misc"],
    "dmc-charts":   ["Charts", "charts"],
    "dmc-feedback": ["Feedback", "feedback", "Notifications", "notifications", "Dates", "dates"],
    "dmc-theme":    ["General", "general", "Theme", "theme"],
}

# Fallback domain for unmapped categories
DEFAULT_DOMAIN = "dmc-ui"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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
    """
    Filter llms.json entries by component name and/or category.

    config keys (both optional, union of matches):
      components: list[str]  — explicit component names
      categories: list[str]  — category values to include

    If config is empty or both lists are empty, all entries are included.
    """
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


def resolve_domain(entry: dict[str, Any], verbose: bool) -> str:
    """Map an llms.json entry to a domain file name."""
    cat = entry.get("category", "")

    for domain, accepted_cats in DOMAIN_CATEGORY_MAP.items():
        # Case-insensitive match against accepted category strings
        if any(cat.lower() == ac.lower() for ac in accepted_cats):
            return domain

    name = entry.get("title", entry.get("name", ""))
    logger.warning(
        "Component '%s' has unmapped category '%s' — placing in %s. "
        "Update DOMAIN_CATEGORY_MAP in generate-dmc-refs.py to fix.",
        name,
        cat,
        DEFAULT_DOMAIN,
    )
    return DEFAULT_DOMAIN


def build_header(url: str, config_path: str, timestamp: str) -> str:
    return (
        f"# AUTO-GENERATED — DO NOT EDIT MANUALLY\n"
        f"# Source: {url}\n"
        f"# Generated: {timestamp}\n"
        f"# Consumer config: {config_path}\n"
        f"# Regenerate: python scripts/generate-dmc-refs.py --project /path/to/project\n"
    )


def extract_version_from_url(url: str) -> str:
    """
    Try to extract a DMC version from the URL.
    Falls back to 'unknown'.
    e.g. ".../0.14.7/llms.json" → "0.14.7"
    """
    match = re.search(r"(\d+\.\d+\.\d+)", url)
    return match.group(1) if match else "unknown"


def build_registry(
    matched: list[dict[str, Any]],
    version: str,
    url: str,
    timestamp: str,
) -> dict[str, Any]:
    """
    Build a component_registry JSON matching mcp-servers/dmc-design/registry format:
      {version, generated, categories: {cat: [names]}, components: {name: {description, props}}}
    """
    categories: dict[str, list[str]] = {}
    components: dict[str, dict[str, Any]] = {}

    for entry in matched:
        name = entry.get("title", entry.get("name", ""))
        if not name:
            continue
        cat = (entry.get("category") or "General").lower().replace(" ", "_")
        content = entry.get("content", "")

        categories.setdefault(cat, [])
        if name not in categories[cat]:
            categories[cat].append(name)

        # Attempt to extract props from content (best-effort: look for prop tables / JSON blocks).
        # If llms.json provides structured props, use them; otherwise store an empty dict.
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


def write_txt_files(
    matched: list[dict[str, Any]],
    header_fn,
    output_dir: Path,
    dry_run: bool,
    verbose: bool,
) -> int:
    """
    Write per-domain .txt files. Returns number of files written.

    File names are derived from DOMAIN_CATEGORY_MAP keys (e.g., "dmc-layout" → "dmc-layout.txt").
    All domains defined in DOMAIN_CATEGORY_MAP get a file, even if no components matched —
    empty (header-only) files ensure consistent structure and allow discovery by glob.
    """
    domains: dict[str, list[str]] = {d: [] for d in DOMAIN_CATEGORY_MAP}

    for entry in matched:
        domain = resolve_domain(entry, verbose)
        content = entry.get("content", "")
        if content:
            domains.setdefault(domain, []).append(content)

    written = 0
    for domain, blocks in domains.items():
        if not blocks:
            # Write an empty (header-only) file so the file always exists
            blocks = []
        out_path = output_dir / f"{domain}.txt"
        file_content = header_fn() + "\n" + "\n\n".join(blocks) + "\n"
        if dry_run:
            print(f"  [dry-run] Would write {out_path} ({len(blocks)} component(s))")
        else:
            out_path.write_text(file_content, encoding="utf-8")
            if verbose:
                logger.info("Wrote %s (%d component(s))", out_path, len(blocks))
        written += 1

    return written


def write_registry(
    registry: dict[str, Any],
    version: str,
    output_dir: Path,
    dry_run: bool,
    verbose: bool,
) -> Path:
    """Write registry JSON. Returns the path that was (or would be) written."""
    # Filename: dmc_{major}_{minor}.json  (e.g. dmc_0_14.json for 0.14.7)
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


def write_baseline_files(
    output_dir: Path,
    dry_run: bool,
) -> int:
    """
    Write header-only (empty) .txt baseline files for all domains in DOMAIN_CATEGORY_MAP.

    Use this to initialize the references/dmc/ directory before running with --project,
    or to add placeholder files for newly added domains.

    Returns the number of files written.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    written = 0
    for domain in DOMAIN_CATEGORY_MAP:
        out_path = output_dir / f"{domain}.txt"
        header = (
            f"# AUTO-GENERATED — DO NOT EDIT MANUALLY\n"
            f"# Baseline placeholder — run with --project to populate\n"
            f"# Generated: {timestamp}\n"
            f"# Regenerate: python scripts/generate-dmc-refs.py --project /path/to/project\n"
        )
        if dry_run:
            status = "exists" if out_path.exists() else "new"
            print(f"  [dry-run] Would write baseline {out_path} ({status})")
        else:
            out_path.write_text(header + "\n", encoding="utf-8")
        written += 1
    return written


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate DMC reference artifacts from llms.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--project",
        metavar="PATH",
        help="Path to the consumer project (must contain .env with DMC_LLMS_JSON_URL)",
    )
    parser.add_argument(
        "--baseline",
        action="store_true",
        help=(
            "Write empty (header-only) placeholder files for all domains in DOMAIN_CATEGORY_MAP. "
            "Use this to initialize references/dmc/ or add files for newly defined domains. "
            "Does not require --project or network access."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without writing any files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Log each component matched and its domain mapping",
    )
    args = parser.parse_args()

    # --baseline mode: no project required, no network call
    if args.baseline:
        print("Writing baseline (empty) domain files:")
        print(f"  Output dir: {DMC_TXT_OUTPUT_DIR}")
        print(f"  Domains: {', '.join(DOMAIN_CATEGORY_MAP.keys())}")
        if args.dry_run:
            print("[dry-run mode — no files will be written]")
        written = write_baseline_files(DMC_TXT_OUTPUT_DIR, args.dry_run)
        print(f"\nDone. {written} baseline file(s) {'would be ' if args.dry_run else ''}written.")
        return

    if not args.project:
        parser.error("--project is required unless --baseline is specified")

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
        logger.setLevel(logging.INFO)

    project_path = Path(args.project).resolve()
    if not project_path.is_dir():
        print(f"ERROR: --project path does not exist or is not a directory: {project_path}", file=sys.stderr)
        sys.exit(1)

    # 1. Load .env from consumer project
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

    # 2. Load consumer component config
    consumer_config = load_consumer_config(project_path)
    config_path = str(project_path / ".claude" / "dmc-components.json")

    print(f"Fetching llms.json from: {url}")
    entries = fetch_llms_json(url)
    print(f"  {len(entries)} entries found in llms.json")

    # 3. Filter
    matched = filter_components(entries, consumer_config, args.verbose)
    print(f"  {len(matched)} components matched after filtering")

    if not matched:
        print("WARNING: No components matched. Check your .claude/dmc-components.json filters.", file=sys.stderr)

    # 4. Prepare shared metadata
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    version = extract_version_from_url(url)

    def header_fn() -> str:
        return build_header(url, config_path, timestamp)

    print()
    if args.dry_run:
        print("[dry-run mode — no files will be written]")
    print("Writing drawio-plugin domain files:")

    # 5. Write txt domain files
    txt_written = write_txt_files(
        matched, header_fn, DMC_TXT_OUTPUT_DIR, args.dry_run, args.verbose
    )

    print()
    print("Writing dmc-design component registry:")

    # 6. Build and write registry JSON
    registry = build_registry(matched, version, url, timestamp)
    registry_path = write_registry(registry, version, REGISTRY_OUTPUT_DIR, args.dry_run, args.verbose)

    # 7. Summary
    total_components = len(matched)
    total_files = txt_written + 1  # +1 for registry
    print()
    print(f"Done. {total_components} component(s) matched, {total_files} file(s) {'would be ' if args.dry_run else ''}written.")
    print(f"  txt files  → {DMC_TXT_OUTPUT_DIR}/")
    print(f"  registry   → {registry_path}")


if __name__ == "__main__":
    main()
