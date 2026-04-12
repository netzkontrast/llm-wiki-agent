---
name: wiki-graph
description: Rebuilds the knowledge graph and detects communities
---

This skill rebuilds the wiki's knowledge graph. It is purely deterministic and does not use the LLM to infer semantic edges.

Steps:
1. Run `python3 tools/build_graph.py` (add `--open` if the user requests to see it)
2. Report the number of nodes and edges generated.
