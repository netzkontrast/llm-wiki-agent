# LLM Wiki Agent — Schema & Workflow Instructions

This wiki is maintained entirely by Claude Code. No API key or Python scripts needed — just open this repo in Claude Code and talk to it.

## Slash Commands (Claude Code)

| Command | What to say |
|---|---|
| `/wiki-ingest` | `ingest raw/my-article.md` |
| `/wiki-query` | `query: what are the main themes?` |
| `/wiki-lint` | `lint the wiki` |
| `/wiki-graph` | `build the knowledge graph` |
| `/wiki-chapter` | `write chapter 5` |
| `/wiki-character` | `develop character Kael` |
| `/wiki-worldbuild` | `build world element LogosPrime` |
| `/wiki-timeline` | `timeline of fragmentation` |
| `/wiki-conflict` | `resolve conflict KaelVsAegis` |
| `/wiki-reader-model` | `reader state for chapter 1` |
| `/wiki-revise` | `revise chapter 1` |
| `/wiki-lector` | `lector chapter 1` |
| `/wiki-brainstorm` | `brainstorm about The Cage Motif` |

Or just describe what you want in plain English:
- *"Ingest this file: raw/papers/attention-is-all-you-need.md"*
- *"What does the wiki say about transformer models?"*
- *"Check the wiki for orphan pages and contradictions"*
- *"Build the graph and show me what's connected to RAG"*

Claude Code reads this file automatically and follows the workflows below.

---

## Directory Layout

```
raw/          # Immutable source documents — waiting for ingestion
processed/    # Source documents that have been ingested — moved from raw/
wiki/         # Claude owns this layer entirely
  index.md    # Global catalog — all page types, all layers
  log.md      # Append-only chronological record
  overview.md # Living synthesis across all sources
  knowledge/  # Layer 1: static facts (source-derived, author-defined)
    sources/      # One summary page per source document
    entities/     # Real-world people, companies, projects
    concepts/     # Ideas, frameworks, methods, theories
    rules/        # World-rules and narrative-rules (authorial canon)
    timeline/     # Research provenance — source dates, real-world chronology
    syntheses/    # Saved query answers
  narrative/  # Layer 2: mutable story structure
    characters/   # Fictional character profiles
    chapters/     # Chapter specs (POV, timeline, constraints)
    locations/    # World-building settings
    conflicts/    # Conflict tracking
    themes/       # Thematic threads and motifs
    arcs/         # Character and plot transformation arcs
    dramatica/    # Dramatica Theory story points
    timeline/     # Story-world chronology (boundary events, sequence numbers)
    beats/        # Atomic scene moments
    outlines/     # Chapter structural planning
    manuscripts/  # Written prose drafts
  reader_state/ # Layer 3: monotonically accumulating reader knowledge
    reader-model/   # Per-chapter reader knowledge states
    foreshadowing/  # Foreshadowing strands (planted → resolved)
  meta/       # Layer 4: system administration
    archive/    # Deprecated pages (never delete)
    ingest/     # Session plans and logs (adaptive ingest)
    contradiction-log.md
    <protocol docs>
log/          # Agent session logs (branch-scoped, Phase 6)
graph/        # Auto-generated graph data
tools/        # Python scripts (require qmd + ANTHROPIC_API_KEY)
```

---

## When Using the Wiki

## Ingestion Queue

The ingestion queue is managed by file location, not by checklist:

- `raw/` — files waiting to be ingested (queue)
- `processed/` — files that have been successfully ingested (done)

**After every successful ingest**, move the source file:
```bash
mv raw/<filename> processed/<filename>
```

To see what's left to ingest:
```bash
ls raw/*.md | wc -l    # count remaining
ls raw/*.md             # list remaining
```

To see what's been processed:
```bash
ls processed/*.md | wc -l
```

---

## Page Format

Every wiki page uses this frontmatter:

```yaml
---
title: "Page Title"
type: source | entity | concept | synthesis | character | chapter | location | conflict | theme | timeline-event | rule | arc | dramatica | reader-state | foreshadowing
tags: []
sources: []       # list of source slugs that inform this page
requires: []      # list of page slugs this page depends on (depth 2)
informs: []       # list of page slugs this page informs (unbounded)
valid_from: ""    # timeline-event slug
valid_until: ""   # timeline-event slug
traits: {}        # specialized key-value pairs (e.g. voice_profile)
last_updated: YYYY-MM-DD
---
```

