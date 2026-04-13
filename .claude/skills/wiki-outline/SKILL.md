---
name: wiki-outline
description: Executes the wiki-outline capability. Use when triggered. Use when the user requests wiki-outline or related tasks.
---

# wiki-outline

# /wiki-outline

**Triggers:** "outline chapter N", "structure chapter N", "plan chapter N beats"

This workflow triggers the outline-writing process.

## Reference
See `docs/agent-workflows.md` and `docs/writing-pipeline.md` for detailed specifications.

## Context Loading:
1. Read chapter spec (`wiki/chapters/chapter-NN.md`)
2. Load characters, conflicts, themes from chapter frontmatter
3. Load arc pages for characters appearing in chapter
4. Load previous chapter's outline (for continuity)
5. Apply temporal filter from chapter target
6. Apply ceiling (15 pages)

## Output:
- Created or updated outline page with beat sequence
- Updated `outline_status`
- Created stub beat pages if `outline_status` moves to `sketched`
