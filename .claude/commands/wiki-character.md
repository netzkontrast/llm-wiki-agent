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
