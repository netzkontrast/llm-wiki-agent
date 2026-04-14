---
name: wiki-character
description: Executes the wiki-character capability. Use when triggered. Use when the user requests wiki-character or related tasks.
---

# wiki-character

# /wiki-character

**Triggers:** "develop character X", "update character X", "profile character X", "who is X"

Use this workflow to create, update, or analyze character profiles within the novel's knowledge base.

## Reference
See `docs/agent-workflows.md` for detailed specifications.

## Workflow Execution

1.  **Temporal Filter:** If a chapter context is provided, apply the temporal filter based on that chapter. Otherwise, load all temporal versions of the character.
2.  **Context Loading:**
    *   Read the target character page (`wiki/characters/Name.md`).
    *   Load the `arc` page for the character's transformation tracking.
    *   Load `relationships` targets (other character pages, depth 1 only).
    *   Load chapter pages where the character appears (read frontmatter `characters:` field only, do not load full chapter content).
    *   Apply a context ceiling of 10 pages.
3.  **Output Generation:**
    *   Update the character page (profile, psychology, voice, relationships).
    *   Update the `arc` page if the transformation stage changed.
    *   Update relationship target pages if relationship dynamics changed.
4.  **Validation:**
    *   Ensure the character is listed in the `characters:` field of every chapter in their `chapter_appearances`.
    *   If modifying an alter, verify the `system` field points to a valid host character.
    *   Check for contradictions with existing character descriptions in source pages.


## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
