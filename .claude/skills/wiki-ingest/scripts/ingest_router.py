#!/usr/bin/env python3
import sys
import os
import shutil
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: ingest_router.py <file_path>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File {filepath} does not exist.")
        sys.exit(1)

    # Implement routing logic L0, L1
    l0_dir = Path("memory/L0_facts")
    l1_dir = Path("memory/L1_episodes")

    l0_dir.mkdir(parents=True, exist_ok=True)
    l1_dir.mkdir(parents=True, exist_ok=True)

    # Read raw content
    content = filepath.read_text(encoding="utf-8")

    # Create L0 fact node
    fact_name = filepath.stem + "_fact.md"
    fact_path = l0_dir / fact_name

    with open(fact_path, "w", encoding="utf-8") as f:
        f.write(f"---\nsource: {filepath.name}\ntype: L0_fact\n---\n\n")
        f.write(content)

    # Create L1 episode node
    episode_name = filepath.stem + "_episode.md"
    episode_path = l1_dir / episode_name

    with open(episode_path, "w", encoding="utf-8") as f:
        f.write(f"---\nsource: {filepath.name}\ntype: L1_episode\n---\n\n")
        f.write(f"Ingested from {filepath} to extract L0 facts.\n")

    print(f"Successfully routed to L0 facts ({fact_path}) and L1 episodes ({episode_path}).")
    print("Ready for L2 synthesis.")

if __name__ == "__main__":
    main()
