# Characters

Character profiles for all named entities in the novel. Each page covers one character's identity, psychology, voice, relationships, and arc — for the temporal window defined by `valid_from`/`valid_until`.

## Pages
- [Kael.md](Kael.md) — protagonist, ANP host, pre-fragmentation state (valid_until: 010-fragmentation-revealed)
- [AEGIS.md](AEGIS.md) — antagonist, coherence-enforcement system, timeless

## Connections
- Related to: `wiki/narrative/arcs/` — each character links to their arc page
- Related to: `wiki/narrative/chapters/` — chapters list which characters appear (`characters:` field)
- Related to: `wiki/narrative/conflicts/` — conflicts list character parties
- Referenced by: `wiki/reader_state/reader-model/` — reader-state tracks character introductions via `terminology_permitted`

## Routing Layer
Part of the **Narrative Layer** — see [`wiki/narrative/README.md`](../README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `TitleCase.md` (e.g., `Kael.md`, `AEGIS.md`)
- Temporal: Yes — characters with significant state changes across the story use `valid_from`/`valid_until` to scope each page to its story window. Post-fragmentation Kael will be a separate page.
- Multi-page characters: When a character's arc produces a significant state change, create a new page for the new state rather than modifying the existing one. Both pages coexist, scoped by timeline-event slugs.
