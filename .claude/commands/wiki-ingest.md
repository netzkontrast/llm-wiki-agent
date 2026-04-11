---
name: wiki-ingest
description: Orchestrates ingest sub-skills. Guarantees complete extraction.
---

## COMPLETENESS MANDATE

ALL entities in a source document MUST be extracted — no deferral, no sampling, no "test runs".
If a source file contains 31 locations, create 31 location pages.
The words "representative sample", "test run", "defer", "skip for now" are FORBIDDEN in plan files.

## Steps

1. **Decompose**: Run `/wiki-decompose {file}`. Read the FULL output including all counts from `log/{branch}/{session}/plan.md`. If TOTAL entities > 10, note batch mode required.

2. **Determine layers** from the generated plan.

3. **Knowledge layer** (if touched): Call `/wiki-ingest-knowledge` with FULL entity list from plan.
   - For entity types with N > 10: call in batches of 6, iterating until all extracted.

4. **Narrative layer** (if touched): Call `/wiki-ingest-narrative` with FULL entity list from plan.
   - For entity types with N > 10: call in batches of 6, iterating until all extracted.
   - LOOP until decompose inventory is exhausted.

5. **Reader state layer** (if touched): Call `/wiki-ingest-reader`.

6. **Audit**: Run `python3 tools/audit_completeness.py log/{branch}/{session}/plan.md`.
   - If `total_missing > 0`: run cleanup passes for each missing type, then re-audit.
   - Do NOT move file to `processed/` until audit passes with `total_missing == 0`.

7. **Index + Log**: Update `wiki/index.md` (all sections). Append `wiki/log.md`.

8. **Move**: `mv raw/{file} processed/{file}` — only after audit confirms completeness.
