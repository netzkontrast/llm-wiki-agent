---
name: wiki-manuscript
description: Executes the wiki-manuscript capability. Use when triggered. Use when the user requests wiki-manuscript or related tasks.
---

# wiki-manuscript

# /wiki-manuscript

**Triggers:** "write prose for chapter N", "draft chapter N manuscript", "write chapter N"

This workflow triggers the manuscript-drafting process.

## Reference
See `docs/agent-workflows.md` and `docs/writing-pipeline.md` for detailed specifications.

## Context Loading:
1. Read outline page (must be `detailed` or `locked`)
2. Read all beat pages for the chapter
3. Load POV character's voice profile
4. Load narrative rule pages from chapter's `constraint_refs`
5. Load previous chapter's reader-state
6. Apply ceiling (20 pages)

## Output:
- Created or updated manuscript page with prose
- Updated `manuscript_status` and `word_count`
- Updated reader-state page for this chapter


## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
