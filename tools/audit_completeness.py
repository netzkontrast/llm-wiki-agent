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

def extract_entities_from_plan(filepath):
    content = filepath.read_text(encoding="utf-8")

    locations = []
    characters = []
    concepts = []

    # State machine to track which section we're in
    current_section = None

    for line in content.split('\n'):
        # Detect sections based on standard plan.md output format
        if re.search(r'^###\s*Locations', line, re.IGNORECASE):
            current_section = 'locations'
            continue
        elif re.search(r'^###\s*Characters', line, re.IGNORECASE):
            current_section = 'characters'
            continue
        elif re.search(r'^###\s*Concepts', line, re.IGNORECASE):
            current_section = 'concepts'
            continue
        elif line.startswith('#'):
            # If it's a heading but not one of ours, stop collecting or skip
            if not any(x in line.lower() for x in ['locations', 'characters', 'concepts']):
                 current_section = None
            continue

        # Extract entity from list item format "- [Entity Name] -> wiki/..."
        # or simple bullet lists "- Entity Name"
        match = re.search(r'^\s*-\s*(?:\[(.*?)\]|(.*?))(?:\s*->|$)', line)
        if match and current_section:
            entity = match.group(1) or match.group(2)
            if entity:
                entity = entity.strip()
                if current_section == 'locations':
                    locations.append(entity)
                elif current_section == 'characters':
                    characters.append(entity)
                elif current_section == 'concepts':
                    concepts.append(entity)

    return locations, characters, concepts

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/audit_completeness.py <plan-file>", file=sys.stderr)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: {filepath} not found.", file=sys.stderr)
        sys.exit(1)

    wiki_titles = get_wiki_titles()
    locations, characters, concepts = extract_entities_from_plan(filepath)

    report = {
        "source": str(filepath),
        "locations": { "found_in_plan": locations, "found_in_wiki": [], "missing": [] },
        "characters": { "found_in_plan": characters, "found_in_wiki": [], "missing": [] },
        "concepts": { "found_in_plan": concepts, "found_in_wiki": [], "missing": [] },
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
