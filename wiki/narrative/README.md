# Narrative Layer — Mutable Story Structure

This layer contains all plot states mutated by the writing process. Every change
in the narrative arc is recorded here — not in the Knowledge layer.

**All page content lives as subdirectories here (not at wiki root):**

| Dir | Type | What it contains |
|---|---|---|
| `characters/` | character | Fictional character profiles, psychology, voice |
| `chapters/` | chapter | Chapter specs (POV, timeline, constraints, refs) |
| `locations/` | location | World-building settings and psychological mappings |
| `conflicts/` | conflict | Internal, external and thematic conflicts |
| `themes/` | theme | Thematic threads and motifs |
| `arcs/` | arc | Character and plot transformation arcs |
| `dramatica/` | dramatica | Dramatica Theory story points and throughlines |
| `timeline/` | timeline-event | Story-world chronology — boundary events, sequence numbers |
| `beats/` | beat | Atomic scene moments with tension and foreshadowing actions |
| `outlines/` | outline | Chapter structural planning (beat sequences) |
| `manuscripts/` | manuscript | Written prose drafts |

> **Two timelines:** This `timeline/` tracks *story-world* events (`is_boundary`,
> `sequence_number`). Real-world source provenance lives in `wiki/knowledge/timeline/`.

## Mutation rule
Mutates through writing processes. Each beat potentially creates a delta. Changes
propagate via `informs:` chains to dependent pages. Always update `last_updated`
after changes.

## When to load
- During `wiki-ingest-narrative` sub-skill
- During chapter-writing, conflict-resolution, arc-tracking workflows
- qmd collection: `narrative` — `qmd search "term" -c narrative`
