---
name: wiki-query
description: Queries the wiki and synthesizes an answer
---

## Steps

1. Run `python3 tools/compile_context.py --task query --query "<question>"` to gather the wiki context relevant to the user's query.
2. Using the compiled context, synthesize a thorough answer to the user's question.
3. Cite sources using `[[PageName]]` wikilink syntax.
4. Write a well-structured markdown answer with headers, bullets, and `[[wikilink]]` citations.
5. At the end, add a `## Sources` section listing the pages you drew from.
6. If the user requests to save the answer, write it to `wiki/syntheses/<slug>.md` and append it to `wiki/index.md` using the required tagged format: `- [Title](path) — description <!-- type:synthesis slug:slug -->`

You receive a pre-compiled context. Do NOT read wiki/index.md yourself.
