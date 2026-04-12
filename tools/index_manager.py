#!/usr/bin/env python3
import sys
import argparse
import re
from pathlib import Path
import json

INDEX_PATH = Path("wiki/index.md")

class IndexManager:
    def __init__(self, path=INDEX_PATH):
        self.path = path
        self.lines = []
        self.entries = []
        if self.path.exists():
            self.lines = self.path.read_text(encoding="utf-8").splitlines()
            self._parse()

    def _parse(self):
        self.entries = []
        for i, line in enumerate(self.lines):
            match = re.match(r'^-\s+\[(.*?)\]\((.*?)\)(.*?)$', line)
            if match:
                title, file_path, rest = match.groups()
                desc = ""
                type_val = None
                slug_val = None

                tag_match = re.search(r'<!--\s*type:(\S+)\s+slug:(\S+)\s*-->', rest)
                if tag_match:
                    type_val = tag_match.group(1)
                    slug_val = tag_match.group(2)
                    rest = rest[:tag_match.start()]

                desc_match = re.match(r'^\s*(?:[-—]\s*)?(.*?)\s*$', rest)
                if desc_match:
                    desc = desc_match.group(1).strip()

                # If no slug is specified but it's a file path, we can infer a fallback slug for check-duplicate?
                # For now, rely on tag. But legacy lines won't have it.

                self.entries.append({
                    "line_idx": i,
                    "title": title,
                    "path": file_path,
                    "desc": desc,
                    "type": type_val,
                    "slug": slug_val,
                    "raw": line
                })

    def save(self):
        self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")

    def list_entries(self, type_filter=None):
        if type_filter and type_filter != "all":
            return [e for e in self.entries if e.get("type") == type_filter]
        return self.entries

    def get(self, slug):
        for e in self.entries:
            if e.get("slug") == slug:
                return e
        return None

    def format_line(self, title, path, desc, type_val, slug):
        line = f"- [{title}]({path})"
        if desc:
            line += f" — {desc}"
        if type_val and slug:
            line += f" <!-- type:{type_val} slug:{slug} -->"
        return line

    def add(self, title, path, desc, type_val, slug, section):
        new_line = self.format_line(title, path, desc, type_val, slug)

        # Find section
        section_idx = -1
        for i, line in enumerate(self.lines):
            if re.match(r'^#{2,3}\s+' + re.escape(section), line, re.IGNORECASE):
                section_idx = i
                break

        if section_idx == -1:
            # Section not found, append it at the end
            self.lines.append("")
            self.lines.append(f"### {section}")
            self.lines.append(new_line)
        else:
            # Insert after the last item in the section
            insert_idx = section_idx + 1
            while insert_idx < len(self.lines) and (self.lines[insert_idx].startswith("- ") or self.lines[insert_idx].strip() == ""):
                if self.lines[insert_idx].startswith("- "):
                    pass # Keep going
                insert_idx += 1
            # Backtrack empty lines
            while insert_idx > 0 and self.lines[insert_idx - 1].strip() == "":
                insert_idx -= 1

            self.lines.insert(insert_idx, new_line)

        self._parse() # Re-parse
        self.save()

    def update(self, slug, title=None, path=None, desc=None, type_val=None):
        entry = self.get(slug)
        if not entry:
            return False

        t = title if title is not None else entry["title"]
        p = path if path is not None else entry["path"]
        d = desc if desc is not None else entry["desc"]
        ty = type_val if type_val is not None else entry["type"]

        new_line = self.format_line(t, p, d, ty, slug)
        self.lines[entry["line_idx"]] = new_line
        self._parse()
        self.save()
        return True

    def remove(self, slug):
        entry = self.get(slug)
        if not entry:
            return False

        del self.lines[entry["line_idx"]]
        self._parse()
        self.save()
        return True

    def check_duplicate(self, slug, type_val):
        # We should also check legacy lines by path stem
        e = self.get(slug)
        if e:
            if e.get("type") and e.get("type") != type_val:
                return "CONFLICT"
            return "EXISTS"

        # Check fallback (legacy lines might have the same stem in their path)
        for entry in self.entries:
            if not entry.get("slug"): # Legacy line
                p = Path(entry["path"])
                if p.stem == slug:
                    # Try to infer type from parent directory or assume it's just EXISTS if matching
                    return "EXISTS" # Could be CONFLICT if type mismatch but without type in legacy line it's hard to be sure.
        return "OK"

    def rebuild(self):
        print("Rebuilding index from wiki directory...")
        wiki_dir = Path("wiki")
        pages = []
        for p in wiki_dir.rglob("*.md"):
            if p.name in ("index.md", "log.md", "overview.md", "lint-report.md", "README.md"):
                continue
            content = p.read_text(encoding="utf-8")

            # Extract frontmatter
            title = p.stem
            ptype = None
            desc = ""

            match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                yaml_str = match.group(1)
                for line in yaml_str.split('\n'):
                    if line.startswith('title:'):
                        title = line.split(':', 1)[1].strip().strip('"\'')
                    elif line.startswith('type:'):
                        ptype = line.split(':', 1)[1].strip()

            if not ptype:
                continue

            path_str = str(p.relative_to(wiki_dir))

            # Preserve existing desc if we have it in memory
            existing_entry = self.get(p.stem)
            if existing_entry and existing_entry.get("desc"):
                desc = existing_entry["desc"]

            pages.append({
                "title": title,
                "path": path_str,
                "slug": p.stem,
                "type": ptype,
                "desc": desc
            })

        # Group by section type
        sections = {
            "Sources": [p for p in pages if p["type"] == "source"],
            "Entities": [p for p in pages if p["type"] == "entity"],
            "Concepts": [p for p in pages if p["type"] == "concept"],
            "Syntheses": [p for p in pages if p["type"] == "synthesis"],
            "Characters": [p for p in pages if p["type"] == "character"],
            "Chapters": [p for p in pages if p["type"] == "chapter"],
            "Locations": [p for p in pages if p["type"] == "location"],
            "Conflicts": [p for p in pages if p["type"] == "conflict"],
            "Themes": [p for p in pages if p["type"] == "theme"],
            "Timeline": [p for p in pages if p["type"] == "timeline-event"],
            "Rules": [p for p in pages if p["type"] == "rule"],
            "Arcs": [p for p in pages if p["type"] == "arc"],
            "Dramatica": [p for p in pages if p["type"] == "dramatica"],
            "Reader Model": [p for p in pages if p["type"] == "reader-state"],
            "Foreshadowing": [p for p in pages if p["type"] == "foreshadowing"],
            "Outlines": [p for p in pages if p["type"] == "outline"],
            "Beats": [p for p in pages if p["type"] == "beat"],
            "Manuscripts": [p for p in pages if p["type"] == "manuscript"],
        }

        new_lines = [
            "# Wiki Index",
            "",
            "This file is maintained by the LLM. Updated on every ingest.",
            "",
            "## Overview",
            "- [Overview](overview.md) — living synthesis across all sources",
            "",
            "## Knowledge Layer"
        ]

        knowledge_sections = ["Sources", "Entities", "Concepts", "Syntheses", "Rules", "Timeline"]
        narrative_sections = ["Characters", "Chapters", "Locations", "Conflicts", "Themes", "Arcs", "Dramatica", "Beats", "Outlines", "Manuscripts"]
        reader_sections = ["Reader Model", "Foreshadowing"]

        for name in knowledge_sections:
            new_lines.append(f"\n### {name}")
            for p in sorted(sections[name], key=lambda x: x["title"]):
                new_lines.append(self.format_line(p["title"], p["path"], p["desc"], p["type"], p["slug"]))

        new_lines.append("\n## Narrative Layer")
        for name in narrative_sections:
            new_lines.append(f"\n### {name}")
            for p in sorted(sections[name], key=lambda x: x["title"]):
                new_lines.append(self.format_line(p["title"], p["path"], p["desc"], p["type"], p["slug"]))

        new_lines.append("\n## Reader State Layer")
        for name in reader_sections:
            new_lines.append(f"\n### {name}")
            for p in sorted(sections[name], key=lambda x: x["title"]):
                new_lines.append(self.format_line(p["title"], p["path"], p["desc"], p["type"], p["slug"]))

        self.lines = new_lines
        self.save()
        self._parse()
        print("Rebuild complete.")

