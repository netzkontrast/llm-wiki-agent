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

### Commit 4: Implement Phase 3 (this session)
Implemented Phase 3: Agent Workflows & Slash Commands:
- Created 9 slash commands in `.claude/commands/`: `wiki-chapter`, `wiki-character`, `wiki-worldbuild`, `wiki-timeline`, `wiki-conflict`, `wiki-reader-model`, `wiki-revise`, `wiki-lector`, `wiki-brainstorm`.
- Updated `wiki-ingest.md` with extended ingest steps (10-17).
- Formalized `discovery-protocol.md` and `validation-protocol.md` hooks in `wiki/meta/`.
- Established the `SKILL.md` standard with an example in `.claude/commands/wiki-ingest/`.
- Updated tracking files in `todo/`.

---

## Reflections & Learnings (Meta-Analysis)

During this session, I navigated the workflow implementations and realized several key insights about the architecture, token efficiency, and how the repository could be optimized for LLM use:

### Token Efficiency and Workflow Context Load
- **The Context Dilution Problem:** While working on Phase 3, I had to load `docs/agent-workflows.md` and `todo/phase-3-workflows/README.md`. These files are comprehensive, but reading them fully to extract specific, isolated details (like the exact trigger words for one command) is token-inefficient.
- **Progressive Disclosure in Practice:** The principle of progressive disclosure is excellent in theory but needs stricter enforcement in the agent instruction files (`CLAUDE.md` and `GEMINI.md`). Currently, both files contain a mix of system overview, standard workflows, and development roadmap tasks. When I am just trying to ingest a file, I don't need to know about the Phase 5 writing pipeline tasks.

### Structuring Agent Instructions
- **Splitting Responsibilities:** The current instructions mix "How to use the wiki" (the core product) with "How to develop the wiki system itself" (the meta-product).
- **Proposal:** We should separate these into distinct instruction contexts. An agent acting as a "Writer/Researcher" should only load the operational instructions (ingest, query, chapter writing). An agent acting as a "System Developer" should load the schema, protocols, and todo tasks.

---

## Future Enhancements: Agent Orchestration & Process Separation

I have documented a formal proposal for improving the agent operational guidelines and separating the writing vs. development contexts.

See the new specification: **`docs/jules/dev-process.md`** (linked in `CLAUDE.md` and `GEMINI.md`).

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

## Open Ideas for Future Development

Ideas that could be valuable but are not yet designed or scheduled. Each describes a problem and a potential approach.

### Page Split Management

**Problem:** Pages grow over time — during ingestion, novel writing, and decision-making. A character page that starts at 40 lines might reach 300 lines after 20 chapters of development. A concept page might accumulate content from dozens of source ingestions. Long pages degrade context-window efficiency and make it harder for agents to find the right information.

**Potential approach — Automated split triggers:**
- **Length-based:** When a page exceeds a configurable threshold (e.g., 200 lines), the agent should evaluate whether the page can be split by topic, by temporal period, or by section. The split produces two or more pages with clear `requires:`/`informs:` links between them. The original page becomes either a hub (linking to sub-pages) or is archived with a redirect.
- **Temporal splits:** Characters, locations, and conflicts that evolve significantly across the novel's timeline can be split into temporal versions: `Kael.md` (early), `Kael-post-frag.md` (mid), `Kael-integrated.md` (late). Each version has `valid_from`/`valid_until` windows. The temporal filtering system already supports this — it just needs a trigger mechanism to prompt the split.
- **Complexity-based:** When a page covers 2+ distinct topics (detected by section count, heading density, or thematic divergence), it should be flagged for topic-based splitting. Example: a concept page on "Paraconsistent Logic" that also covers its narrative application should split into a pure concept page and a synthesis page.
- **Split protocol:** Every split should (1) create the new pages, (2) update all `[[wikilinks]]` pointing to the original, (3) update folder READMEs, (4) update `wiki/index.md`, (5) archive the original if fully replaced. The `informs:` chain handles downstream propagation.

### Context-Window Budget Tracking

**Problem:** Even with context ceilings and priority-drop rules, there's no feedback loop telling the agent "you're loading too much." If the wiki grows to 500+ pages with dense cross-references, the navigation system might routinely hit ceilings and drop useful pages.

**Potential approach:** Track a per-session "context budget" — the total token count of all wiki pages loaded. Each workflow's ceiling could be expressed in approximate tokens rather than page count (since pages vary in length). The agent would report its budget usage ("loaded 12,000 / 20,000 tokens for this workflow") and the user could adjust ceilings. Long-term, the agent could learn which pages are most frequently dropped and suggest structural changes to reduce context pressure.

