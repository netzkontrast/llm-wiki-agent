# Session Handover — 2026-04-10

## What Was Done

### Commit 1: Initial Architecture (68b4339)
Created the complete novel-author wiki extension framework:
- **`Concept.md`** — project vision and architecture overview
- **`docs/`** (6 files) — reference specs for page types, navigation, workflows, reader model, Dramatica
- **`todo/`** (6 files) — 4 implementation phases + meta maintenance folder
- **`CLAUDE.md`** — appended development roadmap with mandatory session-start protocol

### Commit 2: Unbounded Informs (edd1515)
Changed `informs:` traversal from depth-2 bounded to **unbounded full propagation**:
- `requires:` (reading) stays bounded at depth 2 with context ceilings
- `informs:` (writing) follows the full chain — guaranteed wiki consistency after every edit
- Added cycle protection, context window guard (pause at 20+ page chains), transitive staleness detection

### Commit 3: Writing Pipeline + Handover (this commit)
Added Phase 5 and final session deliverables:
- **`docs/writing-pipeline.md`** — beat, outline, manuscript page types with full specs
- **`todo/phase-5-writing-pipeline/`** — 20 implementation tasks
- Updated all existing docs: wiki-schema (14 types), agent-workflows (12 workflows), navigation-system (16 context-loading specs), Concept.md, docs/README.md
- Refined chapter type: replaced `draft_status` with `outline_ref`/`manuscript_ref`, removed `## Scene Beats`
- **`handover.md`** — this file
- Updated **`CLAUDE.md`** with writing pipeline references
- Rewrote **`README.md`** with full project description

---

## Architecture Decisions Made

| Decision | Rationale |
|----------|-----------|
| 14 page types (4 generic + 10 novel + 3 pipeline) coexisting with original 4 | No breaking changes; original wiki works as before |
| `requires:` bounded (depth 2), `informs:` unbounded | Protect context window on reads, guarantee consistency on writes |
| Temporal filtering via `valid_from`/`valid_until` → timeline-event slugs | Semantic anchors survive chapter reordering |
| `traits:` open map instead of fixed fields | Future-proof without schema changes; recommended keys provide vocabulary |
| `terminology_permitted` as one-way ratchet | Prevents accidental regression of reader knowledge |
| Chapter as spec hub, separate outline/beats/manuscript | Clean separation of concerns; each stage has its own lifecycle |
| Beat as standalone page type (not inline in outline) | Enables querying, cross-referencing, beat-level tension tracking |
| Contradiction hierarchy: `rule > source > character > chapter > synthesis` | Rules are authoritative; syntheses are derived |
| Phase-based todo with session-start protocol | Prevents agents from loading irrelevant specs; progressive disclosure |
| Unbounded `informs:` with cycle protection + 20-page pause | Balances consistency guarantee with practical context limits |

---

## Open Questions

### Writing Pipeline

1. **Large manuscripts:** Should manuscript pages hold full prose inline, or reference external files? A 5000-word chapter could strain context. Current spec says inline with optional split (`chapter-NN-manuscript-part-a/b.md`), but this hasn't been tested.

2. **Beat granularity:** Is `beat` granular enough, or should there be a `scene` type between beat and chapter? Some chapters might have 2-3 distinct scenes each containing multiple beats. Current answer: beats are sufficient; scenes are emergent from beat sequences.

3. **Beat ordering authority:** Should the outline page's `beats:` list be the single source of truth for beat ordering, or should beats self-order via `beat_number`? Current spec has both — potential for desync. Recommend: outline's `beats:` list is authoritative; `beat_number` is derived/convenience.

4. **Polyphonic chapters:** How should chapters with multiple POV characters map to beats? Current spec has `pov_character` per beat (can differ from chapter POV), which handles this. But should there be a chapter-level `polyphony_mode` that constrains beat POV assignments?

### Reader Model

5. **Beat-level reader tracking:** Should reader-state pages track knowledge gains per beat (fine-grained) or per chapter (current)? Beat-level is more precise but multiplies reader-state pages by 5-8x. Current answer: chapter-level mandatory, beat-level optional via `traits:`.

