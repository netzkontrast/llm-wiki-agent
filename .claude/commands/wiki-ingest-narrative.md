---
name: wiki-ingest-narrative
description: narrative layer ingest
---

## EXHAUSTIVE EXTRACTION
Extract EVERY named location, character, alter, persona. Never create a 'representative' subset.

## BATCH GUIDANCE
If the plan lists N > 6 entities of the same type, process them 6 at a time. Run this skill repeatedly, advancing through the list, until the plan inventory is exhausted.

## ALTER/PERSONA DETECTION
Named alters in DID character descriptions (e.g., Limina, Echo, Index, Nox) are characters and require their own character pages.

## MERGE MANDATE

When ingesting characters, locations, or concepts that already exist in the wiki, you MUST merge the new information into the existing file (e.g., append new tags, relationships, or traits) instead of overwriting it completely. Never use file overwrites unless explicitly creating a new file.

## Steps
1. Read the compiled context. You receive a pre-compiled context. Do NOT read wiki/index.md yourself.
2. Draft or update the pages specified in the plan for the narrative layer.
3. Validate your output against the Schema Reminder in the compiled context before writing to disk.
4. Run `python3 tools/validate.py --recent-minutes 5`
   - If validation fails, retry up to 3 times to fix the errors.
5. Append new pages to `wiki/index.md` using the required tagged format: `- [Title](path) — description <!-- type:TYPE slug:SLUG -->`. Do NOT add updates to the index.
6. Before finishing, read the plan's entity count for locations and characters and verify the number of files written matches.

Writes: `narrative/characters/`, `narrative/locations/`, `narrative/conflicts/`, `narrative/themes/`, `narrative/arcs/`, `narrative/dramatica/`, `narrative/timeline/`
Merge rule: merge character profiles; never overwrite established traits without contradiction log entry.
