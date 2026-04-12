---
name: wiki-ingest
description: Orchestrates chunk-loop ingest sub-skills. Guarantees complete extraction.
---

## COMPLETENESS MANDATE

ALL entities in a source document MUST be extracted — no deferral, no sampling, no "test runs".
The words "representative sample", "test run", "defer", "skip for now" are FORBIDDEN in plan files.

## Steps

1. **Chunk**: Run `python3 tools/chunk.py raw/{file}` to generate semantic chunks.

2. **Source Initialization**: Create a new source page `wiki/knowledge/sources/{slug}.md` representing the raw file, including a summary and key claims. Append it to `wiki/index.md` using the standard HTML tag format.

3. **Loop Over Chunks**: For each chunk in `chunks/{slug}/`:
   A. **Plan**: Run `python3 tools/compile_context.py --task plan --chunk {chunk_path}`. Then run `/wiki-decompose` to generate `wiki/meta/ingest/{slug}-plan.md`.
   B. **Knowledge Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-knowledge --chunk {chunk_path}`. Call `/wiki-ingest-knowledge`.
   C. **Narrative Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-narrative --chunk {chunk_path}`. Call `/wiki-ingest-narrative`.
   D. **Reader State Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-reader --chunk {chunk_path}`. Call `/wiki-ingest-reader`.

4. **Merge/Dedup Check**: Run `python3 tools/index_manager.py check-duplicate {slug} {type}` on any newly identified complex entities to ensure we haven't created conflicting type representations.

5. **Overview Synthesis**: Read `wiki/overview.md` and the newly created `wiki/knowledge/sources/{slug}.md` page. Update `wiki/overview.md` to reflect any new high-level syntheses or paradigm shifts introduced by the source.

6. **Final Validation**: Run `python3 tools/validate.py --index-only`. If this fails, resolve the structural/index errors before proceeding.

7. **Log**: Append a success entry to `wiki/log.md`.

8. **Cleanup**: Move `raw/{file}` to `processed/{file}`. Remove the `chunks/{slug}/` directory using `rm -rf`.
