# /wiki-lector

**Triggers:** "lector chapter N", "editorial review of chapter N", "style check chapter N", "proofread chapter N"

Use this workflow to perform detailed editorial review on manuscript drafts, focusing on style, voice, pacing, and thematic alignment.

## Reference
See `docs/agent-workflows.md` for detailed specifications.

## Workflow Execution

1.  **Temporal Filter:** Resolve from the target chapter.
2.  **Context Loading:**
    *   Read the target chapter page (full content if draft exists).
    *   Load the reader-state for this chapter.
    *   Load rule pages with `rule_class: narrative` (style, pacing, concept-load rules).
    *   Load the POV character page (specifically `Voice` and `traits.voice_profile`).
    *   Load theme pages referenced in the chapter's `themes:` field.
    *   Apply a context ceiling of 15 pages.
3.  **Output Generation:**
    *   Generate editorial notes highlighting style issues, voice inconsistencies, and pacing problems.
    *   Provide suggested revisions with reasoning tied to rules or character voice.
    *   Apply straightforward fixes to the chapter page.
4.  **Validation:**
    *   Voice consistency: ensure prose matches the POV character's established voice profile.
    *   Pacing compliance: ensure `tension_level` trajectory aligns with the `pacing` field.
    *   Reader-load: verify `max_new_concepts` is respected.
    *   Terminology: verify no jargon is used before it is permitted by the reader-state.
    *   Style register: ensure prose matches the chapter's `style_register` field.
