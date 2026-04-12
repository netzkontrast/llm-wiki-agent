#!/usr/bin/env python3
import sys
import argparse
import re
import random
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
DOCS_DIR = REPO_ROOT / "docs"
SCHEMA_FILE = DOCS_DIR / "wiki-schema.md"
INDEX_FILE = WIKI_DIR / "index.md"

def extract_yaml_frontmatter(content: str) -> dict:
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    yaml_str = match.group(1)
    data = {}
    for line in yaml_str.split('\n'):
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        data[key] = val
    return data

def get_candidate_names(chunk_content: str) -> set:
    words = re.findall(r'\b[A-Z][a-zA-Z]+\b', chunk_content)
    ignore_list = {"The", "A", "An", "In", "On", "And", "Or", "But", "I", "He", "She", "It"}
    candidates = {w for w in set(words) if w not in ignore_list}
    return candidates

def get_relevant_pages(task_layer: str, candidate_names: set, max_chars: int = 15000) -> list:
    relevant_pages = []
    layer_dir = WIKI_DIR / task_layer

    if not layer_dir.exists():
        return relevant_pages

    for p in layer_dir.rglob("*.md"):
        content = p.read_text(encoding="utf-8")
        stem = p.stem.lower()
        first_500 = content[:500].lower()

        is_relevant = False
        for name in candidate_names:
            name_lower = name.lower()
            if name_lower in stem or name_lower in first_500:
                is_relevant = True
                break

        if is_relevant:
            capped_content = content[:3000]
            if len(content) > 3000:
                capped_content += "\n\n...[content truncated]"

            relevant_pages.append({
                "path": str(p.relative_to(WIKI_DIR)),
                "content": capped_content
            })

    total_chars = 0
    final_pages = []
    for rp in relevant_pages:
        if total_chars + len(rp["content"]) <= max_chars:
            final_pages.append(rp)
            total_chars += len(rp["content"])
        else:
            break

    return final_pages

def get_query_pages(query: str, max_chars: int = 15000) -> list:
    relevant_pages = []
    index_content = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else ""
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', index_content)

    question_lower = query.lower()

    for title, href in md_links:
        if any(word in question_lower for word in title.lower().split() if len(word) > 3):
            p = WIKI_DIR / href
            if p.exists():
                content = p.read_text(encoding="utf-8")
                capped_content = content[:3000]
                if len(content) > 3000:
                    capped_content += "\n\n...[content truncated]"

                relevant_pages.append({
                    "path": href,
                    "content": capped_content
                })

    overview = WIKI_DIR / "overview.md"
    if overview.exists() and not any(rp["path"] == "overview.md" for rp in relevant_pages):
        content = overview.read_text(encoding="utf-8")
        relevant_pages.insert(0, {
            "path": "overview.md",
            "content": content[:3000] + ("\n\n...[content truncated]" if len(content) > 3000 else "")
        })

    total_chars = 0
    final_pages = []
    for rp in relevant_pages[:12]: # Cap at 12 pages
        if total_chars + len(rp["content"]) <= max_chars:
            final_pages.append(rp)
            total_chars += len(rp["content"])
        else:
            break

    return final_pages

def get_lint_pages(max_chars: int = 15000) -> list:
    pages = [p for p in WIKI_DIR.rglob("*.md")
            if p.name not in ("index.md", "log.md", "overview.md", "lint-report.md", "README.md")]

    # Take a random sample or recent pages to stay within context
    sample = random.sample(pages, min(20, len(pages)))

    relevant_pages = []
    total_chars = 0
    for p in sample:
        content = p.read_text(encoding="utf-8")
        capped_content = content[:1500]
        if len(content) > 1500:
            capped_content += "\n\n...[content truncated]"

        if total_chars + len(capped_content) <= max_chars:
            relevant_pages.append({
                "path": str(p.relative_to(WIKI_DIR)),
                "content": capped_content
            })
            total_chars += len(capped_content)
        else:
            break

    return relevant_pages

