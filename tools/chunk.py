#!/usr/bin/env python3
import sys
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

def find_boundary(text, target_size, overlap, search_window=300):
    # This function looks for a suitable semantic boundary.
    # text is the remaining text. We want a chunk of roughly target_size words.

    # Simple word counting
    words = text.split()
    if len(words) <= target_size:
        return len(text)

    # Get approximate character index for target_size words
    # A bit naive but works for text
    approx_char_idx = len(" ".join(words[:target_size]))

    # We search backwards from approx_char_idx for a boundary within search_window words
    # Let's define search_window in chars roughly
    char_search_window = search_window * 6
    start_search = max(0, approx_char_idx - char_search_window)
    search_area = text[start_search:approx_char_idx]

    # Priority 1: Section Header
    match = list(re.finditer(r'\n#{1,6}\s', search_area))
    if match:
        return start_search + match[-1].start()

    # Priority 2: Blank line paragraph
    match = list(re.finditer(r'\n\s*\n', search_area))
    if match:
        return start_search + match[-1].start()

    # Priority 3: Sentence end
    match = list(re.finditer(r'[.!?]\s+', search_area))
    if match:
        return start_search + match[-1].end()

    # Fallback to exact cut
    return approx_char_idx

def chunk_text(text, chunk_size_words=1500, overlap_words=200):
    chunks = []
    current_idx = 0
    text_len = len(text)

    while current_idx < text_len:
        remaining = text[current_idx:]
        boundary_idx = find_boundary(remaining, chunk_size_words, overlap_words)

        chunk_content = remaining[:boundary_idx].strip()
        if chunk_content:
            chunks.append(chunk_content)

        if current_idx + boundary_idx >= text_len:
            break

        # Calculate overlap backwards from boundary_idx
        overlap_chars_approx = overlap_words * 6
        overlap_start = max(0, boundary_idx - overlap_chars_approx)

        # Adjust overlap start to a sentence boundary if possible
        overlap_area = remaining[overlap_start:boundary_idx]
        match = list(re.finditer(r'[.!?]\s+', overlap_area))
        if match:
             overlap_start += match[0].end()

        current_idx += overlap_start

        # Prevent infinite loop if we don't advance
        if overlap_start == 0 and boundary_idx == 0:
            current_idx += 100

    return chunks

def process_file(filepath, chunk_size=1500, overlap=200):
    path = Path(filepath)
    if not path.exists():
        print(f"Error: {filepath} not found.")
        sys.exit(1)

    slug = path.stem
    content = path.read_text(encoding="utf-8")
    file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]

    chunks = chunk_text(content, chunk_size, overlap)

    chunks_dir = Path(f"chunks/{slug}")
    chunks_dir.mkdir(parents=True, exist_ok=True)

    total_chunks = len(chunks)

    for i, chunk_text_content in enumerate(chunks):
        chunk_num = i + 1
        chars = len(chunk_text_content)
        words = count_words(chunk_text_content)

        header = f"<!-- chunk-meta: source={path.name} chunk={chunk_num} total={total_chunks} chars={chars} words={words} -->\n\n"

        chunk_filename = chunks_dir / f"{chunk_num:04d}_chunk.md"
        chunk_filename.write_text(header + chunk_text_content, encoding="utf-8")
        print(f"Wrote {chunk_filename}")

    manifest = {
        "source": str(path),
        "slug": slug,
        "hash": file_hash,
        "total_chunks": total_chunks,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "created_date": datetime.now(timezone.utc).isoformat()
    }

    manifest_path = chunks_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {manifest_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/chunk.py <path-to-raw-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    process_file(filepath)

if __name__ == "__main__":
    main()
