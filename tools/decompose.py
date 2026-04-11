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

    # Heuristic 1: Extract candidate entity names (capitalized terms, not at start of sentence, or headers)
    # This is a simple regex for demonstration.
    words = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', content)
    words = list(set([w for w in words if w.lower() not in ['the', 'a', 'an', 'in', 'on', 'and', 'or', 'but']]))

    known_entities = []
    new_entities = []

    for word in words:
        is_known, _ = run_qmd_search(word)
        if is_known:
            known_entities.append(word)
        else:
            if len(word) > 3: # arbitrary filter to prevent too many new entities
                new_entities.append(word)

    # Heuristics for page types
    layers_touched = set(["knowledge"])
    if "character" in content.lower() or "said" in content.lower():
        layers_touched.add("narrative")
    if "location" in content.lower() or "place" in content.lower():
        layers_touched.add("narrative")
    if "foreshadow" in content.lower() or "reader" in content.lower():
        layers_touched.add("reader_state")

    print(f"## Ingest Plan: {filepath.name}")
    print("### Known entities (merge, do not overwrite)")
    for entity in known_entities:
        print(f"- {entity} → wiki/narrative/characters/{entity}.md  [layer: narrative]")

    print("### New entities (create)")
    for entity in new_entities[:5]: # Cap at 5 for the plan to keep it readable
        print(f"- {entity} → wiki/knowledge/concepts/{entity}.md  [layer: knowledge]")

    print("### Layers touched")
    print(f"- [{'x' if 'knowledge' in layers_touched else ' '}] knowledge")
    print(f"- [{'x' if 'narrative' in layers_touched else ' '}] narrative")
    print(f"- [{'x' if 'reader_state' in layers_touched else ' '}] reader_state")

    print("### Suggested minimal context (qmd per layer)")
    if known_entities:
        print(f"- qmd search \"{known_entities[0]}\" -c narrative")

if __name__ == "__main__":
    main()
