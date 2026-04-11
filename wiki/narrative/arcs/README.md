# Arcs

Arc tracking pages. Each page tracks one transformation arc across the story — character arcs, plot arcs, or thematic arcs. Arcs record stages, current state, and what is being transformed.

## Pages
- [kael-integration-arc.md](kael-integration-arc.md) — character arc, subject: Kael — False Coherence → Fragmentation Exposed → Attempted Strategies → Goedel Gambit

## Connections
- Related to: `wiki/narrative/characters/` — characters link to their arc via `arc:` field; arcs reference their `subject:` character
- Related to: `wiki/narrative/chapters/` — arc stages reference chapter numbers where stage transitions occur
- Related to: `wiki/narrative/conflicts/` — conflict resolution trajectories often parallel arc stages
- Related to: `wiki/narrative/timeline/` — arc stage transitions typically align with boundary events

## Routing Layer
Part of the **Narrative Layer** — see [`wiki/narrative/README.md`](../README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `kebab-case.md` (e.g., `kael-integration-arc.md`, `aegis-escalation-arc.md`)
- Temporal: No — arc pages track the full transformation; individual stages record their chapter reference
