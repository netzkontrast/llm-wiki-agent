# Phase 1: Wiki Schema Extension

**Status:** `not-started`
**Prerequisites:** None
**Spec reference:** `docs/wiki-schema.md`

## Purpose

Implement the 11 new page types, create all new wiki directories, define frontmatter schemas, and seed the wiki with realistic template pages for testing.

---

## Tasks

### Directory Creation

- [ ] 1. Create all new wiki directories: `wiki/characters/`, `wiki/chapters/`, `wiki/locations/`, `wiki/conflicts/`, `wiki/themes/`, `wiki/timeline/`, `wiki/rules/`, `wiki/arcs/`, `wiki/dramatica/`, `wiki/reader-model/`, `wiki/foreshadowing/`, `wiki/archive/`, `wiki/meta/`
- [ ] 2. Add `.gitkeep` to each empty directory so git tracks them

### Index Update

- [ ] 3. Update `wiki/index.md` to include all new sections (Characters, Chapters, Locations, Conflicts, Themes, Timeline, Rules, Arcs, Dramatica, Reader Model, Foreshadowing) — follow the extended index format in `docs/wiki-schema.md`

### Seed Templates

Create realistic example pages to give Phase 2 content to test navigation against. Use the frontmatter schemas defined in `docs/wiki-schema.md`. Content can be brief but frontmatter must be complete and cross-referenced.

- [ ] 4. Create `wiki/timeline/001-story-begins.md` — boundary event (`is_boundary: true`, `sequence_number: 1`)
- [ ] 5. Create `wiki/timeline/010-fragmentation-revealed.md` — boundary event (`is_boundary: true`, `sequence_number: 10`)
- [ ] 6. Create `wiki/timeline/028-goedel-gambit.md` — boundary event (`is_boundary: true`, `sequence_number: 28`)
- [ ] 7. Create `wiki/characters/Kael.md` — protagonist, host, ANP, `valid_from: ""`, `valid_until: "010-fragmentation-revealed"`, traits: `{voice_profile: "fragmented-internal", somatic: "chest-pressure", pov_mode: "first", response_type: "freeze"}`, requires: `[locations/LogosPrime]`, informs: `[chapters/chapter-01, arcs/kael-integration-arc]`
- [ ] 8. Create `wiki/characters/AEGIS.md` — antagonist, with `informs: [conflicts/KaelVsAegis]`
- [ ] 9. Create `wiki/chapters/chapter-01.md` — full frontmatter: `pov: Kael`, `constraint_refs: [rules/MaxOneNewConceptPerScene]`, `characters: [Kael]`, `locations: [LogosPrime]`, `conflicts: [KaelVsAegis]`, `themes: [IntegrationVsFragmentation]`, `timeline_start: 001-story-begins`, `max_new_concepts: 1`
- [ ] 10. Create `wiki/locations/LogosPrime.md` — core world KW1, `psychological_mapping: "rigid control, suppressed chaos"`, `sensory_palette: [sterile-white, humming-silence]`
- [ ] 11. Create `wiki/conflicts/KaelVsAegis.md` — `self_referential: true`, `paradox_source: "AEGIS enforces coherence, but coherence-enforcement generates the fragmentation it claims to prevent"`, `conflict_type: external`, `resolution_status: open`
- [ ] 12. Create `wiki/themes/IntegrationVsFragmentation.md` — central theme, `counter_theme: ""`, `motifs: [the-cage, the-mirror, breath]`
- [ ] 13. Create `wiki/rules/CoherenceTheoryOfTruth.md` — `rule_class: world`, `domain: logic`, constraints
- [ ] 14. Create `wiki/rules/MaxOneNewConceptPerScene.md` — `rule_class: narrative`, `domain: psychology`, constraints
- [ ] 15. Create `wiki/foreshadowing/the-cage-motif.md` — `status: planted`, `planted_chapter: 1`, `related_themes: [IntegrationVsFragmentation]`
- [ ] 16. Create `wiki/reader-model/chapter-01-state.md` — `terminology_permitted: [Kael, LogosPrime, coherence]`, `knows: []`, `learns: [Kael-exists, LogosPrime-is-sterile]`, `tension_level: 3`
- [ ] 17. Create `wiki/arcs/kael-integration-arc.md` — `arc_type: character`, `subject: Kael`, initial stages

### Index Population

- [ ] 18. Update `wiki/index.md` with entries for all seed pages created above
- [ ] 19. Verify all cross-references: every slug in `requires:`, `informs:`, `constraint_refs:`, `characters:`, `locations:`, `conflicts:`, `themes:` resolves to an existing page

---

## Completion Criteria

- All 13 new directories exist under `wiki/`
- `wiki/index.md` has all 15 sections (4 original + 11 new)
- At least 13 seed pages created with complete, cross-referenced frontmatter
- All `requires:`/`informs:` references resolve to existing pages
- All `valid_from`/`valid_until` references point to existing timeline-event pages with `is_boundary: true`

When all tasks are checked, update the phase table in `todo/README.md`: set Phase 1 to `complete`, Phase 2 to `active`.
