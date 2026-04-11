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
