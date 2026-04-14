---
name: wiki-ingest-workflow
description: Complete unified workflow for end-to-end ingestion of a raw file into L0, L1, and L2 layers by utilizing other wiki ingest skills.
---

# wiki-ingest-workflow

This workflow automates the full ingestion process for a specific file. It acts as an orchestrator, executing all the necessary `wiki-ingest-*` skills sequentially while keeping the agent informed of the overall goal: to comprehensively extract ALL entities and facts without skipping, and to synthesize them correctly into the structured Wiki.

## Trigger
Use when the user requests to "ingest a file" or "run the ingest workflow" or refers to end-to-end ingestion of a new raw file.

## Steps

For the file provided (e.g. `raw/{file}`):

### 1. Route to Memory Layers
Execute `python3 .claude/skills/wiki-ingest/scripts/ingest_router.py raw/{file}`
   - *Goal Check*: Ensure the immutable L0 fact node is created in `memory/L0_facts` and the L1 episode node in `memory/L1_episodes`. NEVER delete the original file.

### 2. Chunking
Run `python3 tools/chunk.py memory/L0_facts/{file_fact_name}`
   - *Goal Check*: Ensure the L0 fact file is appropriately divided into smaller semantic chunks in the `chunks/{slug}/` directory.

### 3. Loop Over Chunks
For each chunk generated in `chunks/{slug}/`:

   **A. Plan Extraction**
   - Run `python3 tools/compile_context.py --task plan --chunk {chunk_path}`
   - Read the pre-compiled context.
   - Run `wiki-decompose` to generate `wiki/meta/ingest/{slug}-plan.md` for this chunk. Ensure NO ENTITY IS DEFERRED.

   **B. Ingest Knowledge Layer (if specified in plan)**
   - Run `python3 tools/compile_context.py --task ingest-knowledge --chunk {chunk_path}`
   - Execute `wiki-ingest-knowledge` to draft/update pages.

   **C. Ingest Narrative Layer (if specified in plan)**
   - Run `python3 tools/compile_context.py --task ingest-narrative --chunk {chunk_path}`
   - Execute `wiki-ingest-narrative` to draft/update pages.

   **D. Ingest Reader State Layer (if specified in plan)**
   - Run `python3 tools/compile_context.py --task ingest-reader --chunk {chunk_path}`
   - Execute `wiki-ingest-reader` to draft/update pages.

   **Validation Loop per Chunk**
   - After updating/creating pages for a chunk, run `python3 tools/validate.py --recent-minutes 5`
   - Fix validation errors up to 3 times autonomously.

### 4. Merge / Dedup Verification
Run `python3 tools/index_manager.py check-duplicate {slug} all` on the overall entities found to ensure we haven't created conflicting type representations.

### 5. Final Index Rebuild and Verification
Run `python3 tools/index_manager.py rebuild` to update the index.
Run `python3 tools/validate.py --index-only`. Fix structural/index errors if necessary.

### 6. Logging
Append a success entry to `wiki/log.md` confirming the complete processing of `{file}`.

### 7. Cleanup
Remove the `chunks/{slug}/` directory using `rm -rf`.
*CRITICAL*: NEVER move or delete the file from `raw/`.

## REMINDERS FOR THE ORCHESTRATOR
- **Completeness**: All entities MUST be extracted. No "top 5" or deferrals.
- **Merge Mandate**: Synthesize smoothly. Do not overwrite if a file exists, append lists gracefully, merge text intelligently.
- **Contradictions**: Any discrepancies MUST use `[!contradiction]` tags.
