# Phase 5: Writing Pipeline (Beats, Outlines, Manuscripts)

**Status:** `complete`
**Prerequisites:** Phase 1 complete (directories and seed pages exist)
**Spec reference:** `docs/writing-pipeline.md`

## Purpose

Implement the writing pipeline that separates chapter specs, outlines, beats, and manuscripts into distinct page types with their own lifecycles, workflows, and dependency chains. Refine the existing chapter type to serve as a pure metadata hub.

---

## Tasks

### Directory Creation

- [x] 1. Create new wiki directories: `wiki/beats/`, `wiki/outlines/`, `wiki/manuscripts/`
- [x] 2. Add `.gitkeep` to each new directory

### Schema Updates

- [x] 3. Update chapter seed page (`wiki/chapters/chapter-01.md`): replace `draft_status` with `outline_ref` and `manuscript_ref` fields; remove `## Scene Beats` section. Reference `docs/writing-pipeline.md` "Chapter Page Refinement" section.
- [x] 4. Verify `docs/wiki-schema.md` has all 14 page types documented with complete frontmatter (11 original + beat + outline + manuscript). The chapter type must show `outline_ref`/`manuscript_ref` instead of `draft_status`.

### Seed Templates

Create realistic example pages for chapter 1 to test the pipeline end-to-end. Use frontmatter schemas from `docs/writing-pipeline.md`.

- [x] 5. Create `wiki/outlines/chapter-01-outline.md` — `outline_status: detailed`, `beats: [beats/chapter-01-beat-01, beats/chapter-01-beat-02, beats/chapter-01-beat-03]`, `arc_function: setup`, `requires: [chapters/chapter-01, characters/Kael, conflicts/KaelVsAegis]`, `informs: [beats/chapter-01-beat-01, beats/chapter-01-beat-02, beats/chapter-01-beat-03, manuscripts/chapter-01-manuscript]`
- [x] 6. Create `wiki/beats/chapter-01-beat-01.md` — opening beat, `characters_present: [Kael]`, `location: LogosPrime`, `tension_direction: rising`, `tension_delta: 1`, `foreshadowing_action: "the-cage-motif:plant"`, `requires: [chapters/chapter-01, characters/Kael, locations/LogosPrime]`, `informs: [outlines/chapter-01-outline, manuscripts/chapter-01-manuscript]`
- [x] 7. Create `wiki/beats/chapter-01-beat-02.md` — escalation beat, `conflicts_active: [KaelVsAegis]`, `tension_direction: rising`, `tension_delta: 2`
- [x] 8. Create `wiki/beats/chapter-01-beat-03.md` — chapter-end beat, `tension_direction: turning-point`, `tension_delta: 1`
- [x] 9. Create `wiki/manuscripts/chapter-01-manuscript.md` — `manuscript_status: not-started`, `pov_voice_ref: Kael`, `requires: [outlines/chapter-01-outline, characters/Kael, rules/MaxOneNewConceptPerScene]`, `informs: [reader-model/chapter-01-state, chapters/chapter-01]`

### Index & Cross-Reference Updates

- [x] 10. Update `wiki/index.md` with new sections: Outlines, Beats, Manuscripts — add entries for all seed pages
- [x] 11. Update chapter-01 seed page: set `outline_ref: outlines/chapter-01-outline`, `manuscript_ref: manuscripts/chapter-01-manuscript`
- [x] 12. Verify all cross-references: every slug in `requires:`, `informs:`, `beats:`, `outline_ref`, `manuscript_ref` resolves to an existing page

### Workflow Slash Commands

- [x] 13. Create `.claude/commands/wiki-outline.md` — triggers: "outline/structure/plan chapter N". References outline-writing workflow in `docs/writing-pipeline.md`.
- [x] 14. Create `.claude/commands/wiki-beats.md` — triggers: "detail/expand beats for chapter N". References beat-detailing workflow.
- [x] 15. Create `.claude/commands/wiki-manuscript.md` — triggers: "write/draft prose for chapter N". References manuscript-drafting workflow.
- [x] 16. Update `.claude/commands/wiki-chapter.md` (if exists) to serve as orchestrator: delegates to outline → beats → manuscript based on current state.

### Validation

- [x] 17. Test outline-writing workflow: verify it loads chapter spec + characters + conflicts correctly
- [x] 18. Test manuscript-drafting workflow: verify it requires outline to be `detailed` or `locked` before proceeding
- [x] 19. Test `informs:` propagation: modify a beat page and verify the chain reaches manuscript and reader-state pages
- [x] 20. Verify the chapter page no longer has `draft_status` or `## Scene Beats`

---

## Completion Criteria

- 3 new directories exist: `wiki/beats/`, `wiki/outlines/`, `wiki/manuscripts/`
- `docs/writing-pipeline.md` has complete specs for beat, outline, manuscript types
- Chapter type refined: `outline_ref`/`manuscript_ref` replace `draft_status`
- At least 5 seed pages (1 outline + 3 beats + 1 manuscript) with cross-referenced frontmatter
- Pipeline dependency chain verified: chapter → outline → beats → manuscript → reader-state
- `wiki/index.md` updated with Outlines, Beats, Manuscripts sections

When all tasks are checked, update the phase table in `todo/README.md`: set Phase 5 to `complete`.
