---
name: wiki-lint
description: validates schema and identifies semantic inconsistencies
---

## Steps

1. Run `python3 tools/validate.py --format json`
   - If there are errors, stop and report them. Do not proceed to semantic checks.

2. Run `python3 tools/compile_context.py --task lint` to gather the wiki context.
   - Use the output from `compile_context.py` to perform the following semantic checks:
     - Identify contradictions between pages (claims that conflict)
     - Identify stale content (summaries that newer sources have superseded)
     - Identify data gaps (important questions the wiki can't answer — suggest specific sources to find)
     - Identify concepts mentioned but lacking depth

3. Return a markdown lint report with these sections:
   ## Contradictions
   ## Stale Content
   ## Data Gaps & Suggested Sources
   ## Concepts Needing More Depth

Be specific — name the exact pages and claims involved.

You receive a pre-compiled context. Do NOT read wiki/index.md yourself.
