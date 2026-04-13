---
name: wiki-ingest
description: Orchestrates chunk-loop ingest sub-skills. Guarantees complete extraction.
---

## COMPLETENESS MANDATE

ALL entities in a source document MUST be extracted — no deferral, no sampling, no "test runs".
The words "representative sample", "test run", "defer", "skip for now" are FORBIDDEN in plan files.

## MERGE MANDATE & AUTOMATION (DOs and DONTs)

When ingesting characters, locations, or concepts that already exist in the wiki, you MUST merge the new information into the existing file instead of overwriting it completely. Never use file overwrites unless explicitly creating a new file.

**DOs:**
- Perform **Semantic Synthesis**: When updating the body of an existing file (e.g., the `## Description`), you must rewrite the section to smoothly and logically integrate the new facts.
- Safely update YAML frontmatter: Merge arrays (like `tags`, `sources`, `related_entities`) by appending new unique items to the existing lists.
- Write Python scripts to safely parse existing YAML and markdown body, synthesize the text, and write it back.

**DONTs:**
- Do NOT naively append `## Update [Date]` blocks to the end of the file. This leads to fragmentation and readability issues.
- Do NOT delete or omit previously established facts when synthesizing the new description.

## LANGUAGE RULES
All generated wiki content (summaries, concept names, entity names, syntheses) MUST be written entirely in English, regardless of the raw source file's language. However, source page slugs must remain the kebab-case version of the original raw filename to maintain a direct mapping.

## RELATIONSHIPS & CONTRADICTIONS
Ensure all sub-skills capture relationships in the YAML frontmatter (`relationships` or `related_entities`) and inline wiki-links.
Ensure any contradictions are formally logged to `wiki/meta/ingest/registers/contradictions.md`.

## Steps

1. **Chunk**: Run `python3 tools/chunk.py raw/{file}` to generate semantic chunks.

2. **Loop Over Chunks**: For each chunk in `chunks/{slug}/`:
   A. **Plan**: Run `python3 tools/compile_context.py --task plan --chunk {chunk_path}`. Then run `/wiki-decompose` to generate `wiki/meta/ingest/{slug}-plan.md`.
   B. **Knowledge Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-knowledge --chunk {chunk_path}`. Call `/wiki-ingest-knowledge`.
   C. **Narrative Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-narrative --chunk {chunk_path}`. Call `/wiki-ingest-narrative`.
   D. **Reader State Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-reader --chunk {chunk_path}`. Call `/wiki-ingest-reader`.

3. **Merge/Dedup Check**: Run `python3 tools/index_manager.py check-duplicate {slug} {type}` on any newly identified complex entities to ensure we haven't created conflicting type representations.

4. **Final Validation**: Run `python3 tools/validate.py --index-only`. If this fails, resolve the structural/index errors before proceeding.

5. **Log**: Append a success entry to `wiki/log.md`.

6. **Cleanup**: Move `raw/{file}` to `processed/{file}`. Remove the `chunks/{slug}/` directory using `rm -rf`.
