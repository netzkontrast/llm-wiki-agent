# Timeline (Research Provenance)

Chronological index of source documents — when each source was written, published, and
ingested. Used to track the real-world provenance of knowledge claims.

> **Two timelines:** This directory tracks *real-world* dates (source chronology, ingest
> history). Story-world chronology (boundary events, `is_boundary`, `sequence_number`)
> lives in `wiki/narrative/timeline/`.

## Pages

*(none yet — populated during Phase 6 ingest tooling)*

## Connections
- Related to: `wiki/knowledge/sources/` — each source page may reference its timeline entry
- Related to: `wiki/meta/ingest/` — session logs record when each file was ingested

## Routing Layer
Part of the **Knowledge Layer** — see [`wiki/knowledge/README.md`](../README.md) for loading rules and mutation constraints.

## Conventions
- Naming: `YYYY-MM-DD-source-slug.md` or by ingestion sequence
- Temporal: These pages ARE the real-world temporal index — they don't use `valid_from`/`valid_until`
