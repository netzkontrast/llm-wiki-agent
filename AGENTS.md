# LLM Wiki Agent — Schema & Workflow Instructions

This wiki is maintained entirely by your coding agent. No API key or Python scripts needed — just open this repo in Codex, OpenCode, or any agent that reads this file, and talk to it.

## How to Use

Describe what you want in plain English:
- *"Ingest this file: raw/papers/my-paper.md"*
- *"What does the wiki say about transformer models?"*
- *"Check the wiki for orphan pages and contradictions"*
- *"Build the knowledge graph"*

Or use shorthand triggers:
- `ingest <file>` → runs the Ingest Workflow
- `query: <question>` → runs the Query Workflow
- `lint` → runs the Lint Workflow
- `build graph` → runs the Graph Workflow

---

## Directory Layout

```
raw/          # Immutable source documents — waiting for ingestion
processed/    # Source documents that have been ingested — moved from raw/
memory/L0_facts/    # Immutable, high-fidelity extractions directly from raw sources
memory/L1_episodes/ # Chronological provenance and temporal connections between ingested files
wiki/         # Agent owns this layer entirely (L2 Synthesized Concepts)
  index.md    # Catalog of all pages — update on every ingest
  log.md      # Append-only chronological record
  overview.md # Living synthesis across all sources
  knowledge/  # Routing layer: concepts, entities, sources, rules, timeline
  narrative/  # Routing layer: characters, chapters, locations, conflicts, themes, arcs, dramatica, beats, outlines, manuscripts
  reader_state/ # Routing layer: reader-model, foreshadowing
  meta/       # Routing layer: archive, ingest, logs, contradiction-log, protocols
graph/        # Auto-generated graph data
tools/        # Optional standalone Python scripts (require ANTHROPIC_API_KEY)
```

---

## Setup & Commands
Activate virtual environment: `uv venv && source .venv/bin/activate`
Install dependencies: `uv sync`

## Testing Protocol
Run file-scoped tests first: `uv run pytest tests/unit/`. Run full suite ONLY when explicitly requested.

## Code Style
Python: PEP 8. Formatting: Ruff. Use functional patterns where possible.

## Security & Guardrails
NEVER commit .env files. Store secrets in environment variables.

---

## Ingest Workflow

Triggered by: *"ingest <file>"*

Steps (in order):
1. Execute `python3 .claude/skills/wiki-ingest/scripts/ingest_router.py <file>` to route to L0 and L1.
2. Read the source document fully.
3. Read `wiki/index.md` and `wiki/overview.md` for current wiki context.
4. Synthesize L2 concepts. DO NOT overwrite pages if they contradict, use `[!contradiction]` block instead.

## Query Workflow
...