def build_context(task_type: str, chunk_path: Path = None, batch_threshold: int = 15, query_str: str = None):
    context = []

    # Task reminder
    context.append(f"# Task Context: {task_type.upper()}")

    if task_type == "ingest-knowledge":
        task_layer = "knowledge"
        context.append("You are processing a chunk for the KNOWLEDGE layer.")
    elif task_type == "ingest-narrative":
        task_layer = "narrative"
        context.append("You are processing a chunk for the NARRATIVE layer.")
    elif task_type == "ingest-reader":
        task_layer = "reader_state"
        context.append("You are processing a chunk for the READER_STATE layer.")
    elif task_type == "plan":
        task_layer = "all"
        context.append("You are creating an initial extraction plan for this chunk.")
    elif task_type == "query":
        task_layer = "none"
        context.append(f"You are answering a query: '{query_str}'")
    elif task_type == "lint":
        task_layer = "none"
        context.append("You are performing semantic lint checks on the wiki.")
    else:
        task_layer = "all"

    # Query specific context
    if task_type == "query" and query_str:
        pages = get_query_pages(query_str)
        if pages:
            context.append("\n## Relevant Wiki Context")
            for p in pages:
                context.append(f"\n### {p['path']}")
                context.append(p['content'])
        index_content = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else ""
        context.append("\n## Wiki Index")
        context.append("```markdown\n" + index_content + "\n```")

    # Lint specific context
    if task_type == "lint":
        pages = get_lint_pages()
        if pages:
            context.append(f"\n## Wiki Context Sample ({len(pages)} pages)")
            for p in pages:
                context.append(f"\n### {p['path']}")
                context.append(p['content'])

        # Include structural lint report
        try:
            res = subprocess.run([sys.executable, str(REPO_ROOT / "tools" / "lint_deterministic.py")], capture_output=True, text=True)
            context.append("\n## Deterministic Lint Report")
            context.append("```\n" + (res.stdout + "\n" + res.stderr).strip() + "\n```")
        except Exception as e:
            context.append(f"\n## Deterministic Lint Report\nCould not run: {e}")

    # Chunk Content
    if chunk_path and chunk_path.exists():
        chunk_content = chunk_path.read_text(encoding="utf-8")
        context.append("\n## Source Chunk")
        context.append("```markdown")
        context.append(chunk_content)
        context.append("```")

        # Batch Injection
        if task_type == "plan":
            candidates = get_candidate_names(chunk_content)
            if len(candidates) > batch_threshold:
                context.append("\n## Batch Processing Instructions")
                context.append(f"High entity count detected ({len(candidates)} candidates). Split the task into Pass 1 (knowledge-layer types) and Pass 2 (narrative-layer types).")

        # Relevant Context
        if task_layer not in ("all", "none"):
            candidates = get_candidate_names(chunk_content)
            pages = get_relevant_pages(task_layer, candidates)
            if pages:
                context.append(f"\n## Relevant Wiki Context ({task_layer} layer)")
                for p in pages:
                    context.append(f"\n### {p['path']}")
                    context.append(p['content'])

    # Schema Reminder (Skip for query, lint usually doesn't need full schema reminder but keep it consistent, query can use it)
    if SCHEMA_FILE.exists() and task_type != "lint":
        schema_content = SCHEMA_FILE.read_text(encoding="utf-8")
        context.append("\n## Schema Reminder")
        context.append("```markdown")
        context.append(schema_content)
        context.append("```")

    # Validation Expectations (Skip for query and lint)
    if task_type not in ["query", "lint"]:
        context.append("\n## Validation Expectations")
        context.append("- All pages must contain valid YAML frontmatter (with all universal fields present).")
        context.append("- Page 'type' must be one of the 18 valid types.")
        context.append("- Type-specific required fields must be present.")
        context.append("- Slugs and references must resolve correctly.")
        context.append("- New pages must be appended to wiki/index.md using the required tagged format: `- [Title](path) — description <!-- type:TYPE slug:SLUG -->`")

    return "\n".join(context)

def main():
    parser = argparse.ArgumentParser(description="Compile Context for Agent Task")
    parser.add_argument("--task", required=True, choices=["plan", "ingest-knowledge", "ingest-narrative", "ingest-reader", "query", "lint"])
    parser.add_argument("--chunk", help="Path to chunk file")
    parser.add_argument("--batch-threshold", type=int, default=15, help="Threshold for batch processing instructions")
    parser.add_argument("--query", type=str, help="Query string for query task")

    args = parser.parse_args()

    chunk_path = Path(args.chunk) if args.chunk else None

    context_str = build_context(args.task, chunk_path, args.batch_threshold, args.query)
    print(context_str)

if __name__ == "__main__":
    main()
