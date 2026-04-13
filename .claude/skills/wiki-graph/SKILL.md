---
name: wiki-graph
description: Executes the following: Rebuilds the knowledge graph and detects communities. Use when the user requests wiki-graph or related tasks.
---

# wiki-graph

This skill rebuilds the wiki's knowledge graph. It is purely deterministic and does not use the LLM to infer semantic edges.

Steps:
1. Run `python3 tools/build_graph.py` (add `--open` if the user requests to see it)
2. Report the number of nodes and edges generated.

## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
