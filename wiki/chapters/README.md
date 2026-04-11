# Chapters

Chapter specification pages — one per chapter. Each page is a metadata hub: it records POV, pacing, characters, locations, conflicts, themes, timeline bounds, and constraints. Prose lives in `wiki/manuscripts/`; scene structure lives in `wiki/outlines/` and `wiki/beats/`.

## Pages
- [chapter-01.md](chapter-01.md) — Chapter 1: The Sterile Beginning, pov: Kael, setup

## Connections
- Related to: `wiki/characters/` — `pov:` and `characters:` fields reference character slugs
- Related to: `wiki/locations/` — `locations:` field references location slugs
- Related to: `wiki/conflicts/` — `conflicts:` field references active conflict slugs
- Related to: `wiki/themes/` — `themes:` field references theme slugs
- Related to: `wiki/rules/` — `constraint_refs:` field references rules that govern the chapter
- Related to: `wiki/timeline/` — `timeline_start:` and `timeline_end:` reference boundary event slugs
- Related to: `wiki/outlines/` — `outline_ref:` links to the chapter's outline page
- Related to: `wiki/manuscripts/` — `manuscript_ref:` links to the chapter's manuscript page
- Referenced by: `wiki/reader-model/` — each reader-state page corresponds to one chapter

## Routing Layer
Part of the **Narrative Layer** — see [`wiki/narrative/README.md`](../narrative/README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `chapter-NN.md` (zero-padded two digits: `chapter-01.md`, `chapter-39.md`)
- Temporal: No — chapter pages themselves are not temporally scoped. They describe a fixed point in the story.