Use `[[PageName]]` wikilinks to link to other wiki pages.

---

## Ingest Workflow

Triggered by: *"ingest <file>"* or `/wiki-ingest`

Steps (in order):
1. Read the source document fully using the Read tool
2. Read `wiki/index.md` and `wiki/overview.md` for current wiki context
3. Write `wiki/sources/<slug>.md` — use the source page format below
4. Update `wiki/index.md` — add entry under Sources section
5. Update `wiki/overview.md` — revise synthesis if warranted
6. Update/create entity pages for key people, companies, projects mentioned
7. Update/create concept pages for key ideas and frameworks discussed
8. Flag any contradictions with existing wiki content
9. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Title>`
10. Create/update **character pages** for fictional characters mentioned in the source
11. Create/update **location pages** for settings described
12. Create/update **conflict pages** for conflicts identified
13. Create/update **theme pages** for thematic elements discussed
14. Create/update **rule pages** if the source defines world rules or narrative mandates
15. Link source page to relevant **chapter pages** if chapter-specific content
16. Update **timeline events** if the source establishes chronological facts
17. Create/update **foreshadowing pages** if the source discusses foreshadowing strands
18. Move the source file from `raw/` to `processed/`: `mv raw/<filename> processed/<filename>`

### Source Page Format

```markdown
---
title: "Source Title"
type: source
tags: []
date: YYYY-MM-DD
source_file: raw/...
---

## Summary
2–4 sentence summary.

## Key Claims
- Claim 1
- Claim 2

## Key Quotes
> "Quote here" — context

## Connections
- [[EntityName]] — how they relate
- [[ConceptName]] — how it connects

## Contradictions
- Contradicts [[OtherPage]] on: ...
```

---

## Query Workflow

Triggered by: *"query: <question>"* or `/wiki-query`

Steps:
1. Read `wiki/index.md` to identify relevant pages
2. Read those pages with the Read tool
3. Synthesize an answer with inline citations as `[[PageName]]` wikilinks
4. Ask the user if they want the answer filed as `wiki/syntheses/<slug>.md`

---

## Lint Workflow

Triggered by: *"lint the wiki"* or `/wiki-lint`

Use Grep and Read tools to check for:
- **Orphan pages** — wiki pages with no inbound `[[links]]` from other pages
- **Broken links** — `[[WikiLinks]]` pointing to pages that don't exist
- **Contradictions** — claims that conflict across pages
- **Stale summaries** — pages not updated after newer sources
- **Missing entity pages** — entities mentioned in 3+ pages but lacking their own page
- **Data gaps** — questions the wiki can't answer; suggest new sources
- **Novel-specific checks** — orphan characters, timeline gaps, foreshadowing with no resolution, `constraint_refs` to non-existent rules, `terminology_permitted` ratchet violations.

Output a lint report and ask if the user wants it saved to `wiki/lint-report.md`.

---

## Graph Workflow

Triggered by: *"build the knowledge graph"* or `/wiki-graph`

When the user asks to build the graph, run `tools/build_graph.py` which:
- Pass 1: Parses all `[[wikilinks]]` and `requires:`/`informs:` relationships → deterministic `EXTRACTED` edges
- Pass 2: Infers implicit relationships → `INFERRED` edges with confidence scores
- Runs Louvain community detection
- Outputs `graph/graph.json` + `graph/graph.html`

If the user doesn't have Python/dependencies set up, instead generate the graph data manually:
1. Use Grep to find all `[[wikilinks]]` across wiki pages
2. Build a node/edge list
3. Write `graph/graph.json` directly
4. Write `graph/graph.html` using the vis.js template

---

## Naming Conventions

- Source slugs: `kebab-case` matching source filename
- Entity pages: `TitleCase.md` (e.g. `OpenAI.md`, `SamAltman.md`)
- Concept pages: `TitleCase.md` (e.g. `ReinforcementLearning.md`, `RAG.md`)
- Character pages: `TitleCase.md`
- Chapter pages: `chapter-NN.md`
- Location pages: `TitleCase.md`
- Conflict pages: `TitleCase.md`
- Theme pages: `TitleCase.md`
- Timeline events: `NNN-slug.md`
- Rule pages: `TitleCase.md`
- Arc pages: `kebab-case.md`
- Dramatica pages: `TitleCase.md`
- Reader-state pages: `chapter-NN-state.md`
- Foreshadowing pages: `kebab-case.md`
- Outline pages: `chapter-NN-outline.md`
- Beat pages: `chapter-NN-beat-NN.md`
- Manuscript pages: `chapter-NN-manuscript.md`

## Index Format

```markdown
# Wiki Index