6. **Terminology gate enforcement:** When a concept requires prerequisites (e.g., DualKernelTheory requires CoherenceTheory), should the agent hard-block or soft-warn? Current: soft check via `requires:` on concept pages.

### Content & Language

7. **Wiki language:** The 94 raw source files are all in German. Should the wiki pages be German, English, or bilingual? Entity/concept names would naturally be in the source language, but structural metadata (frontmatter) is in English. No decision made yet.

8. **Lectoring workflow target:** Should `lectoring` operate on manuscript pages directly (editing prose inline) or produce separate annotation pages? Current spec says directly on manuscript with notes. Could also produce a `wiki/lectoring/chapter-NN-notes.md` page.

### Infrastructure

9. **Obsidian integration:** Should we generate Dataview-compatible queries or templates? The wiki is plain markdown and works in Obsidian, but Dataview could unlock powerful queries over frontmatter. Not in scope yet.

10. **Graph integration for pipeline:** Should the knowledge graph show the writing pipeline (chapter → outline → beats → manuscript) as visible edges, or should these be filtered to a separate "pipeline view"? The graph could get very dense with 39 chapters x 5-8 beats each.

---

## Ideas Generated During Design

### Tooling Ideas
- **Beat heat maps** — color-code beats by tension, character presence, or theme density across all 39 chapters. Would produce a visual overview of the novel's structure.
- **Automated tension curve validation** — compare actual `tension_level` trajectory to structural archetypes (three-act, hero's journey). Flag deviations for review.
- **Voice fingerprinting** — define character voice traits as quantifiable metrics (sentence length, vocabulary register, somatic frequency) and check prose compliance automatically.
- **Manuscript versioning** — leverage git's diff capabilities to compare draft-1 vs draft-2 prose at the sentence level. Could surface what changed and why.

### Structural Ideas
- **Ghost beats** — placeholder beat pages that mark structural positions before content is written. Status: `ghost`. Useful during early outlining when you know "something needs to happen here" but not what.
- **Parallel timelines** — the novel may need non-linear timeline support. Current temporal filtering assumes a single linear sequence. Could extend `timeline-event` with `timeline_branch` for parallel storylines.
- **Cross-chapter foreshadowing density** — a lint rule that checks foreshadowing strand "distance" (chapters between planting and resolution). Very long distances may need more reinforcement beats.
- **Character voice drift detection** — compare a character's voice traits in early vs. late chapters. If drift is unintentional, flag it. If intentional (character growth), document it in the arc page.

### Process Ideas
- **Ingest-to-pipeline bridge** — when ingesting a raw source that discusses chapter structure, automatically create stub outline and beat pages from the source content. Currently ingest creates source/entity/concept pages but not pipeline pages.
- **Conflict escalation tracker** — visualize how each conflict's `resolution_status` changes across chapters. Similar to a burndown chart but for narrative tension.
- **Reader surprise metric** — track the gap between what the reader expects (based on foreshadowing) and what actually happens. Large gaps = surprise; small gaps = satisfaction. Could be modeled via dramatic irony tracking.

---

## File Inventory (Created/Modified This Session)

### Created (19 files)
```
Concept.md
handover.md
docs/README.md
docs/wiki-schema.md
docs/navigation-system.md
docs/agent-workflows.md
docs/reader-model.md
docs/dramatica-integration.md
docs/writing-pipeline.md
todo/README.md
todo/meta/README.md
todo/phase-1-schema/README.md
todo/phase-2-navigation/README.md
todo/phase-3-workflows/README.md
todo/phase-4-integration/README.md
todo/phase-5-writing-pipeline/README.md
```

### Modified (2 files)
```
CLAUDE.md    — development roadmap + writing pipeline references
README.md    — full project rewrite
```

---

## Next Session Entry Point

1. Read `todo/README.md` → Phase 1 is the first `not-started` phase
2. Read `todo/meta/README.md` → validation rules, session protocol
3. Read `todo/phase-1-schema/README.md` → 19 tasks starting with directory creation
4. Load `docs/wiki-schema.md` only when tasks reference it
5. Begin with task 1: create wiki directories

The framework is complete. Implementation begins with Phase 1.
