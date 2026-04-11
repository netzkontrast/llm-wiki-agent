#!/usr/bin/env python3
"""
Ingest a source document into the LLM Wiki.

Usage:
    python tools/ingest.py <path-to-source>
    python tools/ingest.py raw/articles/my-article.md

The LLM reads the source, extracts knowledge, and updates the wiki:
  - Creates wiki/sources/<slug>.md
  - Updates wiki/index.md
  - Updates wiki/overview.md (if warranted)
  - Creates/updates entity and concept pages
  - Appends to wiki/log.md
  - Flags contradictions
"""

import os
import sys
import json
import shutil
import hashlib
import re
import subprocess
from pathlib import Path
from datetime import date

import anthropic

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
LOG_FILE = WIKI_DIR / "log.md"
INDEX_FILE = WIKI_DIR / "index.md"
OVERVIEW_FILE = WIKI_DIR / "overview.md"
SCHEMA_FILE = REPO_ROOT / "CLAUDE.md"
PROCESSED_DIR = REPO_ROOT / "processed"
RAW_DIR = (REPO_ROOT / "raw").resolve()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote: {path.relative_to(REPO_ROOT)}")


def build_wiki_context() -> str:
    parts = []
    if INDEX_FILE.exists():
        parts.append(f"## wiki/index.md\n{read_file(INDEX_FILE)}")
    if OVERVIEW_FILE.exists():
        parts.append(f"## wiki/overview.md\n{read_file(OVERVIEW_FILE)}")
    # Include a few recent source pages for contradiction checking
    sources_dir = WIKI_DIR / "sources"
    if sources_dir.exists():
        recent = sorted(sources_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
        for p in recent:
            parts.append(f"## {p.relative_to(REPO_ROOT)}\n{p.read_text()}")

    # Include qmd context if available. For the script logic, we leave this stubbed or manual search.
    # In a full run, the caller should have populated context, or we can run qmd search here for file contents

    return "\n\n---\n\n".join(parts)


def parse_json_from_response(text: str) -> dict:
    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text.strip())
    # Find the outermost JSON object
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in response")
    return json.loads(match.group())


def update_index_multi(index_entries: dict):
    content = read_file(INDEX_FILE)
    if not content:
        content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md) — living synthesis\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"

    for section, entries in index_entries.items():
        section_header = f"## {section}"
        entries_str = "\n".join(entries)
        if section_header in content:
            content = content.replace(section_header + "\n", section_header + "\n" + entries_str + "\n")
        else:
            content += f"\n{section_header}\n{entries_str}\n"

    write_file(INDEX_FILE, content)


def append_log(entry: str):
    existing = read_file(LOG_FILE)
    write_file(LOG_FILE, entry.strip() + "\n\n" + existing)


