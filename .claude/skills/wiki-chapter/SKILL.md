---
name: wiki-chapter
description: Executes the wiki-chapter capability. Use when triggered. Use when the user requests wiki-chapter or related tasks.
---

# wiki-chapter

# /wiki-chapter

**Triggers:** "write chapter N", "draft chapter N", "continue chapter N", "work on chapter N"

This workflow acts as an orchestrator for the chapter writing pipeline. It delegates to the appropriate sub-workflow based on the current state of the chapter.

## Reference
See `docs/agent-workflows.md` and `docs/writing-pipeline.md` for detailed specifications.

## Workflow Execution

1.  **Determine Target:** Identify the target chapter page (`wiki/chapters/chapter-NN.md`).
2.  **State Assessment:**
    *   Read the target chapter page.
    *   If the chapter has no outline, trigger the `outline-writing` sub-workflow (see `.claude/commands/wiki-outline.md`).
    *   If an outline exists but beats are not detailed, trigger the `beat-detailing` sub-workflow (see `.claude/commands/wiki-beats.md`).
    *   If beats are detailed but no manuscript exists, trigger the `manuscript-drafting` sub-workflow (see `.claude/commands/wiki-manuscript.md`).
    *   If a manuscript exists, trigger the `manuscript-revision` sub-workflow.
3.  **Discovery Hook (`wiki/meta/discovery-protocol.md`):**
    *   Extract `characters:`, `locations:`, `conflicts:`, and `constraint_refs:` from the chapter frontmatter.
    *   Load *only* these referenced pages from `wiki/knowledge/`.
4.  **Context Loading:**
    *   Load the previous chapter's reader-state (`wiki/reader-model/chapter-(N-1)-state.md`).
    *   Apply temporal filtering: skip pages outside the chapter's temporal window.
    *   Apply a context ceiling of 20 pages.
5.  **Output Generation:**
    *   Execute the selected sub-workflow to generate/update the relevant pipeline pages (outline, beats, manuscript).
    *   Update or create the reader-state page (`wiki/reader-model/chapter-NN-state.md`).
    *   Mark `informs:` targets as stale if chapter content changed materially.
6.  **Validation Hook (`wiki/meta/validation-protocol.md`):**
    *   Verify `constraint_refs` compliance (the chapter respects referenced rule pages).
    *   Verify `terminology_permitted` is not violated (no unknown concepts used).
    *   Verify `max_new_concepts` is not exceeded.
    *   Log the validation results in `wiki/meta/log.md`.
    *   Check for contradictions per the contradiction hierarchy.
