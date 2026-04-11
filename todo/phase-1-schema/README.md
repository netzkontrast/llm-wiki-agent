# Phase 1: Wiki Schema Extension

**Status:** `complete`
**Prerequisites:** None
**Spec reference:** `docs/wiki-schema.md`

## Purpose

Implement the 11 new page types, create all new wiki directories, define frontmatter
schemas, and seed the wiki with realistic template pages for testing.

> **Migration note:** Phase 1 was completed with a flat `wiki/` structure. The
> redesigned 4-layer nested layout (`wiki/narrative/characters/` etc.) is implemented
> as a migration task in Phase 6, Group A (task A0). See `todo/phase-6-adaptive-ingest/README.md`.

---

## Tasks (all complete)

### Directory Creation

- [x] 1. Create all new wiki directories: `wiki/characters/`, `wiki/chapters/`, `wiki/locations/`, `wiki/conflicts/`, `wiki/themes/`, `wiki/timeline/`, `wiki/rules/`, `wiki/arcs/`, `wiki/dramatica/`, `wiki/reader-model/`, `wiki/foreshadowing/`, `wiki/archive/`, `wiki/meta/`, `wiki/beats/`, `wiki/outlines/`, `wiki/manuscripts/`
- [x] 2. Add `.gitkeep` to each empty directory so git tracks them

### Index Update

- [x] 3. Update `wiki/index.md` to include all new sections (Characters, Chapters, Locations, Conflicts, Themes, Timeline, Rules, Arcs, Dramatica, Reader Model, Foreshadowing) — follow the extended index format in `docs/wiki-schema.md`

### Seed Templates

- [x] 4. Create `wiki/timeline/001-story-begins.md` — boundary event (`is_boundary: true`, `sequence_number: 1`)
- [x] 5. Create `wiki/timeline/010-fragmentation-revealed.md` — boundary event (`is_boundary: true`, `sequence_number: 10`)
- [x] 6. Create `wiki/timeline/028-goedel-gambit.md` — boundary event (`is_boundary: true`, `sequence_number: 28`)
- [x] 7. Create `wiki/characters/Kael.md`
- [x] 8. Create `wiki/characters/AEGIS.md`
- [x] 9. Create `wiki/chapters/chapter-01.md`
- [x] 10. Create `wiki/locations/LogosPrime.md`
- [x] 11. Create `wiki/conflicts/KaelVsAegis.md`
- [x] 12. Create `wiki/themes/IntegrationVsFragmentation.md`
- [x] 13. Create `wiki/rules/CoherenceTheoryOfTruth.md`
- [x] 14. Create `wiki/rules/MaxOneNewConceptPerScene.md`
- [x] 15. Create `wiki/foreshadowing/the-cage-motif.md`
- [x] 16. Create `wiki/reader-model/chapter-01-state.md`
- [x] 17. Create `wiki/arcs/kael-integration-arc.md`

### Index Population

- [x] 18. Update `wiki/index.md` with entries for all seed pages created above
- [x] 19. Verify all cross-references

### Folder READMEs

- [x] 20. Create README.md for each new wiki/ subdirectory
- [x] 21. Each README contains: purpose, naming convention, page type, connections, temporal filter flag
- [x] 22. Link each folder README to its parent layer README (knowledge/, narrative/, reader_state/, meta/)

---

## Completion Criteria — all met

When all tasks are checked, update the phase table in `todo/README.md`: set Phase 1 to `complete`, Phase 2 to `active`.
