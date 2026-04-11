# Phase 1: Wiki Schema Extension

**Status:** `complete`
**Prerequisites:** None
**Spec reference:** `docs/wiki-schema.md`

## Purpose

Implement the 11 new page types, create all new wiki directories, define frontmatter schemas, and seed the wiki with realistic template pages for testing.

---

## Tasks

### Directory Creation

- [x] 1. Create all new wiki directories: `wiki/characters/`, `wiki/chapters/`, `wiki/locations/`, `wiki/conflicts/`, `wiki/themes/`, `wiki/timeline/`, `wiki/rules/`, `wiki/arcs/`, `wiki/dramatica/`, `wiki/reader-model/`, `wiki/foreshadowing/`, `wiki/archive/`, `wiki/meta/`, `wiki/beats/`, `wiki/outlines/`, `wiki/manuscripts/`
- [x] 2. Add `.gitkeep` to each empty directory so git tracks them

### Index Update

- [x] 3. Update `wiki/index.md` to include all new sections (Characters, Chapters, Locations, Conflicts, Themes, Timeline, Rules, Arcs, Dramatica, Reader Model, Foreshadowing) — follow the extended index format in `docs/wiki-schema.md`

### Seed Templates

Create realistic example pages to give Phase 2 content to test navigation against. Use the frontmatter schemas defined in `docs/wiki-schema.md`. Content can be brief but frontmatter must be complete and cross-referenced.

- [x] 4. Create `wiki/timeline/001-story-begins.md` — boundary event (`is_boundary: true`, `sequence_number: 1`)
- [x] 5. Create `wiki/timeline/010-fragmentation-revealed.md` — boundary event (`is_boundary: true`, `sequence_number: 10`)
- [x] 6. Create `wiki/timeline/028-goedel-gambit.md` — boundary event (`is_boundary: true`, `sequence_number: 28`)
- [x] 7. Create `wiki/characters/Kael.md` — protagonist, host, ANP, `valid_from: ""`, `valid_until: "010-fragmentation-revealed"`, traits: `{voice_profile: "fragmented-internal", somatic: "chest-pressure", pov_mode: "first", response_type: "freeze"}`, requires: `[locations/LogosPrime]`, informs: `[chapters/chapter-01, arcs/kael-integration-arc]`
- [x] 8. Create `wiki/characters/AEGIS.md` — antagonist, with `informs: [conflicts/KaelVsAegis]`
- [x] 9. Create `wiki/chapters/chapter-01.md` — full frontmatter: `pov: Kael`, `constraint_refs: [rules/MaxOneNewConceptPerScene]`, `characters: [Kael]`, `locations: [LogosPrime]`, `conflicts: [KaelVsAegis]`, `themes: [IntegrationVsFragmentation]`, `timeline_start: 001-story-begins`, `max_new_concepts: 1`
- [x] 10. Create `wiki/locations/LogosPrime.md` — core world KW1, `psychological_mapping: "rigid control, suppressed chaos"`, `sensory_palette: [sterile-white, humming-silence]`
- [x] 11. Create `wiki/conflicts/KaelVsAegis.md` — `self_referential: true`, `paradox_source: "AEGIS enforces coherence, but coherence-enforcement generates the fragmentation it claims to prevent"`, `conflict_type: external`, `resolution_status: open`
- [x] 12. Create `wiki/themes/IntegrationVsFragmentation.md` — central theme, `counter_theme: ""`, `motifs: [the-cage, the-mirror, breath]`
- [x] 13. Create `wiki/rules/CoherenceTheoryOfTruth.md` — `rule_class: world`, `domain: logic`, constraints
- [x] 14. Create `wiki/rules/MaxOneNewConceptPerScene.md` — `rule_class: narrative`, `domain: psychology`, constraints
- [x] 15. Create `wiki/foreshadowing/the-cage-motif.md` — `status: planted`, `planted_chapter: 1`, `related_themes: [IntegrationVsFragmentation]`
- [x] 16. Create `wiki/reader-model/chapter-01-state.md` — `terminology_permitted: [Kael, LogosPrime, coherence]`, `knows: []`, `learns: [Kael-exists, LogosPrime-is-sterile]`, `tension_level: 3`
- [x] 17. Create `wiki/arcs/kael-integration-arc.md` — `arc_type: character`, `subject: Kael`, initial stages

### Index Population

- [x] 18. Update `wiki/index.md` with entries for all seed pages created above
- [x] 19. Verify all cross-references: every slug in `requires:`, `informs:`, `constraint_refs:`, `characters:`, `locations:`, `conflicts:`, `themes:` resolves to an existing page

### Folder READMEs (Navigations-Layer)

- [x] 20. Erstelle README.md für jedes neue wiki/-Unterverzeichnis: characters/, chapters/, locations/, conflicts/, themes/, timeline/, rules/, arcs/, dramatica/, reader-model/, foreshadowing/, beats/, outlines/, manuscripts/, archive/
- [x] 21. Jede README enthält: Zweck, Namenskonvention, Seitentyp, Verbindungen zu anderen Verzeichnissen, ob temporal gefiltert wird
- [x] 22. Verlinke jede Folder-README zur passenden Wiki-Oberschicht-README (knowledge/, narrative/, reader_state/, meta/)

---

## Completion Criteria

- All 16 new directories exist under `wiki/`
- `wiki/index.md` has all 18 sections (4 original + 14 new)
- At least 13 seed pages created with complete, cross-referenced frontmatter
- All `requires:`/`informs:` references resolve to existing pages
- All `valid_from`/`valid_until` references point to existing timeline-event pages with `is_boundary: true`
- All new wiki/ subdirectories have a README.md linked to their Oberschicht

When all tasks are checked, update the phase table in `todo/README.md`: set Phase 1 to `complete`, Phase 2 to `active`.
