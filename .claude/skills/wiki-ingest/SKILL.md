---
name: wiki-ingest
description: Extracts factual data from raw source documents, generates immutable L0 factual nodes, and synthesizes L2 wiki concept pages using the chunking loop. Use when the user requests to ingest a document, process a new file in the raw directory, or update the knowledge base with a new source file. Use when handling PDFs, text files, or markdown sources.
---

# wiki-ingest

Use this workflow to process new source material into the layered memory structure.

## COMPLETENESS MANDATE

ALL entities in a source document MUST be extracted — no deferral, no sampling, no "test runs".
The words "representative sample", "test run", "defer", "skip for now" are FORBIDDEN in plan files.

## MERGE MANDATE & AUTOMATION (DOs and DONTs)

When ingesting characters, locations, or concepts that already exist in the wiki, you MUST merge the new information into the existing file instead of overwriting it completely. Never use file overwrites unless explicitly creating a new file.

**DOs:**
- Always check if an entity page exists using `grep` or `ls` before writing.
- Perform **Semantic Synthesis**: When updating the body of an existing file (e.g., the `## Description`), read the existing file completely. Identify where the new information fits, rewrite that section logically, and write back the entire updated file.
- **Safely update YAML frontmatter arrays**: When updating `tags`, `sources`, `related_entities`, or `relationships` on existing pages, parse the existing array, add your new items uniquely, and write the array back. Do NOT overwrite the entire list with only your new items.
- Write a short python script in your step to safely parse, append, and rewrite the file if needed.

**DONTs:**
- Do NOT naively append `## Update [Date]` blocks to the end of the file. This leads to fragmentation.
- Do NOT delete or omit previously established facts when synthesizing the new description.
- Do NOT overwrite a YAML array completely; append to it.

## LANGUAGE RULES
All generated wiki content (summaries, concept names, entity names, syntheses) MUST be written entirely in English, regardless of the raw source file's language. However, source page slugs must remain the kebab-case version of the original raw filename to maintain a direct mapping.

## RELATIONSHIPS & CONTRADICTIONS
Ensure all sub-skills capture relationships in the YAML frontmatter (`relationships` or `related_entities`) and inline wiki-links.
If the source document contains conflicting data with an existing L2 page, then DO NOT overwrite the page; instead, append a `[!contradiction]` callout block detailing the discrepancy and log to `wiki/meta/contradiction-log.md`.

## Steps

1. **Route to Memory Layers**: Execute `python3 .claude/skills/wiki-ingest/scripts/ingest_router.py raw/{file}`
   - This creates an immutable fact node in `memory/L0_facts`.
   - This creates an episode node in `memory/L1_episodes`.
   - NEVER delete the original file from the raw directory.

2. **Chunk**: Run `python3 tools/chunk.py memory/L0_facts/{file_fact_name}` to generate semantic chunks from the L0 fact.

3. **Loop Over Chunks**: For each chunk in `chunks/{slug}/`:
   A. **Plan**: Run `python3 tools/compile_context.py --task plan --chunk {chunk_path}`. Then run `wiki-decompose` to generate `wiki/meta/ingest/{slug}-plan.md`.
   B. **Knowledge Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-knowledge --chunk {chunk_path}`. Call `wiki-ingest-knowledge`.
   C. **Narrative Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-narrative --chunk {chunk_path}`. Call `wiki-ingest-narrative`.
   D. **Reader State Layer** (if touched): Run `python3 tools/compile_context.py --task ingest-reader --chunk {chunk_path}`. Call `wiki-ingest-reader`.

4. **Merge/Dedup Check**: Run `python3 tools/index_manager.py check-duplicate {slug} {type}` on any newly identified complex entities to ensure we haven't created conflicting type representations.

5. **Final Validation**: Run `python3 tools/validate.py --index-only`. If this fails, resolve the structural/index errors before proceeding.

6. **Log**: Append a success entry to `wiki/log.md`.

7. **Cleanup**: Remove the `chunks/{slug}/` directory using `rm -rf`. NEVER move or delete the file from `raw/`.

## Negative Constraints
- NEVER delete the original file from the `raw/` directory.
- NEVER move the original file to `processed/`
- NEVER overwrite existing L2 data if there is a contradiction. Use the `[!contradiction]` block.
- NEVER hallucinate wikilinks to pages that do not exist.
- ALWAYS read existing files completely before updating them.
