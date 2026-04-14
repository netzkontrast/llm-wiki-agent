# Wiki Ingest Workflow Architecture

The `wiki-ingest-workflow` represents a fundamental shift in how the LLM Wiki Agent processes raw documents. Instead of a naive top-to-bottom pass that risks dropping crucial character traits or world rules due to context limits, the system employs an **Adaptive Chunk-Loop**.

## Preparing Data for Writing Workflows

The primary objective of the ingest process in the context of the novel-authoring pipeline is to populate the `narrative` and `knowledge` layers. A robust writing pipeline (Outlines → Beats → Manuscripts) requires perfectly mapped characters, locations, and rules.

Here is how the ingest workflow ensures high-fidelity preparation:

### 1. Immutable L0 Routing
Before any LLM action, raw documents are deterministically routed to `memory/L0_facts`. The original document in `raw/` is never modified or deleted, preserving provenance.

### 2. Semantic Chunking
Large texts are sliced into ~1500-word chunks (`tools/chunk.py`). This guarantees that the LLM has sufficient attention to dedicate to localized details.

### 3. Decompose & Plan (The Context Hook)
For every chunk, the workflow runs `wiki-decompose`. The agent reads the chunk and creates a strict extraction plan. This step explicitly checks for:
- New **Characters** or **Alters**.
- New **Locations**.
- Novel **Rules** or **Concepts**.
- **Contradictions** against established lore.

By forcing a planning phase *before* generation, we eliminate the "deferred entity" problem where an LLM skips extracting minor characters to save tokens.

### 4. Layered Passes
Once the plan is set, the workflow delegates to specialized skills:
- **`wiki-ingest-knowledge`**: Synthesizes global rules, scientific frameworks, and general entities.
- **`wiki-ingest-narrative`**: Focuses entirely on the story: character sheets, timeline events, thematic arcs, and plot conflicts.
- **`wiki-ingest-reader`**: Updates the progressive disclosure ratchet (e.g., foreshadowing planted, terminology permitted).

### 5. The Merge Mandate
When preparing elements for the outline stage, existing entities must grow organically. The workflow strictly enforces semantic merging. For example, if a chunk reveals that the character "Kael" has a new fear, the narrative pass will update `Kael.md` by weaving the new fear into the existing psychological profile, rather than overwriting it or tacking on an isolated update block.

### Handover to the Writing Pipeline
By the time the `wiki-ingest-workflow` completes, the dependency graph is fully populated. When the user subsequently triggers the `/wiki-chapter` workflow, the chapter metadata can seamlessly `require:` the freshly updated character pages, ensuring the beat-writer and manuscript-generator have the absolute latest canon.
