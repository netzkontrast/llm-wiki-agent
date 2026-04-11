#!/usr/bin/env python3
import sys
import re
import json
from pathlib import Path

def normalize_title(title):
    # Lowercase, strip punctuation, collapse spaces
    title = title.lower()
    title = re.sub(r'[^\w\s]', '', title)
    return re.sub(r'\s+', ' ', title).strip()

def get_wiki_titles():
    wiki_dir = Path("wiki")
    if not wiki_dir.exists():
        return set()

    titles = set()
    for filepath in wiki_dir.rglob("*.md"):
        # Add filename without extension
        titles.add(normalize_title(filepath.stem))

        # Check frontmatter title
        content = filepath.read_text(encoding="utf-8")
        match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        if match:
            titles.add(normalize_title(match.group(1)))

    return titles

def extract_entities_from_source(filepath):
    content = filepath.read_text(encoding="utf-8")

    locations_items = set()
    for match in re.finditer(r'^\s*-\s*\*\*([0-9]+\.\s*.*?)\*\*', content, re.MULTILINE):
        item = re.sub(r'^[0-9]+\.\s*', '', match.group(1)).strip()
        if item:
            locations_items.add(item)

    characters_entities = set()
    for match in re.finditer(r'\*\*([A-Z][a-zA-Z\s-]+)\*\*', content):
        item = match.group(1).strip()
        if item:
            characters_entities.add(item)

    concepts = set()
    for match in re.finditer(r'^(?:#|##)\s+(.+)$', content, re.MULTILINE):
        item = match.group(1).strip()
        if item.lower() not in ["summary", "overview", "introduction", "conclusion"]:
            concepts.add(item)

    return list(locations_items), list(characters_entities), list(concepts)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/audit_completeness.py <source-file>", file=sys.stderr)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: {filepath} not found.", file=sys.stderr)
        sys.exit(1)

    wiki_titles = get_wiki_titles()
    locations, characters, concepts = extract_entities_from_source(filepath)

    report = {
        "source": str(filepath),
        "locations": { "found_in_source": locations, "found_in_wiki": [], "missing": [] },
        "characters": { "found_in_source": characters, "found_in_wiki": [], "missing": [] },
        "concepts": { "found_in_source": concepts, "found_in_wiki": [], "missing": [] },
        "total_missing": 0
    }

    for item in locations:
        if normalize_title(item) in wiki_titles:
            report["locations"]["found_in_wiki"].append(item)
        else:
            report["locations"]["missing"].append(item)

    for item in characters:
        if normalize_title(item) in wiki_titles:
            report["characters"]["found_in_wiki"].append(item)
        else:
            report["characters"]["missing"].append(item)

    for item in concepts:
        if normalize_title(item) in wiki_titles:
            report["concepts"]["found_in_wiki"].append(item)
        else:
            report["concepts"]["missing"].append(item)

    report["total_missing"] = (
        len(report["locations"]["missing"]) +
        len(report["characters"]["missing"]) +
        len(report["concepts"]["missing"])
    )

    print(json.dumps(report, indent=2))

    if report["total_missing"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
