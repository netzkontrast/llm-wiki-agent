# Phase 3: Meta Consolidation

**Status:** `active`
**Prerequisites:** Phase 1 and Phase 2 complete

## Overview & Rationale
After evaluating the ingestion flow on a large document (`raw/40ChapterPlotModule.md`) and observing the overall agent behavior, several systemic issues were discovered that prevent the Wiki from acting as a fully robust autonomous system. These primarily center around workflow alignment and context persistence.

### Findings from the Audit:
1. **Contradictions are Ephemeral:** `tools/ingest.py` prints contradictions to standard output. If the system runs headless (as designed), these contradictions disappear forever, breaking the "Error Persistence" rule defined in `todo/meta/README.md`.
2. **Layer-Blind Ingestion:** Phase 1 refactored the wiki into a 4-layer nested layout (knowledge, narrative, reader_state, meta). However, `tools/ingest.py` still creates new files directly in the legacy paths (e.g., `wiki/sources/<slug>.md`). It needs to become layer-aware.
3. **Index Orphan Generation:** The `update_index` function blindly appends to `## Sources` but fails to appropriately route dynamically generated concept and entity pages into the index, leaving them as orphans.
4. **Agent Instruction Desync:** The documentation (`GEMINI.md` and `CLAUDE.md`) hasn't been updated to reflect the new tools created in Phase 2 (`lint_deterministic.py` and `check_staleness.py`). The LLM agents will therefore not execute them autonomously.

This Meta-Consolidation phase bridges these gaps, ensuring the new architectural rules are strictly enforced by the automated tools.

---

## Tasks

### 1. Ingestion Pipeline Layer-Awareness
- [ ] Modify `tools/ingest.py` so it routes files correctly into the 4-layer architecture (e.g., `wiki/knowledge/sources/` instead of `wiki/sources/`).
- [ ] Update the prompt inside `tools/ingest.py` to instruct the LLM to output the correct subdirectories for `entity_pages` and `concept_pages` (e.g. `knowledge/entities/EntityName.md`).

### 2. Contradiction Persistence Protocol
- [ ] Update `tools/ingest.py`: Whenever the LLM identifies a contradiction, the script MUST append it to `wiki/meta/contradiction-log.md` with a timestamp and the slug of the offending source.
- [ ] Modify the ingestion script to prepend a Markdown Warning block to the top of the generated `source_page` if contradictions are detected, alerting agents who load the context that it conflicts with canon.

### 3. Dynamic Index Optimization
- [ ] Rewrite the `update_index` logic in `tools/ingest.py` so that it parses the LLM's `index_entry` output and places it under the correct layer headings (Knowledge, Narrative, Reader State) rather than blindly appending it to `## Sources`.

### 4. Agent Sync & Instructions
- [ ] Update `GEMINI.md` to add `lint deterministic` (which maps to `python tools/lint_deterministic.py`) and `check staleness` (which maps to `python tools/check_staleness.py`).
- [ ] Update `CLAUDE.md` to match these new tool instructions.

### 5. Orchestration Manifest
- [ ] Create `wiki/meta/workflows-manifest.md`. This file should explicitly define the chronological order of operations for autonomous agents to follow after an ingestion event (e.g., Ingest -> Lint Deterministic -> Check Staleness -> Build Graph).

---

## Completion Criteria
- `tools/ingest.py` automatically routes files to their correct layers and logs contradictions to `wiki/meta/contradiction-log.md`.
- Both `GEMINI.md` and `CLAUDE.md` reflect the new Phase 2 commands.
- The `workflows-manifest.md` acts as a central orchestration truth.
