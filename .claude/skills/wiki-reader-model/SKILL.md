---
name: wiki-reader-model
description: Executes the wiki-reader-model capability. Use when triggered. Use when the user requests wiki-reader-model or related tasks.
---

# wiki-reader-model

# /wiki-reader-model

**Triggers:** "reader state for chapter N", "what does the reader know at chapter N", "update reader model", "progressive disclosure check", "foreshadowing status"

Use this workflow to manage progressive disclosure, tracking what the reader knows, learns, and anticipates at a specific point in the narrative.

## Reference
See `docs/agent-workflows.md` and `docs/reader-model.md` for detailed specifications.

## Workflow Execution

1.  **Temporal Filter:** Resolve from the target chapter.
2.  **Context Loading:**
    *   Read the target reader-state page (or create it).
    *   Read the corresponding chapter page.
    *   Load the previous chapter's reader-state for `terminology_permitted` inheritance.
    *   Load foreshadowing strands referenced in `foreshadowing_planted` and `foreshadowing_resolved`.
    *   Load dramatic irony references.
    *   Apply a context ceiling of 10 pages.
3.  **Output Generation:**
    *   Update or create the reader-state page.
    *   Update foreshadowing strand statuses (e.g., planted -> resolved).
    *   Flag any disclosure issues (e.g., concept used before introduction).
4.  **Validation:**
    *   Verify `terminology_permitted` is a superset of the previous chapter's list (one-way ratchet).
    *   Verify the `knows` list is a superset of the previous chapter's `knows` + `learns`.
    *   Ensure foreshadowing strands in `foreshadowing_resolved` are updated to `status: resolved`.
    *   Verify `constraints_active` reference valid, existing rule pages.


## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