def main():
    parser = argparse.ArgumentParser(description="Wiki Index Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list
    p_list = subparsers.add_parser("list", help="List index entries")
    p_list.add_argument("--type", help="Filter by type", default="all")

    # get
    p_get = subparsers.add_parser("get", help="Get entry by slug")
    p_get.add_argument("slug", help="Slug of the entry")

    # add
    p_add = subparsers.add_parser("add", help="Add a new entry")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--path", required=True)
    p_add.add_argument("--desc", default="")
    p_add.add_argument("--type", required=True)
    p_add.add_argument("--slug", required=True)
    p_add.add_argument("--section", required=True)

    # update
    p_update = subparsers.add_parser("update", help="Update an entry")
    p_update.add_argument("slug", help="Slug of the entry to update")
    p_update.add_argument("--title")
    p_update.add_argument("--path")
    p_update.add_argument("--desc")
    p_update.add_argument("--type")

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove an entry")
    p_remove.add_argument("slug", help="Slug of the entry to remove")

    # check-duplicate
    p_check = subparsers.add_parser("check-duplicate", help="Check if a slug exists and type matches")
    p_check.add_argument("slug", help="Slug to check")
    p_check.add_argument("type", help="Type to check against")

    # rebuild
    p_rebuild = subparsers.add_parser("rebuild", help="Rebuild the index")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = IndexManager()

    if args.command == "list":
        t = getattr(args, 'type', 'all')
        entries = manager.list_entries(t)
        for e in entries:
            print(json.dumps(e))

    elif args.command == "get":
        e = manager.get(args.slug)
        if e:
            print(json.dumps(e))
        else:
            print("Not found", file=sys.stderr)
            sys.exit(1)

    elif args.command == "add":
        manager.add(args.title, args.path, args.desc, args.type, args.slug, args.section)
        print("Added.")

    elif args.command == "update":
        success = manager.update(args.slug, args.title, args.path, args.desc, args.type)
        if success:
            print("Updated.")
        else:
            print("Not found", file=sys.stderr)
            sys.exit(1)

    elif args.command == "remove":
        success = manager.remove(args.slug)
        if success:
            print("Removed.")
        else:
            print("Not found", file=sys.stderr)
            sys.exit(1)

    elif args.command == "check-duplicate":
        res = manager.check_duplicate(args.slug, args.type)
        print(res)

    elif args.command == "rebuild":
        manager.rebuild()

if __name__ == "__main__":
    main()
