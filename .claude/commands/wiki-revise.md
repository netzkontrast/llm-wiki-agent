# /wiki-revise

**Triggers:** "revise chapter N", "revise chapters N-M", "consistency check", "continuity review", "revision pass"

Use this workflow to perform holistic continuity, consistency, and structural reviews across a range of chapters.

## Reference
See `docs/agent-workflows.md` for detailed specifications.

## Workflow Execution

1.  **Temporal Filter:** Apply per-chapter within the specified range.
2.  **Context Loading:**
    *   Read all chapter pages in the target range.
    *   Load timeline events with a `chapter_ref` in the range.
    *   Load rule pages (world, narrative, structural).
    *   Load character arc pages for characters appearing in the range.
    *   Load foreshadowing strands with `planted_chapter` or `intermediate_refs` in the range.
    *   Apply a context ceiling of 30 pages.
3.  **Output Generation:**
    *   Generate revision notes detailing specific issues found, with page references.
    *   Apply straightforward fixes to chapter pages.
    *   Update timeline events if ordering issues are found.
    *   Update foreshadowing statuses if strands are resolved within the range.
4.  **Validation:**
    *   Timeline consistency: events must be causally coherent.
    *   Character arc continuity: ensure no arc stage is skipped.
    *   Rule compliance: ensure chapters do not violate world or structural rules.
    *   Foreshadowing status: planted strands must have `intermediate_refs` or a resolution within the expected range.
    *   Reader-state consistency: ensure `terminology_permitted` is monotonically increasing.
