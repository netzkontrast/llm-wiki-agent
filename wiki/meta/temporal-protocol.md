# Temporal Protocol

This document outlines the temporal resolution algorithm as an executable checklist. Agents must follow this protocol when loading pages into context for any workflow that has a chapter target.

## Resolution Algorithm

1. **Determine the chapter target position**
   - Read the target chapter's page (e.g., `wiki/chapters/chapter-01.md`).
   - Find the `timeline_start` field in the frontmatter. This points to a timeline-event slug.
   - Look up the corresponding timeline-event page (e.g., `wiki/timeline/001-story-begins.md`) and resolve its `sequence_number`.
   - The target chapter's temporal position is this sequence number.

2. **Filter loaded pages**
   - For each page loaded via the `requires:` chain (up to depth 2):
     - **Check `valid_from` and `valid_until`**:
       - If both are empty: **Always load** the page (it is timeless).
       - If `valid_from` is set: Resolve its `sequence_number`. If the target chapter's sequence number is **less than** this event's sequence number, **skip the page**.
       - If `valid_until` is set: Resolve its `sequence_number`. If the target chapter's sequence number is **greater than or equal to** this event's sequence number, **skip the page**.
       - If both are set: Load the page **only if** the target chapter falls within the window (inclusive of `valid_from` but before `valid_until`).

3. **Resolve Sibling Pages**
   - If a page is skipped due to the temporal filtering step above, look for sibling pages (same base name but with a different temporal suffix, e.g., `Kael.md` vs `Kael-post-frag.md`).
   - Load the correct sibling page that falls within the temporal window.

## Temporal Index Building

To quickly find the sequence numbers of boundary events:
1. Grep all `wiki/timeline/` pages for `is_boundary: true`.
2. Extract and sort by `sequence_number`.
