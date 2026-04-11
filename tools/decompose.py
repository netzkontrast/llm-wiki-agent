#!/usr/bin/env python3
import sys
import re
import subprocess
from pathlib import Path

def run_qmd_search(name):
    # Fallback to stub behavior for the test env if qmd is not real
    try:
        result = subprocess.run(
            ["qmd", "search", f'"{name}"', "--files", "--min-score", "0.4"],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.strip()
        if "qmd stub" in output:
            return False, [] # Mock not found
        return len(output) > 0, output.split('\n')
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, []

def main():
    if len(sys.argv) < 2:
        print("Usage: decompose.py <path-to-raw-file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: {filepath} not found.")
        sys.exit(1)

    content = filepath.read_text(encoding="utf-8")

    # Heuristics for page types
    layers_touched = set(["knowledge"])
    if "character" in content.lower() or "said" in content.lower():
        layers_touched.add("narrative")
    if "location" in content.lower() or "place" in content.lower():
        layers_touched.add("narrative")
    if "foreshadow" in content.lower() or "reader" in content.lower():
        layers_touched.add("reader_state")

    # Detect locations/items: numbered bold items `^- \*\*[0-9]+\.`
    # Detect characters/entities: bold proper nouns `\*\*[A-Z][a-zA-Z\s-]+\*\*`
    # Detect concept categories: section headers `^## ` and `^# `

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
        # ignore general headers that are likely not concepts
        if item.lower() not in ["summary", "overview", "introduction", "conclusion"]:
            concepts.add(item)

    all_found_entities = locations_items.union(characters_entities).union(concepts)

    known_entities = []
    new_locations = []
    new_characters = []
    new_concepts = []

    for item in locations_items:
        is_known, _ = run_qmd_search(item)
        if is_known:
            known_entities.append(item)
        else:
            new_locations.append(item)

    for item in characters_entities:
        is_known, _ = run_qmd_search(item)
        if is_known:
            known_entities.append(item)
        else:
            new_characters.append(item)

    for item in concepts:
        is_known, _ = run_qmd_search(item)
        if is_known:
            known_entities.append(item)
        else:
            new_concepts.append(item)

    # Note: If an entity overlaps categories it might be classified randomly based on iteration order
    # above, but sets prevent duplicates per category. We can refine if needed, but this is a good start.

    print(f"## Ingest Plan: {filepath.name}")
    print("### Known entities (merge, do not overwrite)")
    for entity in known_entities:
        print(f"- {entity} → wiki/narrative/characters/{entity}.md  [layer: narrative]") # Using generic known layer message

    print("### New entities (create)")
    for entity in new_locations:
        print(f"- {entity} → wiki/narrative/locations/{entity}.md  [layer: narrative]")
    for entity in new_characters:
        print(f"- {entity} → wiki/narrative/characters/{entity}.md  [layer: narrative]")
    for entity in new_concepts:
        print(f"- {entity} → wiki/knowledge/concepts/{entity}.md  [layer: knowledge]")

    print("### Layers touched")
    print(f"- [{'x' if 'knowledge' in layers_touched else ' '}] knowledge")
    print(f"- [{'x' if 'narrative' in layers_touched else ' '}] narrative")
    print(f"- [{'x' if 'reader_state' in layers_touched else ' '}] reader_state")

    print("### Suggested minimal context (qmd per layer)")
    if known_entities:
        print(f"- qmd search \"{known_entities[0]}\" -c narrative")

    print("\n## Summary")
    print(f"Locations found: {len(new_locations)}")
    print(f"Characters found: {len(new_characters)}")
    print(f"Concepts found: {len(new_concepts)}")
    total_entities = len(new_locations) + len(new_characters) + len(new_concepts)
    print(f"TOTAL entities: {total_entities}", end="")
    if total_entities > 10:
        print("  → batch processing recommended (>10)")
    else:
        print("")

    if total_entities > 10:
        print("\nWARNING: High entity count detected. Batch processing mode is required.")

if __name__ == "__main__":
    main()
