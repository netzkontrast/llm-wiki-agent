# Reader Model

Reader-state pages — one per chapter. Each page tracks what the reader knows, learns, and feels at a given story point. The `terminology_permitted` field is a one-way ratchet: every term introduced in chapter N carries forward to chapter N+1. See `docs/reader-model.md` for the full progressive disclosure spec.

## Pages
- [chapter-01-state.md](chapter-01-state.md) — Chapter 1, tension_level: 3 — Kael and LogosPrime introduced; cage motif planted

## Connections
- Related to: `wiki/narrative/chapters/` — one reader-state page per chapter, linked by chapter number
- Related to: `wiki/reader_state/foreshadowing/` — `foreshadowing_planted:` and `foreshadowing_resolved:` reference foreshadowing slugs
- Related to: `wiki/knowledge/rules/` — `constraints_active:` references rule pages governing reader experience at this point
- Referenced by: `wiki/reader_state/README.md` — reader model is part of the reader-state routing layer

## Routing Layer
Part of the **Reader State Layer** — see [`wiki/reader_state/README.md`](../README.md) for loading rules and ratchet constraints.

## Conventions
- Naming: `chapter-NN-state.md` (e.g., `chapter-01-state.md`, `chapter-10-state.md`)
- Temporal: No — each page describes the reader's state at a fixed story point; the ratchet is encoded in the cumulative `terminology_permitted` list
- Ratchet rule: `terminology_permitted` in chapter N must be a superset of chapter N-1's `terminology_permitted`
