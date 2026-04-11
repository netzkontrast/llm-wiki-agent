#!/usr/bin/env python3
"""
Deterministic Linter for the LLM Wiki.

Usage:
    python tools/lint_deterministic.py

This script enforces deterministic rules (no LLM required) on the wiki pages:
1. `requires:` and `informs:` resolution
2. `valid_from` and `valid_until` consistency (must point to `is_boundary: true` timeline events)
3. Terminology ratchet (reader-state `terminology_permitted` is a superset of previous)
4. `constraint_refs:` resolution (points to existing rule page)
5. `characters:` resolution (points to existing character page)
6. Foreshadowing completeness (`planted` and `planted_chapter` < last chapter -> needs `resolved_chapter` or `intentionally unresolved`)
7. Top-level directory validation (must belong to knowledge, narrative, reader_state, meta)
"""

import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

VALID_LAYERS = {"knowledge", "narrative", "reader_state", "meta"}

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def all_wiki_pages() -> list[Path]:
    return [p for p in WIKI_DIR.rglob("*.md")
            if p.name not in ("index.md", "log.md", "overview.md", "lint-report.md", "README.md")]

def get_page_slugs() -> set[str]:
    # A reference to `rules/MaxOneNewConceptPerScene` has slug `MaxOneNewConceptPerScene`
    return {p.stem for p in all_wiki_pages()}

def extract_yaml_frontmatter(content: str) -> dict:
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    yaml_str = match.group(1)

    # A simple YAML parser for our specific format
    data = {}
    for line in yaml_str.split('\n'):
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()

        if val.startswith('[') and val.endswith(']'):
            # simple list parsing
            inner = val[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                data[key] = [item.strip().strip('"\'') for item in inner.split(',')]
        elif val.startswith('{') and val.endswith('}'):
             data[key] = {}
        elif val.lower() == 'true':
            data[key] = True
        elif val.lower() == 'false':
            data[key] = False
        elif val.lower() == 'null' or val == '':
            data[key] = None
        else:
            try:
                data[key] = int(val)
            except ValueError:
                data[key] = val.strip('"\'')
    return data

def check_layer(page: Path):
    parts = page.relative_to(WIKI_DIR).parts
    if len(parts) > 0 and parts[0] not in VALID_LAYERS:
         return f"Error: Page not in valid layer: {parts[0]}"
    return None

def check_refs(frontmatter: dict, page: Path, all_slugs: set[str], field_name: str):
    errors = []
    refs = frontmatter.get(field_name, [])
    if isinstance(refs, list):
         for ref in refs:
             # some refs might be prefixed with their directory like 'rules/MaxOneNewConceptPerScene'
             clean_ref = ref.split('/')[-1]
             if clean_ref not in all_slugs:
                 errors.append(f"Error: {field_name} ref '{ref}' (slug: {clean_ref}) not found in wiki")
    return errors

def main():
    pages = all_wiki_pages()
    all_slugs = get_page_slugs()

    print(f"Running deterministic linting on {len(pages)} pages...")

    # Collect boundary events for valid_from/valid_until checks
    boundary_events = set()
    rule_pages = set()
    character_pages = set()
    reader_states = {} # chapter_ref -> terminology_permitted
    max_chapter = 0

    for p in pages:
        fm = extract_yaml_frontmatter(read_file(p))
        if fm.get("type") == "timeline-event" and fm.get("is_boundary") is True:
             boundary_events.add(p.stem)
        if fm.get("type") == "rule":
             rule_pages.add(p.stem)
        if fm.get("type") == "character":
             character_pages.add(p.stem)
        if fm.get("type") == "reader-state":
             ch_ref = fm.get("chapter_ref")
             terms = fm.get("terminology_permitted", [])
             if ch_ref is not None:
                 reader_states[ch_ref] = set(terms)
                 max_chapter = max(max_chapter, ch_ref)
        elif fm.get("type") == "chapter":
            ch_ref = fm.get("chapter_ref", 0) # Assumes chapters might have ref

    # Also find max chapter looking at names
    for p in pages:
         if p.stem.startswith("chapter-"):
             try:
                 num = int(p.stem.split("-")[1].replace("-state", ""))
                 max_chapter = max(max_chapter, num)
             except ValueError:
                 pass

    errors = []

    for p in pages:
        fm = extract_yaml_frontmatter(read_file(p))
        layer_err = check_layer(p)
        if layer_err: errors.append(f"{p}: {layer_err}")

        # Check requires and informs
        errs = check_refs(fm, p, all_slugs, "requires")
        for e in errs: errors.append(f"{p}: {e}")

        errs = check_refs(fm, p, all_slugs, "informs")
        for e in errs: errors.append(f"{p}: {e}")

        # Check valid_from / valid_until
        v_from = fm.get("valid_from")
        if v_from and v_from not in boundary_events:
            errors.append(f"{p}: valid_from '{v_from}' must point to an is_boundary: true event")

        v_until = fm.get("valid_until")
        if v_until and v_until not in boundary_events:
            errors.append(f"{p}: valid_until '{v_until}' must point to an is_boundary: true event")

        # Check constraint_refs
        if "constraint_refs" in fm:
            errs = check_refs(fm, p, rule_pages, "constraint_refs")
            for e in errs: errors.append(f"{p}: constraint_refs error - {e}")

        # Check characters
        if "characters" in fm:
             errs = check_refs(fm, p, character_pages, "characters")
             for e in errs: errors.append(f"{p}: characters error - {e}")

        # Check foreshadowing
        if fm.get("type") == "foreshadowing":
            status = fm.get("status")
            planted = fm.get("planted_chapter")
            resolved = fm.get("resolved_chapter")
            if status == "planted" and planted is not None and max_chapter is not None and planted < max_chapter:
                 if resolved is None and fm.get("intentionally_unresolved") is not True:
                      content = read_file(p)
                      if "intentionally unresolved" not in content.lower():
                           errors.append(f"{p}: Foreshadowing is planted at chap {planted} but unresolved (max chap {max_chapter})")

    # Check terminology ratchet
    sorted_chapters = sorted(reader_states.keys())
    for i in range(1, len(sorted_chapters)):
        prev_ch = sorted_chapters[i-1]
        curr_ch = sorted_chapters[i]
        prev_terms = reader_states[prev_ch]
        curr_terms = reader_states[curr_ch]

        if not prev_terms.issubset(curr_terms):
            missing = prev_terms - curr_terms
            errors.append(f"Reader State Terminology Error: Chapter {curr_ch} does not include terms {missing} from chapter {prev_ch}")

    if errors:
        print("Linting failed with the following errors:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("All deterministic lint checks passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
