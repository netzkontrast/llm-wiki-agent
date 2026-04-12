import sys
import re
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

REPO_ROOT = Path(".").resolve()
WIKI_DIR = REPO_ROOT / "wiki"
INDEX_PATH = WIKI_DIR / "index.md"

def all_wiki_pages() -> list[Path]:
    return [p for p in WIKI_DIR.rglob("*.md")
            if p.name not in ("index.md", "log.md", "overview.md", "lint-report.md", "README.md")]

all_pages = all_wiki_pages()
pages = all_wiki_pages()
recent_minutes = 5
cutoff = datetime.now(timezone.utc) - timedelta(minutes=recent_minutes)
pages = [p for p in pages if datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc) >= cutoff]

print("All wiki pages:")
print(any(p.stem == "test-kael-konflikt" for p in all_pages))
print("Recent wiki pages:")
print(any(p.stem == "test-kael-konflikt" for p in pages))
