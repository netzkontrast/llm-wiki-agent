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
    missing_required_pages = []

    link_targets = set()
    page_contents = {p.name: p.read_text(encoding="utf-8") for p in pages}


    reader_states = {}
    max_chapter = 0
    boundary_events = set()

    # First pass: collect metadata for deep checks
    for page in pages:
        c = page_contents[page.name]
        match = re.search(r'^type:\s*(.*?)$', c, re.MULTILINE)
        ptype = match.group(1).strip().strip('"\'') if match else ""

        if ptype == "timeline-event":
            if re.search(r'^is_boundary:\s*true', c, re.MULTILINE | re.IGNORECASE):
                boundary_events.add(page.stem)

        if ptype == "reader-state":
            cmatch = re.search(r'^chapter_ref:\s*(\d+)', c, re.MULTILINE)
            if cmatch:
                ch_ref = int(cmatch.group(1))
                max_chapter = max(max_chapter, ch_ref)

                tmatch = re.search(r'^terminology_permitted:\s*\[(.*?)\]', c, re.MULTILINE)
                if tmatch:
                    terms_str = tmatch.group(1)
                    terms = {t.strip().strip('"\'') for t in terms_str.split(',') if t.strip()}
                    reader_states[ch_ref] = terms
    for page in pages:
        content = page_contents[page.name]

        # Missing Metadata
        if not content.startswith('---'):
            incomplete_metadata.append(page.name)
        else:
            # Check requires
            match = re.search(r'^requires:\s*\[(.*?)\]', content, re.MULTILINE)
            if match:
                reqs_str = match.group(1)
                reqs = [r.strip().strip('"\'') for r in reqs_str.split(',') if r.strip()]
                for req in reqs:
                    if req and req not in all_slugs:
                        missing_required_pages.append((page.name, req))

            # Check informs
            match = re.search(r'^informs:\s*\[(.*?)\]', content, re.MULTILINE)
            if match:
                reqs_str = match.group(1)
                reqs = [r.strip().strip('"\'') for r in reqs_str.split(',') if r.strip()]
                for req in reqs:
                    if req and req not in all_slugs:
                        missing_required_pages.append((page.name, req))


        match = re.search(r'^type:\s*(.*?)$', content, re.MULTILINE)
        ptype = match.group(1).strip().strip('"\'') if match else ""

        # chapter_ref requirement for Narrative Layer
        if ptype in ("chapter", "outline", "beat", "manuscript"):
            if not re.search(r'^chapter_ref:', content, re.MULTILINE):
                incomplete_metadata.append(page.name + " (Missing chapter_ref)")

        # Knowledge layer must not have manuscript_status or beat_number
        if "knowledge" in page.parts:
            if re.search(r'^(manuscript_status|beat_number):', content, re.MULTILINE):
                incomplete_metadata.append(page.name + " (Knowledge layer shouldn't have narrative metadata)")

        # valid_from / valid_until must point to boundary events
        vmatch = re.search(r'^valid_from:\s*(.*?)$', content, re.MULTILINE)
        if vmatch:
            v_from = vmatch.group(1).strip().strip('"\'')
            if v_from and v_from not in boundary_events:
                dead_links.append((page.name, v_from + " (Invalid boundary event)"))

        vmatch = re.search(r'^valid_until:\s*(.*?)$', content, re.MULTILINE)
        if vmatch:
            v_until = vmatch.group(1).strip().strip('"\'')
            if v_until and v_until not in boundary_events:
                dead_links.append((page.name, v_until + " (Invalid boundary event)"))

        # Dead links check
        links = re.findall(r'\[\[(.*?)\]\]', content)
        for link in links:
            target = link.split('|')[0].strip()
            link_targets.add(target)
            if target not in all_slugs and target not in ["index", "log", "overview"]:
                dead_links.append((page.name, target))

        # Empty sections check
        sections_raw = re.split(r'^(##+)\s+(.*?)$', content, flags=re.MULTILINE)
        i = 1
        while i < len(sections_raw):
            heading_level = sections_raw[i]
            heading_title = sections_raw[i+1].strip()
            body_content = sections_raw[i+2] if (i+2) < len(sections_raw) else ""
            body_content = body_content.strip()
            if len(body_content) < 5:
                empty_sections.append((page.name, heading_title))
            i += 3

    # Orphan pages check
    for page in pages:
        if page.stem not in link_targets and page.name not in ["index.md", "log.md", "overview.md"]:
            orphan_pages.append(page.name)

    # Unlinked mentions
    for page in pages:
        content = page_contents[page.name]
        for other_slug in all_slugs:
            if other_slug != page.stem and len(other_slug) > 4:
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

    print(f"\nMissing Required Pages: {len(missing_required_pages)}")
    for page, target in missing_required_pages:
        print(f"  - In {page}, missing required/informs page {target}")

    print(f"\nEmpty Sections: {len(empty_sections)}")
    for page, section in empty_sections:
        print(f"  - In {page}, section '{section}' is empty.")

    print(f"\nUnlinked Mentions (Potential): {len(unlinked_mentions)}")
    for page, target in unlinked_mentions[:10]:
        print(f"  - In {page}, potential unlinked mention of {target}")
    if len(unlinked_mentions) > 10:
        print(f"  ... and {len(unlinked_mentions) - 10} more.")

    print(f"\nIncomplete Metadata: {len(incomplete_metadata)}")
    for p in incomplete_metadata:
        print(f"  - {p}")


    print(f"\nTerminology Ratchet Checks:")
    sorted_chapters = sorted(reader_states.keys())
    for i in range(1, len(sorted_chapters)):
        prev_ch = sorted_chapters[i-1]
        curr_ch = sorted_chapters[i]
        if not reader_states[prev_ch].issubset(reader_states[curr_ch]):
            missing = reader_states[prev_ch] - reader_states[curr_ch]
            print(f"  - Error: Chapter {curr_ch} does not include terms {missing} from chapter {prev_ch}")

    print("\nChecks completed.")

if __name__ == "__main__":
    main()
