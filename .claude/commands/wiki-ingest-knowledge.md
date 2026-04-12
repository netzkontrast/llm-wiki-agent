---
name: wiki-ingest-knowledge
description: knowledge layer ingest
---

## EXHAUSTIVE EXTRACTION
Extract EVERY entity (persons, systems, organizations), concept, rule. No entity may be deferred.
Create entity pages in `knowledge/entities/` for ALL named persons, AI systems, organizations, or world-structural systems encountered — not just prominent ones.

## MERGE MANDATE

When ingesting characters, locations, or concepts that already exist in the wiki, you MUST merge the new information into the existing file (e.g., append new tags, relationships, or traits) instead of overwriting it completely. Never use file overwrites unless explicitly creating a new file.

## Steps
1. Read the compiled context. You receive a pre-compiled context. Do NOT read wiki/index.md yourself.
2. Draft or update the pages specified in the plan for the knowledge layer.
3. Validate your output against the Schema Reminder in the compiled context before writing to disk.
4. Run `python3 tools/validate.py --recent-minutes 5`
   - If validation fails, retry up to 3 times to fix the errors.
5. Append new pages to `wiki/index.md` using the required tagged format: `- [Title](path) — description <!-- type:TYPE slug:SLUG -->`. Do NOT add updates to the index.

Writes: `knowledge/sources/`, `knowledge/entities/`, `knowledge/concepts/`, `knowledge/rules/`, `knowledge/timeline/`, `knowledge/syntheses/`
Merge rule: always update `sources:` field; never overwrite established content without contradiction log entry, only append new facts.
