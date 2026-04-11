# Phase 1: Wiki Schema Extension

**Status:** `not-started`
**Prerequisites:** None
**Spec reference:** `docs/wiki-schema.md`

## Purpose

Implement the 11 new page types inside the 4-layer nested wiki structure, define
frontmatter schemas, and seed the wiki with realistic template pages for testing.

**Directory structure:** All page type directories live *inside* their layer folder
(`wiki/knowledge/sources/`, `wiki/narrative/characters/`, etc.) — not at `wiki/` root.
Two timelines exist: `knowledge/timeline/` (research provenance) and
`narrative/timeline/` (story-world chronology).

---

## Tasks

### Directory Creation

- [ ] 1. Create all new wiki subdirectories nested under their layer:
  ```
  wiki/knowledge/sources/
  wiki/knowledge/entities/
  wiki/knowledge/concepts/
  wiki/knowledge/rules/
  wiki/knowledge/timeline/        ← research/source provenance
  wiki/knowledge/syntheses/

  wiki/narrative/characters/
  wiki/narrative/chapters/
  wiki/narrative/locations/
  wiki/narrative/conflicts/
  wiki/narrative/themes/
  wiki/narrative/arcs/
  wiki/narrative/dramatica/
  wiki/narrative/timeline/        ← story-world chronology (boundary events)
  wiki/narrative/beats/           ← Phase 5 creates seed pages; dir created here
  wiki/narrative/outlines/        ← Phase 5 creates seed pages; dir created here
  wiki/narrative/manuscripts/     ← Phase 5 creates seed pages; dir created here

  wiki/reader_state/reader-model/
  wiki/reader_state/foreshadowing/

  wiki/meta/archive/
  wiki/meta/ingest/
  ```
- [ ] 2. Add `.gitkeep` to each empty directory so git tracks them
- [ ] 3. Update `CLAUDE.md` Directory Layout section to show the nested 4-layer structure
        (replace the flat layout with the layered one per `docs/adaptive-ingest.md`)

### Index Update

- [ ] 4. Update `wiki/index.md` to include all new sections with nested paths:
        (Characters, Chapters, Locations, Conflicts, Themes, Timeline ×2, Rules, Arcs,
        Dramatica, Reader Model, Foreshadowing, Syntheses) — follow `docs/wiki-schema.md`

### Seed Templates

Create realistic example pages to give Phase 2 content to test navigation against.
Use frontmatter schemas defined in `docs/wiki-schema.md`. Content can be brief but
frontmatter must be complete and cross-referenced.

**Narrative timeline seeds (story-world boundary events):**
- [ ] 5. Create `wiki/narrative/timeline/001-story-begins.md` — `is_boundary: true`, `sequence_number: 1`
- [ ] 6. Create `wiki/narrative/timeline/010-fragmentation-revealed.md` — `is_boundary: true`, `sequence_number: 10`
- [ ] 7. Create `wiki/narrative/timeline/028-goedel-gambit.md` — `is_boundary: true`, `sequence_number: 28`

**Character seeds:**
- [ ] 8. Create `wiki/narrative/characters/Kael.md` — protagonist, host, ANP,
        `valid_from: ""`, `valid_until: "010-fragmentation-revealed"`,
        `traits: {voice_profile: "fragmented-internal", somatic: "chest-pressure", pov_mode: "first", response_type: "freeze"}`,
        `requires: [narrative/locations/LogosPrime]`,
        `informs: [narrative/chapters/chapter-01, narrative/arcs/kael-integration-arc]`
- [ ] 9. Create `wiki/narrative/characters/AEGIS.md` — antagonist,
        `informs: [narrative/conflicts/KaelVsAegis]`

**Chapter, location, conflict, theme seeds:**
- [ ] 10. Create `wiki/narrative/chapters/chapter-01.md` — `pov: Kael`,
         `constraint_refs: [knowledge/rules/MaxOneNewConceptPerScene]`,
         `characters: [Kael]`, `locations: [LogosPrime]`, `conflicts: [KaelVsAegis]`,
         `themes: [IntegrationVsFragmentation]`,
         `timeline_start: 001-story-begins`, `max_new_concepts: 1`
