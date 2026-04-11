# Workflow Consolidation & Token Efficiency

## Findings from Phase 4 and 5
During the implementation of the complex novel writing pipeline (chapters -> outlines -> beats -> manuscripts), it became clear that the sheer number of markdown files interacting with one another creates a massive Web of `requires` and `informs` links.

### The Ingestion Bottleneck
Running `tools/ingest.py` on a large raw markdown file attempts to parse out Entities, Concepts, Characters, Locations, Themes, Conflicts, Rules, Timeline events, and Foreshadowing all in one massive LLM pass.
- **Risk:** High chance of context truncation (as seen when we tried to read the task list).
- **Risk:** High token cost and slow execution.
- **Risk:** The LLM might silently drop JSON keys if the output token limit is reached.

## Proposed Enhancements

### 1. Multi-Stage Ingestion
Instead of one prompt attempting to extract 9 different page types, `ingest.py` should be refactored into a pipeline:
- **Pass 1:** Summarize the source and extract high-level Concepts/Entities.
- **Pass 2 (Narrative extraction):** Extract Characters, Locations, and Conflicts.
- **Pass 3 (Structural extraction):** Extract Rules, Timeline events, and Foreshadowing.

This mirrors the "adaptive ingest" mentioned in Phase 6 but explicitly breaks down the JSON payload to prevent truncation.

### 2. Dynamic Context Ceilings
The current ceiling of 15-20 pages per workflow is a blunt instrument. We should track token counts dynamically. A page with 5 lines of frontmatter and 2 lines of text should not "cost" the same against the ceiling as a 3000-word manuscript page.
- **Idea:** Create a Python tool (`tools/estimate_context.py`) that returns the token weight of a dependency tree.

### 3. Progressive Disclosure
The addition of READMEs in every subdirectory is a huge win. We should double down on this.
- If an agent needs to know about characters, it should read `wiki/narrative/characters/README.md` first, which lists all characters. It should only load `Kael.md` if specifically needed for the scene.
