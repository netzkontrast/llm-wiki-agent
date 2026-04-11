# Validation Protocol (Hooks)

This document describes the Validation Hook mechanism used in the novel-writing agent workflows, specifically after generation steps in the `chapter-writing` workflow.

## Purpose

To ensure narrative consistency, maintain the progressive disclosure model, and enforce stylistic and world-building constraints automatically after every generative action.

## Mechanism

After generating or updating content (e.g., writing a beat, drafting manuscript prose, or updating a character), the agent must perform the following validation checks:

1.  **Constraint Compliance:**
    *   Check all rules referenced in the chapter's `constraint_refs:` frontmatter field.
    *   Verify that the newly generated content respects and adheres to these narrative or world-building mandates.
2.  **Terminology Ratchet:**
    *   Check the words and concepts used in the generated content against the `terminology_permitted` list from the applicable reader-state page.
    *   Verify that no unknown or premature terminology is used, preserving the progressive disclosure model.
3.  **Concept Load Check:**
    *   Count the number of *new* concepts introduced in the generated content.
    *   Verify that this count does not exceed the `max_new_concepts` threshold defined for the chapter or workflow.
4.  **Contradiction Check:**
    *   Run standard contradiction checks against existing wiki knowledge, following the contradiction resolution hierarchy (`rule > source > character > chapter > synthesis`).
5.  **Logging:**
    *   Record the results of these validation checks in `wiki/meta/log.md`. Log any warnings, violations, or adjustments made to pass validation.
