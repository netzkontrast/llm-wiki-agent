# /wiki-conflict

**Triggers:** "analyze conflict X", "resolve conflict X", "develop conflict X", "conflict status for X", "how does X resolve"

Use this workflow to track and develop narrative conflicts, their escalation, and their resolution across chapters.

## Reference
See `docs/agent-workflows.md` for detailed specifications.

## Workflow Execution

1.  **Temporal Filter:** Resolve from the conflict's `chapter_range` midpoint.
2.  **Context Loading:**
    *   Read the target conflict page (`wiki/conflicts/slug.md`).
    *   Load character pages for the `parties` involved.
    *   Load timeline events within the `chapter_range`.
    *   Load theme pages from `related themes` or `Thematic Connection` section.
    *   Load Dramatica elements if the conflict maps to a throughline.
    *   Apply a context ceiling of 15 pages.
3.  **Output Generation:**
    *   Update the conflict page (escalation trajectory, resolution path).
    *   Update `resolution_status` if the status changed.
    *   If resolved, set `resolution_chapter` and update chapter pages in the `informs:` chain.
4.  **Validation:**
    *   Ensure the resolution is consistent with character arcs (no unjustified deviations from established patterns).
    *   If `self_referential: true`, ensure the resolution addresses the paradox mechanism.
    *   Verify thematic implications of the resolution align with related theme pages.