- [ ] 11. Create `wiki/narrative/locations/LogosPrime.md` — core world KW1,
         `psychological_mapping: "rigid control, suppressed chaos"`,
         `sensory_palette: [sterile-white, humming-silence]`
- [ ] 12. Create `wiki/narrative/conflicts/KaelVsAegis.md` — `self_referential: true`,
         `paradox_source: "AEGIS enforces coherence, but coherence-enforcement generates the fragmentation it claims to prevent"`,
         `conflict_type: external`, `resolution_status: open`
- [ ] 13. Create `wiki/narrative/themes/IntegrationVsFragmentation.md` — central theme,
         `counter_theme: ""`, `motifs: [the-cage, the-mirror, breath]`

**Rule seeds (knowledge layer):**
- [ ] 14. Create `wiki/knowledge/rules/CoherenceTheoryOfTruth.md` — `rule_class: world`, `domain: logic`
- [ ] 15. Create `wiki/knowledge/rules/MaxOneNewConceptPerScene.md` — `rule_class: narrative`, `domain: psychology`

**Reader state and foreshadowing seeds:**
- [ ] 16. Create `wiki/reader_state/foreshadowing/the-cage-motif.md` — `status: planted`,
         `planted_chapter: 1`, `related_themes: [IntegrationVsFragmentation]`
- [ ] 17. Create `wiki/reader_state/reader-model/chapter-01-state.md` —
         `terminology_permitted: [Kael, LogosPrime, coherence]`,
         `knows: []`, `learns: [Kael-exists, LogosPrime-is-sterile]`, `tension_level: 3`

**Arc seed:**
- [ ] 18. Create `wiki/narrative/arcs/kael-integration-arc.md` — `arc_type: character`,
         `subject: Kael`, initial stages

### Index Population

- [ ] 19. Update `wiki/index.md` with entries for all seed pages, using nested paths
- [ ] 20. Verify all cross-references: every slug in `requires:`, `informs:`,
         `constraint_refs:`, `characters:`, `locations:`, `conflicts:`, `themes:`
         resolves to an existing page (use nested paths throughout)

### Folder READMEs

Each page-type subdirectory needs its own README (the layer READMEs already exist):

- [ ] 21. Create `README.md` for each new subdirectory: `knowledge/sources/`,
         `knowledge/entities/`, `knowledge/concepts/`, `knowledge/rules/`,
         `knowledge/timeline/`, `knowledge/syntheses/`,
         `narrative/characters/`, `narrative/chapters/`, `narrative/locations/`,
         `narrative/conflicts/`, `narrative/themes/`, `narrative/arcs/`,
         `narrative/dramatica/`, `narrative/timeline/`,
         `narrative/beats/`, `narrative/outlines/`, `narrative/manuscripts/`,
         `reader_state/reader-model/`, `reader_state/foreshadowing/`,
         `meta/archive/`, `meta/ingest/`
- [ ] 22. Each README contains: purpose, naming convention, page type, connections to
         other dirs, whether temporally filtered
- [ ] 23. Each README references its parent layer README
         (e.g. `narrative/characters/README.md` → `narrative/README.md`)

---

## Completion Criteria

- All directories exist nested under their layer (no flat page-type dirs at `wiki/` root)
- `CLAUDE.md` Directory Layout section shows the 4-layer nested structure
- `wiki/index.md` has all sections with correct nested paths
- At least 14 seed pages created with complete, cross-referenced frontmatter
- All `requires:`/`informs:` references resolve to existing pages (nested paths)
- All `valid_from`/`valid_until` reference narrative timeline-event pages
- All new subdirectories have a README.md

When all tasks are checked, update `todo/README.md`: set Phase 1 to `complete`, Phase 2 to `active`.