## Overview
- [Overview](overview.md) — living synthesis

## Sources
- [Source Title](sources/slug.md) — one-line summary

## Entities
- [Entity Name](entities/EntityName.md) — one-line description

## Concepts
- [Concept Name](concepts/ConceptName.md) — one-line description

## Syntheses
- [Analysis Title](syntheses/slug.md) — what question it answers

## Characters
- [Name](characters/Name.md) — role, brief

## Chapters
- [Chapter N: Title](chapters/chapter-NN.md) — pov, outline_status/manuscript_status

## Locations
- [Name](locations/Name.md) — world, brief

## Conflicts
- [Name](conflicts/Name.md) — type, status

## Themes
- [Name](themes/Name.md) — brief statement

## Timeline
- [NNN Event](timeline/NNN-slug.md) — timepoint

## Rules
- [Name](rules/Name.md) — class, brief

## Arcs
- [Name](arcs/slug.md) — type, subject

## Dramatica
- [Name](dramatica/Name.md) — element_type

## Reader Model
- [Chapter N](reader-model/chapter-NN-state.md) — tension_level

## Foreshadowing
- [Name](foreshadowing/slug.md) — status

## Outlines
- [Chapter N](outlines/chapter-NN-outline.md) — outline_status

## Beats
- [Chapter N, Beat M](beats/chapter-NN-beat-NN.md) — purpose

## Manuscripts
- [Chapter N](manuscripts/chapter-NN-manuscript.md) — manuscript_status
```

## Log Format

Each entry starts with `## [YYYY-MM-DD] <operation> | <title>` so it's grep-parseable:

```
grep "^## \[" wiki/log.md | tail -10
```

Operations: `ingest`, `query`, `lint`, `graph`

---

## When Developing the Wiki System

## Development Roadmap (todo/)

The wiki is being extended for novel-author use. Detailed specs live in `docs/`, phased implementation plan in `todo/`.

See `Concept.md` for the overall vision and architecture overview. See `handover.md` for open questions and ideas.

### Reference Specs

| Spec | Contents |
|------|----------|
| `docs/wiki-schema.md` | 14 page types, frontmatter, templates, traits, temporal fields |
| `docs/navigation-system.md` | `requires:/informs:` dependency, temporal filtering, context ceilings |
| `docs/agent-workflows.md` | 12 workflows: 8 core + 4 writing pipeline |
| `docs/reader-model.md` | Reader progressive disclosure, terminology ratchet, foreshadowing |
| `docs/dramatica-integration.md` | Dramatica Theory mapping to wiki pages |
| `docs/writing-pipeline.md` | Beats, outlines, manuscripts — the 4-stage writing pipeline |

### Writing Pipeline

The writing pipeline separates chapter specs from structural planning and prose:

```
Chapter (spec) → Outline (structure) → Beats (atomic scenes) → Manuscript (prose)
```

Four dedicated workflows: `outline-writing`, `beat-detailing`, `manuscript-drafting`, `manuscript-revision`. The `chapter-writing` workflow orchestrates by delegating to the right stage.

### Session Start Protocol (MANDATORY)

Every session that touches wiki structure or implementation:
1. Read `todo/README.md` — find the active phase (first phase with status != `complete`)
2. Read `todo/meta/README.md` — validation rules, contradiction hierarchy, wiki hygiene
3. Read the active phase's `README.md` in `todo/phase-N-*/`
4. Continue from the first unchecked task in that phase

### Rules
- Mark tasks `- [x]` immediately after completing them
- Update phase status when all tasks in a phase complete
- Load `docs/` specs ONLY when the active task references them
- NEVER read inactive phase folders (status `not-started` or `complete`)
- Flag contradictions — never silently resolve them (log to `wiki/meta/contradiction-log.md`)
- Archive deprecated content to `wiki/archive/` — never delete wiki pages
- Follow contradiction hierarchy: `rule > source > character > chapter > synthesis`
- **Every `wiki/` subfolder MUST have a `README.md`** with navigational info — update it whenever pages are added, removed, or archived (see `todo/meta/README.md` for template)

## Developer Enhancements
See `docs/jules/dev-process.md` for future proposals on splitting Wiki Operations from System Development to improve token efficiency.
