# Reader State Layer — Monotonically Accumulating Reader Knowledge

This layer models what the reader knows at each point in the narrative. It accumulates
monotonically — knowledge is added, never removed (Terminology Ratchet).

**All page content lives as subdirectories here (not at wiki root):**

| Dir | Type | What it contains |
|---|---|---|
| `reader-model/` | reader-state | Per-chapter reader knowledge states |
| `foreshadowing/` | foreshadowing | Strands: `planted` → `reinforced` → `resolved` |

## Mutation rule
Accumulates monotonically. `terminology_permitted` is a one-way ratchet — once a
term is unlocked it cannot be removed. New entries are added after each chapter;
existing entries are never deleted.

## When to load
- During `wiki-ingest-reader` sub-skill (usually manual, after chapter writing)
- During manuscript-drafting workflow (constraint check)
- During wiki-lint workflow (terminology-ratchet validation)
- qmd collection: `reader-state` — `qmd search "term" -c reader-state`
