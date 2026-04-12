---
name: wiki-ingest-reader
description: reader_state layer ingest
---

## Steps
1. Read the compiled context. You receive a pre-compiled context. Do NOT read wiki/index.md yourself.
2. Draft or update the pages specified in the plan for the reader_state layer.
3. Validate your output against the Schema Reminder in the compiled context before writing to disk. Focus especially on the terminology_permitted monotonic accumulation rule.
4. Run `python3 tools/validate.py --recent-minutes 5`
   - If validation fails, retry up to 3 times to fix the errors.
5. Append new pages to `wiki/index.md` using the required tagged format: `- [Title](path) — description <!-- type:TYPE slug:SLUG -->`. Do NOT add updates to the index.

Writes: `reader_state/reader-model/`, `reader_state/foreshadowing/`
Merge rule: terminology_permitted is a one-way ratchet. Never remove previously permitted terminology.
