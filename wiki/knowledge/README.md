# Knowledge Layer — Static Canon

This layer contains immutable world knowledge. Information here changes only when
the author introduces new definitions — never through the narrative process itself.

**All page content lives as subdirectories here (not at wiki root):**

| Dir | Type | What it contains |
|---|---|---|
| `sources/` | source | One summary page per ingested raw document |
| `entities/` | entity | Real-world people, organisations, projects |
| `concepts/` | concept | Ideas, frameworks, methods, theories |
| `rules/` | rule | World-rules and narrative-rules (authorial canon) |
| `timeline/` | timeline-event | Research provenance — source dates, ingestion order, real-world chronology |
| `syntheses/` | synthesis | Saved query answers and derived knowledge |

> **Two timelines:** This `timeline/` tracks *real-world* dates (when a source was
> written, when it was ingested). Story-world chronology lives in
> `wiki/narrative/timeline/`.

## Mutation rule
**NEVER** overwrite via agentic writing processes. When chapter-writing generates
a character development, the delta goes to `wiki/narrative/` — not here.

## When to load
- Before any write process as read-only context (Discovery Hook)
- During `wiki-ingest-knowledge` sub-skill
- During world-building and rule-definition workflows
- qmd collection: `knowledge` — `qmd search "term" -c knowledge`
