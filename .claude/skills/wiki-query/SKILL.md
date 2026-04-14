---
name: wiki-query
description: Executes the following: Queries the wiki and synthesizes an answer. Use when the user requests wiki-query or related tasks.
---

# wiki-query

## Steps

1. Run `python3 tools/compile_context.py --task query --query ""[question]""` to gather the wiki context relevant to the user's query.
2. Using the compiled context, synthesize a thorough answer to the user's question.
3. Cite sources using `[[PageName]]` wikilink syntax.
4. Write a well-structured markdown answer with headers, bullets, and `[[wikilink]]` citations.
5. At the end, add a `## Sources` section listing the pages you drew from.
6. If the user requests to save the answer, write it to `wiki/syntheses/"[slug]".md` and append it to `wiki/index.md` using the required tagged format: `- [Title](path) — description <!-- type:synthesis slug:slug -->`

You receive a pre-compiled context. Do NOT read wiki/index.md yourself.

## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