def ingest(source_path: str):
    source = Path(source_path)
    if not source.exists():
        print(f"Error: file not found: {source_path}")
        sys.exit(1)

    source_content = source.read_text(encoding="utf-8")
    source_hash = sha256(source_content)
    today = date.today().isoformat()

    print(f"\nIngesting: {source.name}  (hash: {source_hash})")

    wiki_context = build_wiki_context()
    schema = read_file(SCHEMA_FILE)
    wiki_schema = read_file(REPO_ROOT / "docs" / "wiki-schema.md")
    schema += "\n\n" + wiki_schema

    client = anthropic.Anthropic()

    prompt = f"""You are maintaining an LLM Wiki. Process this source document and integrate its knowledge into the wiki.

Schema and conventions:
{schema}

Current wiki state (index + recent pages):
{wiki_context if wiki_context else "(wiki is empty — this is the first source)"}

New source to ingest (file: {source.relative_to(REPO_ROOT) if source.is_relative_to(REPO_ROOT) else source.name}):
=== SOURCE START ===
{source_content}
=== SOURCE END ===

Today's date: {today}

Return ONLY a valid JSON object with these fields (no markdown fences, no prose outside the JSON):
{{
  "title": "Human-readable title for this source",
  "slug": "kebab-case-slug-for-filename",
  "source_page": "full markdown content for wiki/sources/<slug>.md — use the source page format from the schema",
  "index_entries": {{
    "Sources": ["- [Title](sources/slug.md) — one-line summary"]
  }},
  "overview_update": "full updated content for wiki/overview.md, or null if no update needed",
  "entity_pages": [
    {{"action": "create", "path": "entities/EntityName.md", "content": "full markdown content"}}
  ],
  "concept_pages": [
    {{"action": "create", "path": "concepts/ConceptName.md", "content": "full markdown content"}}
  ],
  "character_pages": [],
  "location_pages": [],
  "conflict_pages": [],
  "theme_pages": [],
  "rule_pages": [],
  "timeline_events": [],
  "foreshadowing_pages": [],
  "contradictions": ["describe any contradiction with existing wiki content, or empty list"],
  "log_entry": "## [{today}] ingest | <title>\\n\\nAdded source. Key claims: ..."
}}
"""

    print("  calling Claude API...")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    try:
        data = parse_json_from_response(raw)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing API response: {e}")
        print("Raw response saved to /tmp/ingest_debug.txt")
        Path("/tmp/ingest_debug.txt").write_text(raw)
        sys.exit(1)

    # Write all wiki pages — only move source to processed/ if ALL writes succeed
    try:
        slug = data["slug"]
        write_file(WIKI_DIR / "sources" / f"{slug}.md", data["source_page"])

        # Validate layer mapping for standard types
        layer_mapping = {
            "entities": "knowledge",
            "concepts": "knowledge",
            "sources": "knowledge",
            "rules": "knowledge",
            "characters": "narrative",
            "chapters": "narrative",
            "locations": "narrative",
            "conflicts": "narrative",
            "themes": "narrative",
            "arcs": "narrative",
            "reader-model": "reader_state",
            "foreshadowing": "reader_state",
            "timeline": "narrative" # or knowledge based on the file but standard timeline events typically narrative here
        }

        for key in ("entity_pages", "concept_pages", "character_pages", "location_pages", "conflict_pages", "theme_pages", "rule_pages", "timeline_events", "foreshadowing_pages"):
            for page in data.get(key, []):
                path_str = page.get("path", "")
                parts = path_str.split("/")
                if len(parts) >= 2:
                    page_type_dir = parts[-2]
                    expected_layer = layer_mapping.get(page_type_dir)
                    if expected_layer and parts[0] != expected_layer:
                        print(f"  ⚠️  Warning: Page {path_str} is assigned to layer '{parts[0]}' but expected '{expected_layer}'")

                write_file(WIKI_DIR / path_str, page["content"])

        if data.get("overview_update"):
            write_file(OVERVIEW_FILE, data["overview_update"])

        if "index_entries" in data:
            update_index_multi(data["index_entries"])
        elif "index_entry" in data:
            # Fallback
            update_index_multi({"Sources": [data["index_entry"]]})

        append_log(data["log_entry"])

        # Run qmd embed after all writes succeed
        if shutil.which("qmd"):
            try:
                subprocess.run(["qmd", "embed"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                pass

    except Exception as e:
        print(f"\nError during wiki write operations: {e}")
        print("Source file was NOT moved to processed/ — manual cleanup may be needed.")
        sys.exit(1)

    contradictions = data.get("contradictions", [])
    if contradictions:
        print("\n  ⚠️  Contradictions detected:")
        for c in contradictions:
            print(f"     - {c}")

    source_abs = source.resolve()
    if source_abs.is_relative_to(RAW_DIR) and source_abs.exists():
        dest = PROCESSED_DIR / source_abs.relative_to(RAW_DIR)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            dest = dest.with_stem(f"{dest.stem}_{source_hash}")
        shutil.move(source_abs, dest)
        print(f"  moved: {source_abs.relative_to(REPO_ROOT)} → {dest.relative_to(REPO_ROOT)}")
    elif source_abs.is_relative_to(PROCESSED_DIR) and source_abs.exists():
        print(f"  Note: Source is already in processed directory: {source_abs.relative_to(REPO_ROOT)}")

    print(f"\nDone. Ingested: {data['title']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/ingest.py <path-to-source>")
        sys.exit(1)
    ingest(sys.argv[1])