### Refactoring Sessions

**Problem:** Organic wiki growth creates structural debt — pages that should be merged, split, or reorganized. Currently, the lint workflow catches some issues (orphans, broken links), but there's no dedicated "refactoring" workflow.

**Potential approach:** A `wiki-refactor` workflow that:
1. Scans for pages exceeding the line threshold
2. Identifies pages with high `informs:` fan-out (potential for split)
3. Finds near-duplicate pages (similar titles, overlapping content)
4. Detects concept pages that have outgrown their original scope
5. Proposes a refactoring plan (splits, merges, renames, archive) and asks the user for approval before executing

This could run as a periodic maintenance pass (e.g., every 10 ingestions, or after each phase completion).

### Progressive Wiki Indexing

**Problem:** `wiki/index.md` is a flat list. With 500+ pages across 18 types, scrolling through the index to find the right page is slow. Folder READMEs help, but the top-level index becomes unwieldy.

**Potential approach:** Tiered indexing — the main `index.md` shows only section headers with page counts. Each section links to its folder's `README.md` for the detailed listing. Agents read the main index first (fast, small), then drill into the relevant folder README only when needed. This mirrors the progressive disclosure philosophy already used for `docs/` and `todo/`.

### Ingest-Time Wiki Health Scoring

**Problem:** Each ingestion adds pages but may also introduce inconsistencies, increase page lengths, or create orphan content. Currently, the user must manually run `wiki-lint` to discover issues.

**Potential approach:** Add a lightweight health check at the end of every ingest workflow:
- Count pages over line threshold (flag for split)
- Check for new orphan pages (pages created with no inbound links)
- Check `informs:` staleness on pages touched during ingest
- Output a 1-line health summary: "Wiki health: 3 pages need splitting, 1 orphan, 0 stale targets"
- If health score drops below threshold, suggest running `wiki-lint` or `wiki-refactor`

### Semantic Deduplication

**Problem:** Multiple source documents may describe the same concept in different terminology (especially with German/English mixing). Two concept pages might exist for what is essentially the same idea.

**Potential approach:** During ingestion, before creating a new concept or entity page, the agent should search existing pages for semantic overlap — not just exact title matches. If a candidate match is found, the agent asks: "This looks related to [[ExistingPage]] — merge, link, or create separately?" This prevents the wiki from fragmenting knowledge across near-duplicate pages.

### Chapter Dependency Graphs

**Problem:** Chapters don't exist in isolation — chapter 15 might depend on revelations from chapters 3, 8, and 12. Currently, this is tracked via `requires:` and `informs:`, but there's no visualization of chapter-to-chapter dependencies.

**Potential approach:** A specialized graph view (separate from the main knowledge graph) that shows only chapter nodes with edges representing:
- Foreshadowing strands (planted in X, resolved in Y)
- Character arc stage transitions
- Timeline causality
- Reader knowledge prerequisites

This would help identify structural issues like circular dependencies, isolated chapters, or overly dependent clusters.

---

## File Inventory (Created/Modified This Session)

### Created (12 files)
```
.claude/commands/wiki-chapter.md
.claude/commands/wiki-character.md
.claude/commands/wiki-worldbuild.md
.claude/commands/wiki-timeline.md
.claude/commands/wiki-conflict.md
.claude/commands/wiki-reader-model.md
.claude/commands/wiki-revise.md
.claude/commands/wiki-lector.md
.claude/commands/wiki-brainstorm.md
.claude/commands/wiki-ingest/SKILL.md
wiki/meta/discovery-protocol.md
wiki/meta/validation-protocol.md
docs/jules/dev-process.md
docs/jules/README.md
```

### Modified (6 files)
```
CLAUDE.md    — appended reference to dev-process.md
GEMINI.md    — appended reference to dev-process.md
todo/phase-3-workflows/README.md — marked complete
todo/README.md — updated phase statuses
todo/meta/README.md — added SKILL.md standard
.claude/commands/wiki-ingest.md — added extended steps
handover.md — added Commit 4 and meta-reflections
```

---

## Next Session Entry Point

1. Read `todo/README.md` → Phase 4 is the active phase.
2. Read `todo/meta/README.md` → validation rules, session protocol
3. Read `todo/phase-4-integration/README.md`
4. Load `docs/` specs ONLY when tasks reference it
5. Begin with task 1 in Phase 4.
