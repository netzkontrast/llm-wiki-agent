#!/usr/bin/env python3
import sys
import os
import re
from pathlib import Path

def main():
    wiki_dir = Path("wiki")
    if not wiki_dir.exists():
        print("Error: wiki directory does not exist.")
        sys.exit(1)

    pages = [p for p in wiki_dir.rglob("*.md") if p.is_file() and p.name not in ["index.md", "log.md", "overview.md", "lint-report.md", "README.md"]]
    all_slugs = {p.stem for p in pages}

    orphan_pages = []
    dead_links = []
    unlinked_mentions = []
    incomplete_metadata = []
    empty_sections = []

    link_targets = set()
    page_contents = {p.name: p.read_text(encoding="utf-8") for p in pages}

    for page in pages:
        content = page_contents[page.name]

        # Dead links check
        links = re.findall(r'\[\[(.*?)\]\]', content)
        for link in links:
            target = link.split('|')[0].strip()
            link_targets.add(target)
            if target not in all_slugs and target not in ["index", "log", "overview"]:
                dead_links.append((page.name, target))

        # Empty sections check
        sections = re.findall(r'^(##+)\s+(.*?)\n\s*(?:(?=##)|\Z)', content, re.MULTILINE | re.DOTALL)
        for level, title in sections:
            # Check if section text is practically empty
            if not title.strip() or len(title.strip()) < 5:  # Simplified
                pass

        # Missing Metadata
        if not content.startswith('---'):
            incomplete_metadata.append(page.name)

    # Orphan pages check
    for page in pages:
        if page.stem not in link_targets and page.name not in ["index.md", "log.md", "overview.md"]:
            orphan_pages.append(page.name)

    # Unlinked mentions
    # Very basic heuristic: check if another page's slug appears in text without [[ ]]
    for page in pages:
        content = page_contents[page.name]
        for other_slug in all_slugs:
            if other_slug != page.stem and len(other_slug) > 4:
                # check if it exists as a word but not in a link
                # this is a very simplified check
                if re.search(r'(?<!\[\[)\b' + re.escape(other_slug) + r'\b(?!\]\])', content):
                    unlinked_mentions.append((page.name, other_slug))

    print("Linting Report")
    print("==============")
    print(f"Orphan Pages: {len(orphan_pages)}")
    for p in orphan_pages:
        print(f"  - {p}")

    print(f"\nDead Wikilinks: {len(dead_links)}")
    for page, target in dead_links:
        print(f"  - In {page}, dead link to [[{target}]]")

    print(f"\nUnlinked Mentions (Potential): {len(unlinked_mentions)}")
    for page, target in unlinked_mentions[:10]: # Limit output
        print(f"  - In {page}, potential unlinked mention of {target}")
    if len(unlinked_mentions) > 10:
        print(f"  ... and {len(unlinked_mentions) - 10} more.")

    print(f"\nIncomplete Metadata: {len(incomplete_metadata)}")
    for p in incomplete_metadata:
        print(f"  - {p}")

    print("\nChecks completed.")

if __name__ == "__main__":
    main()
