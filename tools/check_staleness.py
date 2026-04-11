#!/usr/bin/env python3
"""
Staleness Detection Script for LLM Wiki.

Usage:
    python tools/check_staleness.py

This script traverses `informs:` chains to detect stale pages. A page is considered stale
if its `last_updated` date is older than any of the pages that inform it (either directly
or transitively).
"""

import sys
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def all_wiki_pages() -> list[Path]:
    return [p for p in WIKI_DIR.rglob("*.md")
            if p.name not in ("index.md", "log.md", "overview.md", "lint-report.md", "README.md")]

def extract_yaml_frontmatter(content: str) -> dict:
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    yaml_str = match.group(1)

    data = {}
    for line in yaml_str.split('\n'):
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()

        if val.startswith('[') and val.endswith(']'):
            inner = val[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                data[key] = [item.strip().strip('"\'') for item in inner.split(',')]
        else:
            data[key] = val.strip('"\'')
    return data

def main():
    pages = all_wiki_pages()

    # Build graph and dates map
    dates_map = {}
    informs_graph = {} # source slug -> list of target slugs
    slug_to_path = {}

    print("Parsing frontmatter for staleness check...")

    for p in pages:
        fm = extract_yaml_frontmatter(read_file(p))
        slug = p.stem
        slug_to_path[slug] = p

        last_updated_str = fm.get("last_updated")
        if last_updated_str:
            try:
                dates_map[slug] = datetime.strptime(last_updated_str, "%Y-%m-%d").date()
            except ValueError:
                dates_map[slug] = None
        else:
            dates_map[slug] = None

        targets = fm.get("informs", [])
        if isinstance(targets, list):
             informs_graph[slug] = [t.split('/')[-1] for t in targets]

    stale_reports = []

    # Traverse informs chains
    def traverse(current_slug, chain, origin_date, origin_slug):
        targets = informs_graph.get(current_slug, [])
        for t in targets:
            if t in chain: # cycle detected
                 continue

            target_date = dates_map.get(t)
            if target_date is None:
                 continue

            if origin_date and origin_date > target_date:
                 stale_reports.append((t, origin_slug, chain + [t]))

            # Continue traversing
            traverse(t, chain + [t], origin_date, origin_slug)

    for slug, date in dates_map.items():
        if date is not None:
             traverse(slug, [slug], date, slug)

    # Deduplicate reports
    deduped = {}
    for target, origin, chain in stale_reports:
         key = (target, origin)
         if key not in deduped:
             deduped[key] = chain

    if deduped:
         print(f"\nFound {len(deduped)} stale relationships:")
         for (target, origin), chain in deduped.items():
              chain_str = " -> ".join(chain)
              print(f" - {target} is stale (informed by newer {origin})")
              print(f"   Chain: {chain_str}")
         sys.exit(1)
    else:
         print("\nNo stale pages found.")
         sys.exit(0)

if __name__ == "__main__":
    main()
