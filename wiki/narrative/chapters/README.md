# Chapters

Chapter specification pages — one per chapter. Each page is a metadata hub: it records POV, pacing, characters, locations, conflicts, themes, timeline bounds, and constraints. Prose lives in `wiki/narrative/manuscripts/`; scene structure lives in `wiki/narrative/outlines/` and `wiki/narrative/beats/`.

## Pages
- [chapter-01.md](chapter-01.md) — Chapter 1: The Sterile Beginning, pov: Kael, setup

## Connections
- Related to: `wiki/narrative/characters/` — `pov:` and `characters:` fields reference character slugs
- Related to: `wiki/narrative/locations/` — `locations:` field references location slugs
- Related to: `wiki/narrative/conflicts/` — `conflicts:` field references active conflict slugs
- Related to: `wiki/narrative/themes/` — `themes:` field references theme slugs
- Related to: `wiki/knowledge/rules/` — `constraint_refs:` field references rules that govern the chapter
- Related to: `wiki/narrative/timeline/` — `timeline_start:` and `timeline_end:` reference boundary event slugs
- Related to: `wiki/narrative/outlines/` — `outline_ref:` links to the chapter's outline page
- Related to: `wiki/narrative/manuscripts/` — `manuscript_ref:` links to the chapter's manuscript page
- Referenced by: `wiki/reader_state/reader-model/` — each reader-state page corresponds to one chapter

## Routing Layer
Part of the **Narrative Layer** — see [`wiki/narrative/README.md`](../README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `chapter-NN.md` (zero-padded two digits: `chapter-01.md`, `chapter-39.md`)
- Temporal: No — chapter pages themselves are not temporally scoped. They describe a fixed point in the story.
