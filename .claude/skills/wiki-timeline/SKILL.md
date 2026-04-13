---
name: wiki-timeline
description: Executes the wiki-timeline capability. Use when triggered. Use when the user requests wiki-timeline or related tasks.
---

# wiki-timeline

# /wiki-timeline

**Triggers:** "timeline check X", "view timeline X", "edit timeline X"

Use this workflow to manage and analyze the chronological sequence of events within the novel.

## Reference
See `docs/agent-workflows.md` and `docs/navigation-system.md` for detailed specifications regarding temporal filtering.

## Workflow Execution

1.  **Determine Target Range:** Identify the specific timeline events or temporal range requested.
2.  **Context Loading:**
    *   Load relevant timeline-event pages (`wiki/timeline/`).
    *   Load associated chapter pages referenced by the events.
    *   Load characters and locations involved in the events.
    *   Apply a context ceiling of 15 pages.
3.  **Output Generation:**
    *   Update or create timeline events as requested.
    *   Synthesize a timeline view if requested.
    *   Flag any chronological inconsistencies or paradoxes.
4.  **Validation:**
    *   Ensure events are causally coherent and do not violate the established temporal sequence.
    *   Verify that `valid_from` and `valid_until` boundaries align with the updated timeline.


## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
