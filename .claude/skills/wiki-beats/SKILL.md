---
name: wiki-beats
description: Executes the wiki-beats capability. Use when triggered. Use when the user requests wiki-beats or related tasks.
---

# wiki-beats

# /wiki-beats

**Triggers:** "detail beats for chapter N", "expand beat M of chapter N", "beat-level work on chapter N"

This workflow triggers the beat-detailing process.

## Reference
See `docs/agent-workflows.md` and `docs/writing-pipeline.md` for detailed specifications.

## Context Loading:
1. Read outline page for the chapter
2. Read target beat page(s)
3. Load characters present in each beat
4. Load location for each beat
5. Load active conflicts
6. Load foreshadowing strands referenced
7. Apply ceiling (15 pages)

## Output:
- Updated beat pages with full action, internal, constraints sections
- Updated outline `outline_status` to `detailed` if all beats now have full pages
- Updated foreshadowing strand pages if beats plant/reinforce/resolve strands


## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
