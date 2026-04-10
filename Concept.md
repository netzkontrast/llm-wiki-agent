# Novel-Author Wiki Extension — Concept

## What

An extension to the LLM Wiki Agent that transforms it from a generic knowledge wiki into a specialized tool for novel authors working on structurally complex hard sci-fi. The extension adds 11 new page types, a navigation & dependency system, temporal filtering, 8 novel-specific agent workflows, and progressive disclosure management — both for the author's context window and for the reader's experience.

## Why

The original wiki has 4 page types (`source`, `entity`, `concept`, `synthesis`) optimized for knowledge management. A complex novel also needs to track characters with psychological profiles, chapters with POV and pacing, locations with symbolic meaning, conflicts that may be self-referential paradoxes, themes evolving across 39 chapters, a precise timeline, hard sci-fi rules, narrative arcs, Dramatica theory elements, and what the reader knows at every point.

Without structure, this information either drowns the agent's context window or gets lost between sessions.

## Type Coexistence

The original 4 types remain unchanged and serve as the **generic knowledge layer**. The 11 new types extend the wiki for **novel-specific use**. A `source` page might feed into a `character` or `rule` page via `sources:`. No existing type is replaced.

## How It Works

### Dependency-Driven Navigation
Every wiki page declares `requires:` (what to load for context) and `informs:` (what to update after changes). Reading uses bounded traversal (max-depth 2, workflow-specific context ceilings) to protect the context window. Writing uses **unbounded propagation** — when a page changes, the agent follows the full `informs:` chain until every downstream page is updated or confirmed current. This asymmetry guarantees the wiki is always consistent after every operation while keeping context loads manageable.

### Temporal Filtering
Pages can have `valid_from`/`valid_until` fields referencing timeline events. An agent writing chapter 15 automatically loads only the character states, conflicts, and world-rules that are true at that point in the story — not the entire novel's worth of evolution.

### Reader Progressive Disclosure
A parallel tracking system models what the *reader* knows at each chapter: `terminology_permitted` (one-way ratchet), foreshadowing strands (planted → reinforced → resolved), dramatic irony gaps, and tension curves. This prevents the agent from using concepts the reader hasn't encountered yet.

### Writing Pipeline
A four-stage pipeline separates structural planning from prose writing: **chapter spec** (metadata hub) → **outline** (beat sequence and pacing) → **beats** (atomic scene moments with characters, tension, foreshadowing) → **manuscript** (actual written prose). Each stage has its own status lifecycle and four dedicated workflows (outline-writing, beat-detailing, manuscript-drafting, manuscript-revision). The chapter-writing workflow orchestrates by delegating to the right stage.

### Generic Extension Points
Every page type includes a `traits:` open key-value map for project-specific metadata the generic schema can't anticipate. Recommended keys per type provide a shared vocabulary without constraining the map.

## Architecture

```
Concept.md          ← you are here
docs/               ← detailed reference specifications
  wiki-schema.md       11 page types, frontmatter, templates, traits, naming
  navigation-system.md dependency system, traversal rules, temporal filtering, ceilings
  agent-workflows.md   12 workflows with triggers, context loads, validation
  writing-pipeline.md  beats, outlines, manuscripts — the 4-stage writing pipeline
  reader-model.md      reader progressive disclosure, terminology ratchet, foreshadowing
  dramatica-integration.md Dramatica Theory mapping
todo/               ← implementation phases with progress tracking
  README.md            phase status table, session-start protocol, universal rules
  meta/README.md       validation rules, contradiction hierarchy, wiki hygiene
  phase-1-schema/      page types, directories, seed templates
  phase-2-navigation/  dependency system, temporal filtering, context protocols
  phase-3-workflows/   agent workflows, slash commands
  phase-4-integration/ CLAUDE.md rewrite, tool updates, migration
  phase-5-writing-pipeline/ beats, outlines, manuscripts, 4 new workflows
```

## New Page Types

| Type | Purpose |
|------|---------|
| `character` | Profiles, arcs, psychological maps, alter system tracking, voice |
| `chapter` | POV, timeline, draft status, scene beats, constraints, reader-load cap |
| `location` | World-building, environmental storytelling, symbolic mapping |
| `conflict` | Internal/external/thematic/structural, self-referential paradoxes |
| `theme` | Thematic threads, motifs, dialectical pairs, chapter tracking |
| `timeline-event` | Chronological anchors, causality chains, boundary markers |
| `rule` | World rules, narrative mandates, structural constraints |
| `arc` | Character/plot/thematic transformation tracking with stages |
| `dramatica` | Throughlines, signposts, story points, genre mechanics |
| `reader-state` | Per-chapter reader knowledge, foreshadowing, tension, terminology |
| `foreshadowing` | Cross-cutting strands: planted → reinforced → resolved |
| `beat` | Atomic scene moments: characters, tension, foreshadowing per beat |
| `outline` | Chapter structural plan: ordered beat sequence, pacing notes |
| `manuscript` | Actual written prose with revision tracking |

## Getting Started

1. Read `todo/README.md` for the implementation roadmap
2. Read `todo/meta/README.md` for validation rules and wiki hygiene
3. Read the active phase's README for current tasks
4. Load `docs/` specs only when a task references them
